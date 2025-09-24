from time import sleep
from typing import Optional
from savepagenow.exceptions import WaybackRuntimeError

import savepagenow

# TODO: Use the official package if that can be easily migrated -- `internetarchive`
# Official API documentation: https://archive.org/developers/internetarchive/api.html


class ArchiveDotOrg:

    @staticmethod
    def archive_webpage(url: str) -> Optional[str]:

        print(f"DEBUG: Archiving url {url}")
        try:
            archive_url, new_archive = savepagenow.capture_or_cache(url)
        except WaybackRuntimeError as wre:
            print(f"ERROR: WaybackRuntimeError -- url: {url} ; full error: {wre}")
            return None

        print(f"DEBUG: internet archive URL: {archive_url}")

        if new_archive:
            print("DEBUG: Internet Archive created a new archive. Sleeping to reduce throttling risk.")
            sleep(2)

        return archive_url
