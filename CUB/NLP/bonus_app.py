import re
from bisect import bisect_left
from collections import Counter, defaultdict
from heapq import nlargest
from math import log
from pathlib import Path
from sys import intern

import pandas as pd
import streamlit as st
from st_keyup import st_keyup


DATA_PATH = Path.home() / "Downloads/emails.csv"
TRAINING_EMAILS = 25_000
TOKEN = re.compile(r"[a-z]+(?:'[a-z]+)?")
LAST_TOKEN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?$")
CUT = re.compile(
    r"(?im)^-{2,}\s*(?:original|forwarded) message\s*-{2,}\s*$|^--\s*$"
)
NOISE = re.compile(
    r"(?im)https?://\S+|www\.\S+|\S+@\S+|<[^>]+>|&\w+;|"
    r"^(?:from|to|cc|bcc|sent|date|subject):.*$|^>.*$"
)


def tokenize(message):
    body = message.split("\n\n", 1)[-1]
    body = CUT.split(body, 1)[0]
    return list(map(intern, TOKEN.findall(NOISE.sub(" ", body).lower())))


class SuggestionModel:
    def __init__(self, path, n=2, min_count=2):
        self.n = n
        self.word_counts = Counter()
        self.next_counts = [None] + [defaultdict(Counter) for _ in range(n)]

        for chunk in pd.read_csv(
            path,
            usecols=["message"],
            nrows=TRAINING_EMAILS,
            chunksize=5000,
        ):
            for message in chunk.message.dropna():
                tokens = tokenize(message)
                self.word_counts.update(tokens)
                for i, word in enumerate(tokens):
                    for order in range(1, min(n, i) + 1):
                        self.next_counts[order][tuple(tokens[i - order:i])][word] += 1

        self.total = sum(self.word_counts.values())
        self.vocabulary = sorted(
            word for word, count in self.word_counts.items()
            if count >= min_count
        )

    def complete(self, prefix, k):
        left = bisect_left(self.vocabulary, prefix)
        right = bisect_left(self.vocabulary, prefix + chr(0x10FFFF))
        indices = nlargest(
            k,
            range(left, right),
            key=lambda i: self.word_counts[self.vocabulary[i]],
        )
        return [
            (self.vocabulary[i], self.word_counts[self.vocabulary[i]] / self.total)
            for i in indices
        ]

    def next_words(self, context, k):
        counts = self.word_counts
        for order in range(min(self.n, len(context)), 0, -1):
            found = self.next_counts[order].get(tuple(context[-order:]))
            if found:
                counts = found
                break
        total = sum(counts.values())
        return [(word, count / total) for word, count in counts.most_common(k)]

    def suggest(self, text, n_words=3, n_texts=3):
        tokens = TOKEN.findall(text.lower())
        width = max(10, n_texts * 4)

        if text and text[-1].isspace():
            context = tokens
            starters = self.next_words(context, width)
        elif tokens:
            context = tokens[:-1]
            starters = self.complete(tokens[-1], width)
        else:
            return []

        beam = [
            (log(probability), [word], context + [word])
            for word, probability in starters
        ]
        for _ in range(n_words - 1):
            expanded = []
            for score, words, history in beam:
                for word, probability in self.next_words(history, width):
                    expanded.append(
                        (
                            score + log(probability),
                            words + [word],
                            history + [word],
                        )
                    )
            beam = nlargest(width, expanded, key=lambda item: item[0])

        return [words for _, words, _ in beam[:n_texts]]


def insert_suggestion(text, suggestion):
    continuation = " ".join(suggestion)
    match = LAST_TOKEN.search(text)
    if match:
        return text[:match.start()] + continuation + " "
    separator = "" if not text or text[-1].isspace() else " "
    return text + separator + continuation + " "


@st.cache_resource(show_spinner="Building the n-gram model...")
def load_model():
    return SuggestionModel(DATA_PATH)


def main():
    st.set_page_config(page_title="Text Suggestion", page_icon="✍️")
    st.markdown(
        """
        <style>
        .block-container {max-width: 760px; padding-top: 4rem;}
        .stButton button {text-align: left; border-radius: 12px; height: 3rem;}
        [data-testid="stCaptionContainer"] {font-size: 1rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("✍️ Text Suggestion")
    st.caption("Type an email and choose one of the generated continuations.")

    if not DATA_PATH.exists():
        st.error(f"Dataset not found: {DATA_PATH}")
        st.stop()

    model = load_model()
    left, right = st.columns(2)
    n_words = left.slider("Words in continuation", 1, 5, 3)
    n_texts = right.slider("Number of suggestions", 1, 5, 3)

    if "text" not in st.session_state:
        st.session_state.text = ""
    if "input_version" not in st.session_state:
        st.session_state.input_version = 0

    text = st_keyup(
        "Email",
        value=st.session_state.text,
        key=f"live_input_{st.session_state.input_version}",
        debounce=180,
        placeholder="Please let me kn",
    )
    st.session_state.text = text

    suggestions = model.suggest(text, n_words, n_texts) if text else []
    if suggestions:
        st.caption("Suggestions")
        for index, suggestion in enumerate(suggestions):
            label = " ".join(suggestion)
            if st.button(f"→  {label}", key=f"suggestion_{index}", width="stretch"):
                st.session_state.text = insert_suggestion(text, suggestion)
                st.session_state.input_version += 1
                st.rerun()
    else:
        st.info("Start typing to see suggestions.")


if __name__ == "__main__":
    main()
