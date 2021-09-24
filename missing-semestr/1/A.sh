#! /bin/bash

echo "Enter a String"
# Taking input from user
file='input.txt'
read file

# Counting words
word=$(echo -n "$file" | wc -w)
# Counting characters
char=$(echo -n "$file" | wc -c)

# Counting Number of white spaces (Here,specificly " ")
# sed "s/ change this to whitespace//g"
space=$(expr length "$file" - length `echo "$file" | sed "s/ //g"`)

# Counting special characters
special=$(expr length "${file//[^\~!@#$&*()]/}")

# Output
echo "Number of Words = $word"
echo "Number of Characters = $char"
echo "Number of White Spaces = $space"
echo "Number of Special symbols = $special"
