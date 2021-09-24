file='input.txt'
word=`wc -w < $file`
char=$(grep -o "[[:alpha:]]" "$file" | wc -l)
lines=`wc -l < $file`

echo "Input file contains:" > 'output.txt'
echo "$char letters" >> 'output.txt'
echo "$word words" >> 'output.txt'
echo "$lines lines" >> 'output.txt'
