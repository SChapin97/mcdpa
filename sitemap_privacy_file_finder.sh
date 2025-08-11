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

cat "$sitemap_file"  | grep -Ei 'privacy|mcdpa|gdpr|ccpa|vcdpa|cpa|ctdpa|ucpa' > tmp_privacy_links.txt

if ! [ -s "$privacy_links" ]; then
    echo "$website_url" >> no_privacy_links_on_sitemap.txt
fi

while read -r line; do
    # TODO cleanup xml
    echo "$line"
    url=$(echo "$line" | sed -E 's|<[^>]+>|\n|g' | grep http)
    filename=$(echo "$url" | sed 's|.*/||g')
    curl -kL -m 30 "$url" -o "output/privacy_policy_pages/$website_url/$filename"
done < tmp_privacy_links.txt

rm tmp_privacy_links.txt
