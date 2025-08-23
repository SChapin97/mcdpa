# MCDPA (Minnesota Consumer Data Privacy Act)


## Purpose
- To log work done to find out who owns my data, who they sell it to, and other related details that I can use the MCDPA to gather.
- Currently, this is a collection of scripts to help automate finding and submitting MCDPA / data privacy requests on behalf of the user via Google Takeout .mbox formatted files.
- The plan is to move these scripts into a single automated script and possibly develop some web scrapers for some of the larger corporations who have a web interface for data privacy requests.


## Roadmap and Infrastructure
- MVP (Version One) is a set of bash scripts that has the end goal of finding a list of either emails and/or a list of links to submit your data privacy request(s) based on a Google Takeout email .mbox file. 
    - First, a user must use the Google Takeout service to get an export of their email history. 
        - This will be presented in a .mbox file, where we find every email address that's ever sent the user an email.
            - This is relatively straightforward, but a lot of time savings happens here. 
            - The script currently filters out personal email addresses (essentially if the domain name is `@gmail.com`, `@yahoo.com`, `@aol.com`, etc.)
            - The resulting business emails may be in one of three current statuses:
                1. The domain name / site no longer exists and there is no redirect available, so we discard the email.
                2. The domain name / site exists, but is a redirect from an older or otherwise non-primary domain, in which case we will take the redirected domain as the domain to process (e.g. `twitter.com` redirects to `x.com`, use `x.com` instead of `twitter.com` for finding the privacy policy).
                3. The domain name / site is valid, no redirects or other processing required.
            - The resulting (and distinct) domain names are then added to a list that is used in another script in an attempt to find the privacy page(s) for that domain.
                - The easiest / most straightforward way I can think of doing this is to use the `sitemap.xml` file (e.g. `https://www.x.com/sitemap.xml`) which should be present in almost every website that we *can* do data privacy requests for (e.g. the MCDPA [excludes businesses that have records on less than 100,000 Minnesota residents or earn less than 25% of revenue from sale of personal data while controlling records on less than 25,000 consumers.](https://web.archive.org/web/20250823032748/https://www.ag.state.mn.us/Office/Communications/2025/07/28_MCDPA.asp))
            - There are three situations for which the script(s) need to handle in order to find the correct (or most helpful) avenue for allowing the user to submit a data privacy request:
                1. There is a dedicated data privacy request page where these types of requests should be submitted.
                    - This is generally a pain point as these are almost certainly all different and there's really no way to automate any of this in the scope of this project (or at least in a timely fashion). Warning: rambling ahead.
                        - Theoretically you could create a ""web scraper"" for the top X number of companies that would have this sort of implementation, but that's a bit lacking.
                        - Theoretically you could utilize an LLM to create a web scraper, but this has its own set of problems (repeatability/reliability, whether or not the guardrails will allow you to do this in the first place, extra headache with setting it up unless you had a sort of one-and-done method of creating a shell or python script that you would make public once and forget about it until someone creates a github issue or something (or write tests but you also have to think about getting IP blacklisted and all sorts of other fun things)).
                        - Theoretically you could crowdsource this, but I highly doubt that this idea will get popular enough to really get enough traction for this approach to make sense.
                2. The company wants you to email them your privacy request.
                    - This is probably the easiest way of implementing this sort of thing. Just add your personal information to an env file and add that to a template and you're off to the races.
                3. The company wants you to call them, send snail mail, write a haiku, etc.
                    - PITA, but the MCDPA doesn't explicitly disallow this from happening. In fact, the official [templates](https://www.ag.state.mn.us/Data-Privacy/Consumer/) seem to be snail-mail focused. Annoying.
                4. Secret fourth option: the company doesn't actually have a method for data privacy requests, in which case you can play the fun game of "cc the office of the attorney general and grab a bucket of popcorn to watch the toil of a half-dozen underpaid contractors rush to implement data privacy regulations they had over a year to implement". That game gets even more fun in February 2026 when the ["Cure Period"](web.archive.org/web/20250823032748/https://www.ag.state.mn.us/Office/Communications/2025/07/28_MCDPA.asp) (where a company has 30 days to get into compliance with the law) ends.
                    - This is honestly the one part of the whole research project I'm looking forward to seeing if this does end up happening. That's a great talking point for publicizing this project/journey in a blogpost or security conference talk.
    - The MVP stage should actually be a mostly feature-complete implementation. I don't want to try to clean this up before I learn more about the process and any additional unhappy paths I need to worry about. That's an easy way for this project to die prematurely.
- Version Two ("one click solution")
    - Okay, I admit "one click" is a very simplified and outright wrong way of describing this stage.
    - I basically want to move this to a "single Python script" (read: hopefully object oriented program but the idea behind this project isn't exactly lending itself to an object oriented approach) that you can give your .mbox file to and it'll do all the work without having to look at a reproduction step guide and have to debug edge cases I didn't encounter yet via return code and debug mode flags.
        - Theoretically want to do this in Python so I can implement a crude Django app and have it be relatively easy for non-technically fluent people to run without having to figure out how to install WSL or how to install and run docker.
            - Not entirely sure how I would "host" or run this on your average computer, but we'll cross that bridge when we get to it.
    - Other "nice to haves" that version two should strive to implement to be more "feature complete"
        - Automated way of grabbing the Google Takeout file?
            - May be very hard and not worth it, probably have to jump through a lot of Google OAuth hoops to do this, and doing it via web scraper is probably a no-no.
        - Some sort of easier way to identify the type of data privacy request and/or the "real" privacy policy page? 
            - Trying to grep for specifics in a privacy policy page is a little rough, especially when there's a ton of candidates for the "real" privacy policy page when the sitemap has a number of different pages that have "privacy" in the title.
            - *Maybe* do some sort of LLM summarization for pages and have it rank each page, but getting that to run on someone's machine is a bit of a hurdle, even with smaller ollama models and some way to automate installation.
                - Maybe there's a non-LLM focused way of doing this sort of heuristics? I kinda doubt it unless you did some sort of like wordmap-like distribution and ranked it based on legalese terms with some sort of ranked-word-dictionary hashmap or something. Way out of scope.
        - Integrate automation for data privacy requests for at least the biggest offenders from the [BADBOOL](https://github.com/yaelwrites/Big-Ass-Data-Broker-Opt-Out-List) list of data brokers.
            - Probably do some research first on what types of FOSS is out there already, but this is pretty much 80+% of what services like DeleteMe and Incogni do -- automate data privacy deletion requests for these data brokers.
                - This is something that is interesting to me, is probably out of scope for this but a lot of the lessons from this project/research/journey can be used to implement this sort of thing. Maybe put it in a separate repo if there's a real need for this.



### Version One Repro steps:
1. Use [google takeout](https://takeout.google.com/) to download just google mail data
2. Run `get_emails_from_mbox_takeout.sh` with the google takeout file in order to generate a list of business and personal email addresses.
3. Run `valid_domain_finder.sh` with `likely_business_emails.txt` (generated from `get_emails_from_mbox_takeout.sh` in order to generate a list of what the redirect site is. E.g. twitter.com -> x.com
4. Run `privacy_policy_page_finder.sh` on each domain name in order to find privacy policy pages for the domain.


### TODO:
1. Use obsidian or some other data visualization tool to add a file/node so I can map out who has what data and who they give this data to.
2. Figure out a way to find MCDPA-related instructions on the privacy policy pages.
3. Generate a mega script that runs everything from [[Repro steps]] without having to actually run / modify files
4. Implement additional logic for data brokers from the [BADBOOL](https://github.com/yaelwrites/Big-Ass-Data-Broker-Opt-Out-List) data broker list here on github.
    - Automation would be nice here, especially for the "high severity" targets.
