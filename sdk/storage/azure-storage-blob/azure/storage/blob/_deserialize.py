# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING
from urllib.parse import unquote
from xml.etree.ElementTree import Element

from ._models import (
    BlobAnalyticsLogging,
    BlobProperties,
    BlobType,
    ContainerProperties,
    ContentSettings,
    CopyProperties,
    CorsRule,
    ImmutabilityPolicy,
    LeaseProperties,
    Metrics,
    ObjectReplicationPolicy,
    ObjectReplicationRule,
    RetentionPolicy,
    StaticWebsite
)
from ._shared.models import get_enum_value
from ._shared.response_handlers import deserialize_metadata

if TYPE_CHECKING:
    from azure.core.pipeline import PipelineResponse
    from ._generated.models import (
        BlobItemInternal,
        BlobTags,
        PageList,
        StorageServiceProperties,
        StorageServiceStats,
    )
    from ._shared.models import LocationMode

def deserialize_pipeline_response_into_cls(cls_method, response: "PipelineResponse", obj: Any, headers: Dict[str, Any]):
    try:
        deserialized_response = response.http_response
    except AttributeError:
        deserialized_response = response
    return cls_method(deserialized_response, obj, headers)


def deserialize_blob_properties(response: "PipelineResponse", obj: Any, headers: Dict[str, Any]) -> BlobProperties:
    blob_properties = BlobProperties(
        metadata=deserialize_metadata(response, obj, headers),
        object_replication_source_properties=deserialize_ors_policies(response.http_response.headers),
        **headers
    )
    if 'Content-Range' in headers:
        if 'x-ms-blob-content-md5' in headers:
            blob_properties.content_settings.content_md5 = headers['x-ms-blob-content-md5']
        else:
            blob_properties.content_settings.content_md5 = None
    return blob_properties


def deserialize_ors_policies(policy_dictionary: Optional[Dict[str, str]]) -> Optional[List[ObjectReplicationPolicy]]:

    if policy_dictionary is None:
        return None
    # For source blobs (blobs that have policy ids and rule ids applied to them),
    # the header will be formatted as "x-ms-or-<policy_id>_<rule_id>: {Complete, Failed}".
    # The value of this header is the status of the replication.
    or_policy_status_headers = {key: val for key, val in policy_dictionary.items()
                                if 'or-' in key and key != 'x-ms-or-policy-id'}

    parsed_result: Dict[str, List[ObjectReplicationRule]] = {}

    for key, val in or_policy_status_headers.items():
        # list blobs gives or-policy_rule and get blob properties gives x-ms-or-policy_rule
        policy_and_rule_ids = key.split('or-')[1].split('_')
        policy_id = policy_and_rule_ids[0]
        rule_id = policy_and_rule_ids[1]

        # If we are seeing this policy for the first time, create a new list to store rule_id -> result
        parsed_result[policy_id] = parsed_result.get(policy_id) or []
        parsed_result[policy_id].append(ObjectReplicationRule(rule_id=rule_id, status=val))

    result_list = [ObjectReplicationPolicy(policy_id=k, rules=v) for k, v in parsed_result.items()]

    return result_list


def deserialize_blob_stream(
    response: "PipelineResponse",
    obj: Any,
    headers: Dict[str, Any]
) -> Tuple["LocationMode", Any]:
    blob_properties = deserialize_blob_properties(response, obj, headers)
    obj.properties = blob_properties
    return response.http_response.location_mode, obj


def deserialize_container_properties(
    response: "PipelineResponse",
    obj: Any,
    headers: Dict[str, Any]
) -> ContainerProperties:
    metadata = deserialize_metadata(response, obj, headers)
    container_properties = ContainerProperties(
        metadata=metadata,
        **headers
    )
    return container_properties


def get_page_ranges_result(ranges: "PageList") -> Tuple[List[Dict[str, int]], List[Dict[str, int]]]:
    page_range = []
    clear_range = []
    if ranges.page_range:
        page_range = [{'start': b.start, 'end': b.end} for b in ranges.page_range]
    if ranges.clear_range:
        clear_range = [{'start': b.start, 'end': b.end} for b in ranges.clear_range]
    return page_range, clear_range


def service_stats_deserialize(generated: "StorageServiceStats") -> Dict[str, Any]:
    status = None
    last_sync_time = None
    if generated.geo_replication is not None:
        status = generated.geo_replication.status
        last_sync_time = generated.geo_replication.last_sync_time
    return {
        'geo_replication': {
            'status': status,
            'last_sync_time': last_sync_time
        }
    }

