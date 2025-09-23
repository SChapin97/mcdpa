#!/bin/bash

main () {
    if [ "$#" -ne 1 ]; then
        echo "This script requires a website URL to work. URL format: example.com instead of https://example.com/"
        echo "Usage: sh privacy_policy_page_finder.sh example.com"
        exit 1
    fi

    website_url="$1"

    mkdir -p "output/privacy_policy_pages/$website_url"

    homepage_file="output/privacy_policy_pages/$website_url/$website_url-homepage.html"
    curl_with_error_handling "https://$website_url/" "$homepage_file"

    if ! [ -f "$homepage_file" ]; then
        echo "$website_url" >> no_homepage.txt
        exit 1
    fi

    # Try hardcoded "privacy-policy" URL first since that's often the correct page.
    privacy_policy_file="output/privacy_policy_pages/$website_url/$website_url-privacy-policy.html"
    curl_with_error_handling "https://$website_url/privacy-policy" "$privacy_policy_file"

    if [ -f "$privacy_policy_file" ]; then
        exit 0
    fi

    privacy_policy_candidates=$(grep -i 'privacy' "$homepage_file" | tr '>' '\n' | grep '<a' | sed 's/.*href=\"/\n/g' | grep -i privacy | sed -E "s|^/|https://$website_url/|g" | awk -F '"' '{print $1}')
    for candidate in $privacy_policy_candidates; do
        cleaned_up_filename=$(echo "$candidate" | sed 's|https://||g' | sed 's/\./_dot_/g' | sed 's|/|_slash_|g' | sed 's/#/_octothorpe_/g')
        candidate_file="output/privacy_policy_pages/$website_url/$website_url-$cleaned_up_filename.html"

        # Can have collision in filenames, like "https://example.com/privacy-policy" and "https://example.com/privacy-policy/#ad-choices
        if [ -f "$candidate_file" ]; then
            continue
        fi

        curl_with_error_handling "$candidate" "$candidate_file"
    done
}

# $1 == website to curl
# $2 == file to output to
curl_with_error_handling () {
    url=$1
    file=$2
    curl -fkL -m 15 "$url" -o "$file"
    curl_rc="$?"
    if [ "$curl_rc" -ne 0 ]; then
        return
    elif ! [ -f "$file" ]; then
        return
    fi

    if [ $(file "$file" | grep -c 'gzip compressed') -gt 0 ]; then
        # Because we aren't saving as ".gz", we need to use -c for STDOUT to uncompress the gzip file
        gunzip -c "$file" > tmpfile
        mv tmpfile "$file"
    fi

    # Error handling based on strings on the page
    if [ $(echo "$url" | grep -i 'privacy') -gt 0 ]; then
        # Privacy policy should have the words "privacy" and "policy", however not necessarily next to each other.
        if [ $(grep -icE "privacy|policy" "$file") -eq 0 ]; then
            rm "$file"
            return
        fi
    else
        # Homepage string checking
        if [ $(grep -icE "contact|policy|email|support|faq" "$file") -eq 0 ]; then
            rm "$file"
            return
        fi
    fi
    # Error handling based on file size
    if [ $(stat --printf="%s" "$file") -lt 2048 ]; then
        rm "$file"
        return
    fi
}

main "$1"
