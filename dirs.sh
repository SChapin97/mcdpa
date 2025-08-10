#!/bin/bash

website_url="$1"

mkdir -p "dirs/$website_url"

while read -r dir; do
    #wc -l dirs/* | grep 'dirs' | grep -v $(wc -l dirs/* | grep 'dirs' | awk -F ' ' '{print $1}' | sort -n | uniq -c | grep -vE '^\s+1 ' | awk -F ' ' '{print $2}' )

    curl -31kL "https://$website_url/$dir" -o "dirs/$website_url/$website_url-$dir.html"
done < privacy_dir_wordlist.txt
