"""Emit nonsecret account mapping requirements without credentials or network."""

import json


def inventory():
    return {
        "schema_version": 1,
        "generation_authorized": False,
        "credentials_read": False,
        "provider_accessed": False,
        "historical_account_attribution": "UNKNOWN",
        "aggregate_ledger_migration": "NOT_PERFORMED",
        "accounts": [
            {
                "credential_variable": f"GROQ_API_KEY_{index}",
                "account_alias": f"user-asserted-account-{index}",
                "distinct_account_source": "user_statement",
                "organization_identity_verified": False,
                "free_billing_verified": False,
                "remaining_daily_tokens": "PENDING",
            }
            for index in range(1, 5)
        ],
        "required_evidence": [
            "Map each variable to its organization in the authenticated console.",
            "Verify Free billing for each organization without recording secrets.",
            "Reconcile historical and unknown usage conservatively before rotation.",
            "Validate transport migration and freeze a candidate before generation.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(inventory(), indent=2, sort_keys=True))
