#!/bin/sh

TEMPFILE="likely_business_emails.txt"
TEMPFILE2="temp_emails.txt"
TEMPFILE3="likely_personal_emails.txt"

if [ "$#" -ne 2 ]; then
   echo "This script needs to be run with the following syntax:"
   echo "sh get_emails_from_mbox_takeout.sh <input file> <name for output directory in output/name>"
   exit 1
fi

input_file="$1"
directory="$2"

if ! [ -f "$input_file" ] ; then
    echo "Input file not found: $input_file"
    echo "Please use a valid file (.mbox) to proceed"
    exit 1
fi


# Get all of the raw email files from the input file
grep -E '^From:|^Reply-To' "$input_file" | sed -r 's/.*\s(<?)(\S+@+.*)(>?)/\2/g' | sed 's/>.*//g' | sed 's/.*<//g' > "$TEMPFILE"

# Make sure we're dealing with a .mbox file
if [ $(wc -l "$TEMPFILE" | awk -F ' ' '{print $1}') -eq 0 ]; then
    echo "No emails found in file $input_file -- make sure this is a .mbox formatted file"
    rm "$TEMPFILE"
    exit 1
fi

# Remove "special characters" from file, additional formatting
sed -i 's/"//g' "$TEMPFILE"
sed -i 's/\[//g' "$TEMPFILE"
sed -i 's/\]//g' "$TEMPFILE"
sed -i 's/\s*$//g' "$TEMPFILE"
sed -i 's/^\s*//g' "$TEMPFILE"
cat "$TEMPFILE" | tr "[[:upper:]]" "[[:lower:]]" | grep "\." > "$TEMPFILE2"
mv "$TEMPFILE2" "$TEMPFILE"


# Save hosted email domains from being filtered out (e.g. friend@gmail.com or employer@hotmail.net). This isn't everything, YMMV
grep -E "gmail.com|yahoo|hotmail|aol.com|msn|yandex|comcast|live.com|outlook.com" "$TEMPFILE" | sort -u > "$TEMPFILE3"
sort -u "$TEMPFILE" > "$TEMPFILE2"
comm -23 "$TEMPFILE2" "$TEMPFILE3" > "$TEMPFILE"
rm "$TEMPFILE2"


# Remove subdomains
cat "$TEMPFILE" | awk -F '@' '{print $2}' | sed 's/\s*$//g' | tr "[:upper:]" "[:lower:]" | perl -pe 's/(.*\.)([a-zA-Z\-]+\.\w+$)/\2/' > "$TEMPFILE2"
mv "$TEMPFILE2" "$TEMPFILE"


# Cleanup -- sort all the unique emails now that formatting is done
cat "$TEMPFILE" | sort -u > "$TEMPFILE2"
mv "$TEMPFILE2" "$TEMPFILE"


# Move to output directory
mkdir -p "output"
mkdir -p "output/$directory"
mv "$TEMPFILE" "output/$directory/"
mv "$TEMPFILE3" "output/$directory/"

