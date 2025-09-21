## Exercise 1 

I write most of my code in ML, so all my arguments and experience will be related to this area. Obviously, various LLMs and agents have made huge technological leaps in the last three years. Very often, my colleagues and I encounter the following pipeline at work: a task is given in natural language, then LLM (most often GPT-5) is used to generate code that solves this task. This code is then tested, and if everything is OK, it's a win. If something goes wrong, LLM is used to generate an explanation or correction. And so on until victory is achieved. Only when everything goes completely wrong does a human read the entire code and try to understand what went wrong. And the integration of such a pipeline is the biggest difference.

## Exercise 2

In the coming years, I expect to see further development of LLM and agents that will be able to solve increasingly complex tasks. Moreover, this improvement will be exponential. Already now, you can look at the ICPC results and compare how the DeepMind and OpenAI teams solved tasks in 2022 and 2023. Previously, models performed at the level of the top teams, while this year, the OpenAI model solved all the tasks and demonstrated the superiority of LLM over the best students, showcasing the level of LLM programming. I also expect to see deeper integration of such models into IDEs and other developer tools (for writing tests, documentation, the code itself, etc.). I also expect to see more zero-code solutions, where a person simply describes a task in natural language, and the system itself generates the code, tests, and everything else needed to solve the task.

## Exercise 3

Programming languages like Python could introduce built-in primitives or libraries for interacting with LLMs, enabling seamless code generation and validation within the language syntax. For example, a llm_generate keyword could invoke an LLM to produce code snippets or tests directly in the editor. One could also try to create a new programming language that would be initially tailored for interaction with LLM. For example, one could introduce new constructs for describing a task in natural language, and LLM would generate code to solve this task in its programming language.

## Exercise 4

The modern development flow, particularly in AI/ML contexts, emphasizes LLM-driven workflows: natural language prompts generating code, iterative debugging with AI agents, seamless IDE integration, and rapid prototyping with low-code elements. To evaluate if a programming language aligns with this, we can use a combination of quantitative benchmarks, empirical studies, and ecosystem analyses. 

| Metric | Description | Measurement Method | Example Tools |
|--------|-------------|-------------------|---------------|
| **LLM Code Accuracy** | How well LLMs generate correct code | Pass@k (e.g., >50% Pass@1) on benchmarks | HumanEval, MultiPL-E |
| **Code Quality** | Maintainability of AI-generated code | Defect density, complexity (<10) | Pylint, SonarQube |
| **Productivity Gains** | Speedup in coding tasks | Task completion time (e.g., >30% faster) | Git analytics, RCTs |
| **Tooling Integration** | Support for AI agents, IDE plugins | % repos with LLM tools, library count | VS Code plugins, PyTorch |
| **Ecosystem Maturity** | Availability of AI/ML libraries | Number of AI/ML libraries, community size | PyPI stats, GitHub stars |

## Exercise 5

[Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)

[Research: quantifying GitHub Copilot’s impact on developer productivity and happiness](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/)


### References

1. [DeepMind AI’s success at ICPC](https://deepmind.google/discover/blog/gemini-achieves-gold-level-performance-at-the-international-collegiate-programming-contest-world-finals/)

2. [OpenAI’s GPT-5 at ICPC](https://news.ycombinator.com/item?id=45279357)

3. [AI in IDE](https://blog.jetbrains.com/ai/2025/02/ai-assistant-expands-with-cutting-edge-models/)