def service_properties_deserialize(generated: "StorageServiceProperties") -> Dict[str, Any]:
    cors_list = None
    if generated.cors is not None:
        cors_list = [CorsRule._from_generated(cors) for cors in generated.cors]  # pylint: disable=protected-access
    return {
        'analytics_logging': BlobAnalyticsLogging._from_generated(generated.logging),  # pylint: disable=protected-access
        'hour_metrics': Metrics._from_generated(generated.hour_metrics),  # pylint: disable=protected-access
        'minute_metrics': Metrics._from_generated(generated.minute_metrics),  # pylint: disable=protected-access
        'cors': cors_list,
        'target_version': generated.default_service_version,
        'delete_retention_policy': RetentionPolicy._from_generated(generated.delete_retention_policy),  # pylint: disable=protected-access
        'static_website': StaticWebsite._from_generated(generated.static_website),  # pylint: disable=protected-access
    }


def get_blob_properties_from_generated_code(generated: "BlobItemInternal") -> BlobProperties:
    blob = BlobProperties()
    if generated.name.encoded and generated.name.content is not None:
        blob.name = unquote(generated.name.content)
    else:
        blob.name = generated.name.content  #type: ignore
    blob_type = get_enum_value(generated.properties.blob_type)
    blob.blob_type = BlobType(blob_type)
    blob.etag = generated.properties.etag
    blob.deleted = generated.deleted
    blob.snapshot = generated.snapshot
    blob.is_append_blob_sealed = generated.properties.is_sealed
    blob.metadata = generated.metadata.additional_properties if generated.metadata else {}  # type: ignore [assignment]
    blob.encrypted_metadata = generated.metadata.encrypted if generated.metadata else None
    blob.lease = LeaseProperties._from_generated(generated)  # pylint: disable=protected-access
    blob.copy = CopyProperties._from_generated(generated)  # pylint: disable=protected-access
    blob.last_modified = generated.properties.last_modified
    blob.creation_time = generated.properties.creation_time  # type: ignore [assignment]
    blob.content_settings = ContentSettings._from_generated(generated)  # pylint: disable=protected-access
    blob.size = generated.properties.content_length  # type: ignore [assignment]
    blob.page_blob_sequence_number = generated.properties.blob_sequence_number
    blob.server_encrypted = generated.properties.server_encrypted  # type: ignore [assignment]
    blob.encryption_scope = generated.properties.encryption_scope
    blob.deleted_time = generated.properties.deleted_time
    blob.remaining_retention_days = generated.properties.remaining_retention_days
    blob.blob_tier = generated.properties.access_tier  # type: ignore [assignment]
    blob.rehydrate_priority = generated.properties.rehydrate_priority
    blob.blob_tier_inferred = generated.properties.access_tier_inferred
    blob.archive_status = generated.properties.archive_status
    blob.blob_tier_change_time = generated.properties.access_tier_change_time
    blob.version_id = generated.version_id
    blob.is_current_version = generated.is_current_version
    blob.tag_count = generated.properties.tag_count
    blob.tags = parse_tags(generated.blob_tags)
    blob.object_replication_source_properties = deserialize_ors_policies(generated.object_replication_metadata)
    blob.last_accessed_on = generated.properties.last_accessed_on
    blob.immutability_policy = ImmutabilityPolicy._from_generated(generated)  # pylint: disable=protected-access
    blob.has_legal_hold = generated.properties.legal_hold
    blob.has_versions_only = generated.has_versions_only
    return blob

def parse_tags(generated_tags: Optional["BlobTags"]) -> Optional[Dict[str, str]]:
    """Deserialize a list of BlobTag objects into a dict.

    :param Optional[BlobTags] generated_tags:
        A list containing the BlobTag objects from generated code.
    :return: A dictionary of the BlobTag objects.
    :rtype: Optional[Dict[str, str]]
    """
    if generated_tags:
        tag_dict = {t.key: t.value for t in generated_tags.blob_tag_set}
        return tag_dict
    return None


def load_single_xml_node(element: Element, name: str) -> Optional[Element]:
    return element.find(name)


def load_many_xml_nodes(
    element: Element,
    name: str,
    wrapper: Optional[str] = None
) -> List[Optional[Element]]:
    found_element: Optional[Element] = element
    if wrapper:
        found_element = load_single_xml_node(element, wrapper)
    if found_element is None:
        return []
    return list(found_element.findall(name))


def load_xml_string(element: Element, name: str) -> Optional[str]:
    node = element.find(name)
    if node is None or not node.text:
        return None
    return node.text


def load_xml_int(element: Element, name: str) -> Optional[int]:
    node = element.find(name)
    if node is None or not node.text:
        return None
    return int(node.text)
