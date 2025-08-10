# MCDPA (Minnesota Consumer Data Privacy Act)


## Purpose
- To log work done to find out who owns my data, who they sell it to, and other related details that I can use the MCDPA to gather.


### Repro steps:
1. Use [google takeout](https://takeout.google.com/) to download just google mail data
2. Run `get_emails_from_mbox_takeout.sh` with the google takeout file in order to generate a list of business and personal email addresses.
3. Run `valid_domain_finder.sh` with `likely_business_emails.txt` (generated from `get_emails_from_mbox_takeout.sh` in order to generate a list of what the redirect site is. E.g. twitter.com -> x.com
4. Run `privacy_policy_page_finder.sh` on each domain name in order to find privacy policy pages for the domain.


### TODO:
1. Use obsidian or some other data visualization tool to add a file/node so I can map out who has what data and who they give this data to.
2. Figure out a way to find MCDPA-related instructions on the privacy policy pages.
3. Generate a mega script that runs everything from [[Repro steps]] without having to actually run / modify files
