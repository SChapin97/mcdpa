from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Address:
    street_address: str
    city: str
    state: str
    zip_code: str
    country: str


@dataclass_json
@dataclass
class CompanyMetadata:
    address: Address
    industry: str
    legal_email: str
    name: str
    phone_number: str


@dataclass_json
@dataclass
class ConsumerCompanyRelationship:
    origin_name: str
    origin_type: str


@dataclass_json
@dataclass
class DataCollected:
    behavioral_data: bool
    biometric_data: bool
    communications_content: bool
    contact_information: bool
    employment_and_education_data: bool
    derived_or_inferred_data: bool
    financial_information: bool
    health_data: bool
    identifying_information: bool
    location_data: bool
    marketing_data: bool
    preference_data: bool
    transaction_history: bool


@dataclass_json
@dataclass
class DataPrivacyRequestMetadata:
    date_of_last_deletion_request: str
    data_privacy_request_method: str
    date_requested: str
    date_responded: str
    date_response_required: str
    has_data: bool
    has_deleted_data: bool
    has_state_level_privacy_policy_language: bool
    is_mcdpa_eligible: bool
    privacy_email: str
    state_level_privacy_policy_excerpt: str
    verification_requested: bool
    verification_reasoning: str


@dataclass_json
@dataclass
class RiskAssessment:
    confidence_score: float
    risk_level: str
    notes: str


@dataclass_json
@dataclass
class ScraperMetadata:
    curl_compatible: bool
    has_scraper: bool
    has_web_form: bool
    last_automated_scraper_run_date: str
    selenium_compatible: bool
    web_form_automatable: bool


@dataclass_json
@dataclass
class ThirdPartyRecipient:
    company_id: int
    category_of_recipient: str
    name: str
    is_data_broker: bool
    website: str


@dataclass_json
@dataclass
class ThirdPartySharing:
    recipients: List[ThirdPartyRecipient]


@dataclass_json
@dataclass
class WebPresence:
    privacy_policy_archive_url: str
    privacy_policy_url: str
    url: str


@dataclass_json
@dataclass
class CompanyPrivacyRecord:
    company_metadata: CompanyMetadata
    consumer_company_relationship: ConsumerCompanyRelationship
    data_collected: Optional[DataCollected]
    data_privacy_request_metadata: DataPrivacyRequestMetadata
    notes: Optional[str]
    risk_assessment: Optional[RiskAssessment]
    scraper_metadata: ScraperMetadata
    third_party_sharing: Optional[ThirdPartySharing]
    web_presence: Optional[WebPresence]
