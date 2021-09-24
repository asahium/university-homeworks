#!/bin/bash
i=0
res=0
while read str
do
if [$i -eq 0]
then
$res=res + $str
echo "$res" > 'output.txt'
