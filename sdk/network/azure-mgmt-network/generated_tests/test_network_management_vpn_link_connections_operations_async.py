# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.network.aio import NetworkManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer
from devtools_testutils.aio import recorded_by_proxy_async

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestNetworkManagementVpnLinkConnectionsOperationsAsync(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(NetworkManagementClient, is_async=True)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_vpn_link_connections_begin_reset_connection(self, resource_group):
        response = await (
            await self.client.vpn_link_connections.begin_reset_connection(
                resource_group_name=resource_group.name,
                gateway_name="str",
                connection_name="str",
                link_connection_name="str",
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_vpn_link_connections_get_all_shared_keys(self, resource_group):
        response = self.client.vpn_link_connections.get_all_shared_keys(
            resource_group_name=resource_group.name,
            gateway_name="str",
            connection_name="str",
            link_connection_name="str",
            api_version="2024-07-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_vpn_link_connections_get_default_shared_key(self, resource_group):
        response = await self.client.vpn_link_connections.get_default_shared_key(
            resource_group_name=resource_group.name,
            gateway_name="str",
            connection_name="str",
            link_connection_name="str",
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_vpn_link_connections_begin_set_or_init_default_shared_key(self, resource_group):
        response = await (
            await self.client.vpn_link_connections.begin_set_or_init_default_shared_key(
                resource_group_name=resource_group.name,
                gateway_name="str",
                connection_name="str",
                link_connection_name="str",
                connection_shared_key_parameters={
                    "id": "str",
                    "name": "str",
                    "properties": {"provisioningState": "str", "sharedKey": "str", "sharedKeyLength": 0},
                    "type": "str",
                },
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_vpn_link_connections_list_default_shared_key(self, resource_group):
        response = await self.client.vpn_link_connections.list_default_shared_key(
            resource_group_name=resource_group.name,
            gateway_name="str",
            connection_name="str",
            link_connection_name="str",
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_vpn_link_connections_begin_get_ike_sas(self, resource_group):
        response = await (
            await self.client.vpn_link_connections.begin_get_ike_sas(
                resource_group_name=resource_group.name,
                gateway_name="str",
                connection_name="str",
                link_connection_name="str",
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_vpn_link_connections_list_by_vpn_connection(self, resource_group):
        response = self.client.vpn_link_connections.list_by_vpn_connection(
            resource_group_name=resource_group.name,
            gateway_name="str",
            connection_name="str",
            api_version="2024-07-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...
