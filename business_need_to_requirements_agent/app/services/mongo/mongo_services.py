from typing import Dict, Any
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()


class MongoServices:

    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI")
        mongo_database = os.getenv("MONGODB_DATABASE")

        missing_settings = [
            name
            for name, value in {
                "MONGODB_URI": mongo_uri,
                "MONGODB_DATABASE": mongo_database,
            }.items()
            if not value
        ]

        if missing_settings:
            raise ValueError(
                "Missing required MongoDB environment variable(s): "
                + ", ".join(missing_settings)
            )

        self.client = MongoClient(
            mongo_uri
        )

        self.db = self.client[
            mongo_database
        ]

    # ==========================
    # INPUT COLLECTION
    # ==========================

    def get_requirement_input(
        self,
        tender_id: str,
        company_id: str
    ) -> Dict[str, Any]:

        collection = self.db[
            "TenderRequirementDeduplications"
        ]

        document = collection.find_one(
            {
                "TenderId": tender_id,
                "CompanyId": company_id,
                "Status": "Active"
            }
        )

        if not document:
            raise ValueError(
                f"No requirements found for tender={tender_id}"
            )

        final_json = document.get(
            "FinalJson",
            {}
        )

        return {
            "TenderId":
                document.get("TenderId"),

            "CompanyId":
                document.get("CompanyId"),

            "RequirementDeduplicationId":
                document.get(
                    "RequirementDeduplicationId"
                ),

            "RequirementExtractionId":
                document.get(
                    "RequirementExtractionId"
                ),

            "UploadedFileId":
                document.get(
                    "UploadedFileId"
                ),

            "RawRequirementCount":
                document.get(
                    "RawRequirementCount",
                    0
                ),

            "CanonicalRequirementCount":
                document.get(
                    "CanonicalRequirementCount",
                    0
                ),

            "DuplicateRemovedCount":
                document.get(
                    "DuplicateRemovedCount",
                    0
                ),

            "CanonicalRequirements":
                final_json.get(
                    "CanonicalRequirements",
                    []
                ),

            "output_mode":
                "json_only"
        }

    # ==========================
    # OUTPUT COLLECTION
    # ==========================

    def save_requirements(
        self,
        tender_id: str,
        company_id: str,
        requirement_deduplication_id: str,
        output_json: Dict[str, Any]
    ) -> str:

        collection = self.db[
            "FunctionalAndNonFunctionalRequirements"
        ]

        now = datetime.utcnow()

        document = {
            "TenderId":
                tender_id,

            "CompanyId":
                company_id,

            "RequirementDeduplicationId":
                requirement_deduplication_id,

            **output_json,

            "Status":
                "Active",

            "ModifiedDate":
                now
        }

        result = collection.update_one(
            {
                "TenderId": tender_id,
                "CompanyId": company_id
            },
            {
                "$set": document,
                "$setOnInsert": {
                    "CreatedDate": now
                }
            },
            upsert=True
        )

        return (
            str(result.upserted_id)
            if result.upserted_id
            else "updated"
        )
