#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "This script requires a website URL to work. URL format: example.com instead of https://example.com/"
    echo "Usage: sh privacy_policy_page_finder.sh example.com"
    exit 1
fi

website_url="$1"

mkdir -p "output/privacy_policy_pages/$website_url"

while read -r dir; do
    curl -31kL "https://$website_url/$dir" -o "output/privacy_policy_pages/$website_url/$website_url-$dir.html"
done < privacy_dir_wordlist.txt

wc -l output/privacy_policy_pages/$website_url/* 2> /dev/null | grep 'privacy_policy_pages' | grep -v $(wc -l output/privacy_policy_pages/$website_url/* 2> /dev/null | grep 'privacy_policy_pages' | awk -F ' ' '{print $1}' | sort -n | uniq -c | grep -vE '^\s+1 ' | awk -F ' ' '{print $2}' ) | grep html | awk -F ' ' '{print $2}' > good_files.txt

mkdir -p "output/privacy_policy_pages/good_files/"
while read -r line; do
    cp "$line" "output/privacy_policy_pages/good_files/"
done < good_files.txt

rm good_files.txt
