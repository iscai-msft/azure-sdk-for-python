# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: get_iana_timezone_ids.py
DESCRIPTION:
    This API returns a full list of IANA time zone IDs. Updates to the IANA service will be reflected in the system within one day.
USAGE:
    python get_iana_timezone_ids.py

    Set the environment variables with your own values before running the sample:
    - AZURE_SUBSCRIPTION_KEY - your subscription key
"""
import os

from azure.core.exceptions import HttpResponseError

subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY", "your subscription key")


def get_iana_timezone_ids():
    from azure.core.credentials import AzureKeyCredential
    from azure.maps.timezone import MapsTimeZoneClient

    timezone_client = MapsTimeZoneClient(credential=AzureKeyCredential(subscription_key))
    try:
        result = timezone_client.get_iana_timezone_ids()
        print(result)
    except HttpResponseError as exception:
        if exception.error is not None:
            print(f"Error Code: {exception.error.code}")
            print(f"Message: {exception.error.message}")


if __name__ == "__main__":
    get_iana_timezone_ids()
