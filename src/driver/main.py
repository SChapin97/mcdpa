import json
from time import sleep
from typing import Optional

from src.data_models.simple_company_model import CompanyMetadata
from src.database import sqlite_wrapper
from src.database.sqlite_wrapper import SqliteWrapper
from src.external.archive_dot_org import ArchiveDotOrg

FIRST_EXECUTION = False


def main():
    with open("../../input/privacy_policy_urls.json", "r") as f:
        # TODO: Error handling for json load error, file not found, etc.
        privacy_policy_file = json.loads(f.read())

    if FIRST_EXECUTION:
        sqlite_wrapper.init_db()
    database_dao: SqliteWrapper = SqliteWrapper()
    all_company_metadata_records: dict[str, CompanyMetadata] = database_dao.list_all()

    for website_url in privacy_policy_file:
        pretty_website_url: str = f"https://{website_url}/" if "http" not in website_url else website_url
        privacy_policy_url: str = privacy_policy_file[website_url].get("privacy_policy_url")
        archived_privacy_policy_url: Optional[str] = privacy_policy_file[website_url].get("archived_privacy_policy_url")
        archiving_error: bool = False

        if pretty_website_url in all_company_metadata_records:
            print(f"DEBUG: Company present in database: {all_company_metadata_records[pretty_website_url]}")
            continue

        if not archived_privacy_policy_url:
            archived_privacy_policy_url = ArchiveDotOrg.archive_webpage(privacy_policy_url)
            if not archived_privacy_policy_url:
                archiving_error = True

        company: CompanyMetadata = CompanyMetadata(
            website_url=pretty_website_url,
            privacy_policy_url=privacy_policy_url,
            archived_privacy_policy_url=archived_privacy_policy_url,
            archiving_error=archiving_error
        )

        print(f"DEBUG: Company not present in database: {company}")
        database_dao.create(company_name=company.website_url, metadata=company)


if __name__ == "__main__":
    main()
