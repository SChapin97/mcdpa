#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "This script requires a website URL to work. URL format: example.com instead of https://example.com/"
    echo "Usage: sh privacy_policy_page_finder.sh example.com"
    exit 1
fi

website_url="$1"

mkdir -p "output/privacy_policy_pages/$website_url"

sitemap_file="output/privacy_policy_pages/$website_url/$website_url-sitemap.xml"
curl -kL -m 30 "https://$website_url/sitemap.xml" -o "$sitemap_file"

if ! [ -s "$sitemap_file" ]; then
    echo "$website_url" >> no_sitemap.txt
    exit 1
fi

privacy_links="tmp_privacy_links.txt"
cat "$sitemap_file" | tr '<' '\n' | grep 'http' | sed 's/.*http/http/g' | sed 's/>.*//g' | tr -d '"' | tr -d "'" | sort -u | grep -Ei 'privacy|data|gdpr|ccpa|mcdpr' | sed 's/ .*//g' > "$privacy_links"

if ! [ -s "$privacy_links" ]; then
    echo "$website_url" >> no_privacy_links_on_sitemap.txt
fi

:> curl_log.txt
while read -r line; do
    echo "$line"
    echo "$line" >> curl_log.txt
    filename=$(echo "$line" | sed -E 's|/$||g' | sed 's|.*/||g')
    curl -kL -m 30 "$line" -o "output/privacy_policy_pages/$website_url/$filename"
done < "$privacy_links"

rm "$privacy_links"
