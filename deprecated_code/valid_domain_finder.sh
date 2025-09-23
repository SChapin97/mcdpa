#!/bin/sh

#TEMPFILE="temp_curl_file.txt"

if [ "$#" -ne 2 ]; then
   echo "This script needs to be run with the following syntax:"
   echo "sh valid_domain_finder.sh <input file> <directory name for website files>"
   exit 1
fi

input_file="$1"
output_directory="$2"
OUTPUT_PATH="output/$output_directory/sites"

if ! [ -f "$input_file" ] ; then
    echo "Input file not found: $input_file"
    echo "Please use a valid text to proceed"
    exit 1
fi

mkdir -p "$OUTPUT_PATH"
# Clean up files so we don't get a lot of overlapping output lines
for file in $(find "$OUTPUT_PATH" -type f ); do
    :> "$file"
done

while read -r line; do
    if [ $(echo "$line" | grep -cE '\w') -eq 0 ]; then
        continue
    fi

    current_domain="$line"

    # Curl the website using redirects to find the current site. eg. "twitter.com" redirects to "x.com"
    site_output=$(curl -m 30 -Ls -o /dev/null -w %{url_effective} "$current_domain")
    rc_1="$?"

    if [ "$rc_1" -ne 0 ]; then
        echo "Site does not exist: $current_domain -- return code $rc_1" >> "$OUTPUT_PATH/site_not_found.txt"
    else
        new_domain_name=$(echo "$site_output" | awk -F '/' '{print $3}' | sed 's/www.//g' | sed 's/:443//g')
        echo "$new_domain_name - $current_domain" >> "$OUTPUT_PATH/valid_sites.txt"
    fi


done < "$input_file"
