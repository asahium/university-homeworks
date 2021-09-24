#!/bin/bash
i=0
res=0
while read str
do
if [$i -eq 0]
then
x=$str
$res=$(res + $str)
$i++
fi
if [$i -ne 0]
then
$res=$($res + $str * ( $x ** $i ))
$i++
fi
done
echo "$res" > 'output.txt'
