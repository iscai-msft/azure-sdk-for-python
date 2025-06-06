# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from azure.identity import DefaultAzureCredential

from azure.mgmt.recoveryservicesbackup.activestamp import RecoveryServicesBackupClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-recoveryservicesbackup
# USAGE
    python trigger_restore_resource_guard_enabled.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = RecoveryServicesBackupClient(
        credential=DefaultAzureCredential(),
        subscription_id="00000000-0000-0000-0000-000000000000",
    )

    client.restores.begin_trigger(
        vault_name="testVault",
        resource_group_name="netsdktestrg",
        fabric_name="Azure",
        container_name="IaasVMContainer;iaasvmcontainerv2;netsdktestrg;netvmtestv2vm1",
        protected_item_name="VM;iaasvmcontainerv2;netsdktestrg;netvmtestv2vm1",
        recovery_point_id="348916168024334",
        parameters={
            "properties": {
                "createNewCloudService": True,
                "encryptionDetails": {"encryptionEnabled": False},
                "identityBasedRestoreDetails": {
                    "targetStorageAccountId": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/testingRg/providers/Microsoft.Storage/storageAccounts/testAccount"
                },
                "identityInfo": {
                    "isSystemAssignedIdentity": False,
                    "managedIdentityResourceId": "/subscriptions/00000000-0000-0000-0000-000000000000/resourcegroups/asmaskarRG1/providers/Microsoft.ManagedIdentity/userAssignedIdentities/asmaskartestmsi",
                },
                "objectType": "IaasVMRestoreRequest",
                "originalStorageAccountOption": False,
                "recoveryPointId": "348916168024334",
                "recoveryType": "RestoreDisks",
                "region": "southeastasia",
                "resourceGuardOperationRequests": [
                    "/subscriptions/063bf7bc-e4dc-4cde-8840-8416fbd7921e/resourcegroups/ankurRG1/providers/Microsoft.DataProtection/resourceGuards/RG341/triggerRestoreRequests/default"
                ],
                "sourceResourceId": "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/netsdktestrg/providers/Microsoft.Compute/virtualMachines/netvmtestv2vm1",
            }
        },
    ).result()


# x-ms-original-file: specification/recoveryservicesbackup/resource-manager/Microsoft.RecoveryServices/stable/2025-02-01/examples/AzureIaasVm/TriggerRestore_ResourceGuardEnabled.json
if __name__ == "__main__":
    main()
