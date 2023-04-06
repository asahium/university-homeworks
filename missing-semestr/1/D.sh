#!/bin/bash
file="input.txt"
output="output.txt"
reg="(https?:\/\/)?([^:\/]*)(:([0-9]*))?(\/\?)?(.*)"
reg2="([^=]*)=([^=]*)"

sed -i "s/google/yandex/g" $file

for line in $(cat $file)
do
 scheme=$(echo "$line" | sed -E "s/$reg/\1/")
 host=$(echo "$line" | sed -E "s/$reg/\2/")
 port=$(echo "$line" | sed -E "s/$reg/\4/")
 args=$(echo "$line" | sed -E "s/$reg/\6/")
 if [ $scheme ]
 then
  echo "Scheme: $scheme" >> $output
 fi
 if [ $host ]
 then
  echo "Host: $host" >> $output
 fi
 if [ $port ]
 then
  echo "Port: $port" >> $output
 fi
 if [ $args ]
 then
  echo "Args:" >> $output
  for arg in $(echo $args | tr "&" "\n")
  do
   key=$(echo "$arg" | sed -E "s/$reg2/\1/")
   value=$(echo "$arg" | sed -E "s/$reg2/\2/")
   echo "  Key: $key; Value: $value" >> $output
  done
 fi
 echo "" >> $output
done
