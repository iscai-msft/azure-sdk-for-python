# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.network import NetworkManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestNetworkManagementVirtualNetworkGatewaysOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(NetworkManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_create_or_update(self, resource_group):
        response = self.client.virtual_network_gateways.begin_create_or_update(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            parameters={
                "activeActive": bool,
                "adminState": "str",
                "allowRemoteVnetTraffic": bool,
                "allowVirtualWanTraffic": bool,
                "autoScaleConfiguration": {"bounds": {"max": 0, "min": 0}},
                "bgpSettings": {
                    "asn": 0,
                    "bgpPeeringAddress": "str",
                    "bgpPeeringAddresses": [
                        {
                            "customBgpIpAddresses": ["str"],
                            "defaultBgpIpAddresses": ["str"],
                            "ipconfigurationId": "str",
                            "tunnelIpAddresses": ["str"],
                        }
                    ],
                    "peerWeight": 0,
                },
                "customRoutes": {
                    "addressPrefixes": ["str"],
                    "ipamPoolPrefixAllocations": [
                        {"allocatedAddressPrefixes": ["str"], "id": "str", "numberOfIpAddresses": "str"}
                    ],
                },
                "disableIPSecReplayProtection": bool,
                "enableBgp": bool,
                "enableBgpRouteTranslationForNat": bool,
                "enableDnsForwarding": bool,
                "enableHighBandwidthVpnGateway": bool,
                "enablePrivateIpAddress": bool,
                "etag": "str",
                "extendedLocation": {"name": "str", "type": "str"},
                "gatewayDefaultSite": {"id": "str"},
                "gatewayType": "str",
                "id": "str",
                "identity": {
                    "principalId": "str",
                    "tenantId": "str",
                    "type": "str",
                    "userAssignedIdentities": {"str": {"clientId": "str", "principalId": "str"}},
                },
                "inboundDnsForwardingEndpoint": "str",
                "ipConfigurations": [
                    {
                        "etag": "str",
                        "id": "str",
                        "name": "str",
                        "privateIPAddress": "str",
                        "privateIPAllocationMethod": "str",
                        "provisioningState": "str",
                        "publicIPAddress": {"id": "str"},
                        "subnet": {"id": "str"},
                    }
                ],
                "location": "str",
                "name": "str",
                "natRules": [
                    {
                        "etag": "str",
                        "externalMappings": [{"addressSpace": "str", "portRange": "str"}],
                        "id": "str",
                        "internalMappings": [{"addressSpace": "str", "portRange": "str"}],
                        "ipConfigurationId": "str",
                        "mode": "str",
                        "name": "str",
                        "provisioningState": "str",
                        "type": "str",
                    }
                ],
                "provisioningState": "str",
                "resiliencyModel": "str",
                "resourceGuid": "str",
                "sku": {"capacity": 0, "name": "str", "tier": "str"},
                "tags": {"str": "str"},
                "type": "str",
                "vNetExtendedLocationResourceId": "str",
                "virtualNetworkGatewayMigrationStatus": {"errorMessage": "str", "phase": "str", "state": "str"},
                "virtualNetworkGatewayPolicyGroups": [
                    {
                        "etag": "str",
                        "id": "str",
                        "isDefault": bool,
                        "name": "str",
                        "policyMembers": [{"attributeType": "str", "attributeValue": "str", "name": "str"}],
                        "priority": 0,
                        "provisioningState": "str",
                        "vngClientConnectionConfigurations": [{"id": "str"}],
                    }
                ],
                "vpnClientConfiguration": {
                    "aadAudience": "str",
                    "aadIssuer": "str",
                    "aadTenant": "str",
                    "radiusServerAddress": "str",
                    "radiusServerSecret": "str",
                    "radiusServers": [
                        {"radiusServerAddress": "str", "radiusServerScore": 0, "radiusServerSecret": "str"}
                    ],
                    "vngClientConnectionConfigurations": [
                        {
                            "etag": "str",
                            "id": "str",
                            "name": "str",
                            "provisioningState": "str",
                            "virtualNetworkGatewayPolicyGroups": [{"id": "str"}],
                            "vpnClientAddressPool": {
                                "addressPrefixes": ["str"],
                                "ipamPoolPrefixAllocations": [
                                    {"allocatedAddressPrefixes": ["str"], "id": "str", "numberOfIpAddresses": "str"}
                                ],
                            },
                        }
                    ],
                    "vpnAuthenticationTypes": ["str"],
                    "vpnClientAddressPool": {
                        "addressPrefixes": ["str"],
                        "ipamPoolPrefixAllocations": [
                            {"allocatedAddressPrefixes": ["str"], "id": "str", "numberOfIpAddresses": "str"}
                        ],
                    },
                    "vpnClientIpsecPolicies": [
                        {
                            "dhGroup": "str",
                            "ikeEncryption": "str",
                            "ikeIntegrity": "str",
                            "ipsecEncryption": "str",
                            "ipsecIntegrity": "str",
                            "pfsGroup": "str",
                            "saDataSizeKilobytes": 0,
                            "saLifeTimeSeconds": 0,
                        }
                    ],
                    "vpnClientProtocols": ["str"],
                    "vpnClientRevokedCertificates": [
                        {"etag": "str", "id": "str", "name": "str", "provisioningState": "str", "thumbprint": "str"}
                    ],
                    "vpnClientRootCertificates": [
                        {"publicCertData": "str", "etag": "str", "id": "str", "name": "str", "provisioningState": "str"}
                    ],
                },
                "vpnGatewayGeneration": "str",
                "vpnType": "str",
            },
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_get(self, resource_group):
        response = self.client.virtual_network_gateways.get(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_delete(self, resource_group):
        response = self.client.virtual_network_gateways.begin_delete(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_update_tags(self, resource_group):
        response = self.client.virtual_network_gateways.begin_update_tags(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            parameters={"tags": {"str": "str"}},
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_list(self, resource_group):
        response = self.client.virtual_network_gateways.list(
            resource_group_name=resource_group.name,
            api_version="2024-07-01",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_list_connections(self, resource_group):
        response = self.client.virtual_network_gateways.list_connections(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_reset(self, resource_group):
        response = self.client.virtual_network_gateways.begin_reset(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_reset_vpn_client_shared_key(self, resource_group):
        response = self.client.virtual_network_gateways.begin_reset_vpn_client_shared_key(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_generatevpnclientpackage(self, resource_group):
        response = self.client.virtual_network_gateways.begin_generatevpnclientpackage(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            parameters={
                "authenticationMethod": "str",
                "clientRootCertificates": ["str"],
                "processorArchitecture": "str",
                "radiusServerAuthCertificate": "str",
            },
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_generate_vpn_profile(self, resource_group):
        response = self.client.virtual_network_gateways.begin_generate_vpn_profile(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            parameters={
                "authenticationMethod": "str",
                "clientRootCertificates": ["str"],
                "processorArchitecture": "str",
                "radiusServerAuthCertificate": "str",
            },
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_vpn_profile_package_url(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_vpn_profile_package_url(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_bgp_peer_status(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_bgp_peer_status(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_supported_vpn_devices(self, resource_group):
        response = self.client.virtual_network_gateways.supported_vpn_devices(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_learned_routes(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_learned_routes(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_advertised_routes(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_advertised_routes(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            peer="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_resiliency_information(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_resiliency_information(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_routes_information(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_routes_information(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_set_vpnclient_ipsec_parameters(self, resource_group):
        response = self.client.virtual_network_gateways.begin_set_vpnclient_ipsec_parameters(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            vpnclient_ipsec_params={
                "dhGroup": "str",
                "ikeEncryption": "str",
                "ikeIntegrity": "str",
                "ipsecEncryption": "str",
                "ipsecIntegrity": "str",
                "pfsGroup": "str",
                "saDataSizeKilobytes": 0,
                "saLifeTimeSeconds": 0,
            },
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_vpnclient_ipsec_parameters(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_vpnclient_ipsec_parameters(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_vpn_device_configuration_script(self, resource_group):
        response = self.client.virtual_network_gateways.vpn_device_configuration_script(
            resource_group_name=resource_group.name,
            virtual_network_gateway_connection_name="str",
            parameters={"deviceFamily": "str", "firmwareVersion": "str", "vendor": "str"},
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_start_packet_capture(self, resource_group):
        response = self.client.virtual_network_gateways.begin_start_packet_capture(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_stop_packet_capture(self, resource_group):
        response = self.client.virtual_network_gateways.begin_stop_packet_capture(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            parameters={"sasUrl": "str"},
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_failover_all_test_details(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_failover_all_test_details(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            type="str",
            fetch_latest=bool,
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_failover_single_test_details(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_failover_single_test_details(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            peering_location="str",
            failover_test_id="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_start_express_route_site_failover_simulation(self, resource_group):
        response = self.client.virtual_network_gateways.begin_start_express_route_site_failover_simulation(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            peering_location="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_stop_express_route_site_failover_simulation(self, resource_group):
        response = self.client.virtual_network_gateways.begin_stop_express_route_site_failover_simulation(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            stop_parameters={
                "details": [{"failoverConnectionName": "str", "failoverLocation": "str", "isVerified": bool}],
                "peeringLocation": "str",
                "wasSimulationSuccessful": bool,
            },
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_get_vpnclient_connection_health(self, resource_group):
        response = self.client.virtual_network_gateways.begin_get_vpnclient_connection_health(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_disconnect_virtual_network_gateway_vpn_connections(self, resource_group):
        response = self.client.virtual_network_gateways.begin_disconnect_virtual_network_gateway_vpn_connections(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            request={"vpnConnectionIds": ["str"]},
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_invoke_prepare_migration(self, resource_group):
        response = self.client.virtual_network_gateways.begin_invoke_prepare_migration(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            migration_params={"migrationType": "str", "resourceUrl": "str"},
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_invoke_execute_migration(self, resource_group):
        response = self.client.virtual_network_gateways.begin_invoke_execute_migration(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_invoke_commit_migration(self, resource_group):
        response = self.client.virtual_network_gateways.begin_invoke_commit_migration(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_virtual_network_gateways_begin_invoke_abort_migration(self, resource_group):
        response = self.client.virtual_network_gateways.begin_invoke_abort_migration(
            resource_group_name=resource_group.name,
            virtual_network_gateway_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...
