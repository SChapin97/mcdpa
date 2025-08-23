# MCDPA Email Templates

## Overview
- The MCDPA grants Minnesota residents certian data privacy rights. These are defined with the "LOCKED+" acronym (quotations taken directly from the [website for the Office of the Attorney General](https://web.archive.org/web/20250823042316/https://www.ag.state.mn.us/Data-Privacy/Consumer/)):
    - **L**ist
        - "You have a right to request a list of third parties to whom your data was sold."
    - **O**pt-Out
        - "You have a right to opt-out, or say 'no' to a business selling your data, using your data for profiling, or using targeted advertising with your data."
    - **C**opy
        - "You have a right to obtain a copy of the personal and sensitive data a business has about you."
    - **K**now
        - "You have a right to know what information a business has collected about you."
    - **E**dit
        - "You have a right to correct inaccuracies in the data a business has collected about you."
            - Editor's note: This isn't implemented in every state privacy law, this is semi-unique to the MCDPA and may be worth (legally) investigating for research purposes.
                - Example: Data brokers tend to have *very* inaccurate data, so doing an edit request for a not-very-popular data broker may prove interesting to see if they actually comply with the law.
    - **D**elete
        - "You have a right to delete personal and sensitive information that is has collected about you."
    - **+** Question
        - "You have the right to question profiling and automated decisions that affect you"
            - Editor's note: This (I believe) is very unique to Minnesota (and maybe one or two other states). This is super important with "AI classification", especially when the raw data (e.g. data broker data) is wildly inaccurate.

## Email Templates
- This directory contains a number of text files. These files are adapted from the [website for the Office of the Attorney General](https://web.archive.org/web/20250823042316/https://www.ag.state.mn.us/Data-Privacy/Consumer/), which contains a number of snail-mail templates that you're meant to print out and physically send to companies.
    - Instead of a snail-mail template, these have been adapted (and combined) to be email-friendly (both for automation and for Minnesota residents to use directly).
    - There's no specific provision in the MCDPA that states that companies have to make their data privacy requests accessible electronically, so I get it the reasoning behind the template format. I also appreciate the inclusion of the templates as it saves me lawyer fees from drafting professional sounding templates that reference the right subdivisions-and-what-have-yous.
    - The website has the following templates, and I have noted which (if any) email template files are available for these (many of which have been bundled together).
        - [Right to Lists](https://web.archive.org/web/20250823043924/https://www.ag.state.mn.us/Data-Privacy/Consumer/Letters/MCDPA_Template_Letter_sub_h.pdf)
            - [list_know_and_copy.txt](list_know_and_copy.txt)
        - [Right to Opt Out](https://web.archive.org/web/20250823043908/https://www.ag.state.mn.us/Data-Privacy/Consumer/Letters/MCDPA_Template_Letter_sub_f.pdf)
            - [opt-out_and_delete.txt](opt-out_and_delete.txt)
        - [Right to Copy](https://web.archive.org/web/20250823043853/https://www.ag.state.mn.us/Data-Privacy/Consumer/Letters/MCDPA_Template_Letter_sub_e.pdf)
            - Not included, seems to fall under the "list" right but that's my opinion.
        - [Right to Know](https://web.archive.org/web/20250823043824/https://www.ag.state.mn.us/Data-Privacy/Consumer/Letters/MCDPA_Template_Letter_sub_b.pdf)
            - [list_know_and_copy.txt](list_know_and_copy.txt)
        - [Right to Edit](https://web.archive.org/web/20250823043807/https://www.ag.state.mn.us/Data-Privacy/Consumer/Letters/MCDPA_Template_Letter_sub_c.pdf)
            - Not included, in my opinion this is something that should be done as a follow-up email and done with intention instead of using a generic template.
        - [Right to Delete](https://web.archive.org/web/20250823043736/https://www.ag.state.mn.us/Data-Privacy/Consumer/Letters/MCDPA_Template_Letter_sub_d.pdf)
            - [opt-out_and_delete.txt](opt-out_and_delete.txt)
        - [Right to Question Profiling Decisions](https://web.archive.org/web/20250823043625/https://www.ag.state.mn.us/Data-Privacy/Consumer/Letters/MCDPA_Template_Letter_sub_g.pdf)
            - Not included (yet), I want to do more research into this before I really touch anything to do with this.
