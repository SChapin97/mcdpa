from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class CompanyMetadata:
    website_url: Optional[str] = None
    privacy_policy_url: Optional[str] = None
    archived_privacy_policy_url: Optional[str] = None
    archiving_error: Optional[bool] = None
