#!/bin/bash

:> output.txt
pages=1
ret=0
while [ $ret -eq 0 ];
do
    url="https://www.dndwiki.io/monsters?227df1c3_page=$pages"
    ret=$(curl -k $url | tee tmp.txt | grep "No items found." -c)
    cat tmp.txt >> output.txt
    rm tmp.txt
    echo $url
    echo $ret
    pages=$(( $pages + 1))
done
