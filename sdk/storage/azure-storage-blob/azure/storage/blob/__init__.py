# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# pylint: disable=docstring-keyword-should-match-keyword-only

import os

from typing import Any, AnyStr, cast, Dict, IO, Iterable, Optional, Union, TYPE_CHECKING
from ._version import VERSION
from ._blob_client import BlobClient
from ._container_client import ContainerClient
from ._blob_service_client import BlobServiceClient
from ._lease import BlobLeaseClient
from ._download import StorageStreamDownloader
from ._quick_query_helper import BlobQueryReader
from ._shared_access_signature import generate_account_sas, generate_container_sas, generate_blob_sas
from ._shared.policies import ExponentialRetry, LinearRetry
from ._shared.response_handlers import PartialBatchErrorException
from ._shared.models import (
    LocationMode,
    ResourceTypes,
    AccountSasPermissions,
    StorageErrorCode,
    UserDelegationKey,
    Services
)
from ._generated.models import RehydratePriority
from ._models import (
    BlobType,
    BlockState,
    StandardBlobTier,
    PremiumPageBlobTier,
    BlobImmutabilityPolicyMode,
    SequenceNumberAction,
    PublicAccess,
    BlobAnalyticsLogging,
    Metrics,
    RetentionPolicy,
    StaticWebsite,
    CorsRule,
    ContainerProperties,
    BlobProperties,
    FilteredBlob,
    LeaseProperties,
    ContentSettings,
    CopyProperties,
    BlobBlock,
    PageRange,
    AccessPolicy,
    ContainerSasPermissions,
    BlobSasPermissions,
    CustomerProvidedEncryptionKey,
    ContainerEncryptionScope,
    BlobQueryError,
    DelimitedJsonDialect,
    DelimitedTextDialect,
    QuickQueryDialect,
    ArrowDialect,
    ArrowType,
    ObjectReplicationPolicy,
    ObjectReplicationRule,
    ImmutabilityPolicy,
)
from ._list_blobs_helper import BlobPrefix

if TYPE_CHECKING:
    from azure.core.credentials import AzureNamedKeyCredential, AzureSasCredential, TokenCredential

__version__ = VERSION


def upload_blob_to_url(
    blob_url: str,
    data: Union[Iterable[AnyStr], IO[AnyStr]],
    credential: Optional[Union[str, Dict[str, str], "AzureNamedKeyCredential", "AzureSasCredential", "TokenCredential"]] = None,  # pylint: disable=line-too-long
    **kwargs: Any
) -> Dict[str, Any]:
    """Upload data to a given URL

    The data will be uploaded as a block blob.

    :param str blob_url:
        The full URI to the blob. This can also include a SAS token.
    :param data:
        The data to upload. This can be bytes, text, an iterable or a file-like object.
    :type data: bytes or str or Iterable
    :param credential:
        The credentials with which to authenticate. This is optional if the
        blob URL already has a SAS token. The value can be a SAS token string,
        an instance of a AzureSasCredential or AzureNamedKeyCredential from azure.core.credentials,
        an account shared access key, or an instance of a TokenCredentials class from azure.identity.
        If the resource URI already contains a SAS token, this will be ignored in favor of an explicit credential
        - except in the case of AzureSasCredential, where the conflicting SAS tokens will raise a ValueError.
        If using an instance of AzureNamedKeyCredential, "name" should be the storage account name, and "key"
        should be the storage account key.
    :type credential:
        ~azure.core.credentials.AzureNamedKeyCredential or
        ~azure.core.credentials.AzureSasCredential or
        ~azure.core.credentials.TokenCredential or
        str or dict[str, str] or None
    :keyword bool overwrite:
        Whether the blob to be uploaded should overwrite the current data.
        If True, upload_blob_to_url will overwrite any existing data. If set to False, the
        operation will fail with a ResourceExistsError.
    :keyword int max_concurrency:
        The number of parallel connections with which to download.
    :keyword int length:
        Number of bytes to read from the stream. This is optional, but
        should be supplied for optimal performance.
    :keyword dict(str,str) metadata:
        Name-value pairs associated with the blob as metadata.
    :keyword bool validate_content:
        If true, calculates an MD5 hash for each chunk of the blob. The storage
        service checks the hash of the content that has arrived with the hash
        that was sent. This is primarily valuable for detecting bitflips on
        the wire if using http instead of https as https (the default) will
        already validate. Note that this MD5 hash is not stored with the
        blob. Also note that if enabled, the memory-efficient upload algorithm
        will not be used, because computing the MD5 hash requires buffering
        entire blocks, and doing so defeats the purpose of the memory-efficient algorithm.
    :keyword str encoding:
        Encoding to use if text is supplied as input. Defaults to UTF-8.
    :return: Blob-updated property dict (Etag and last modified)
    :rtype: dict(str, Any)
    """
    with BlobClient.from_blob_url(blob_url, credential=credential) as client:
        return cast(BlobClient, client).upload_blob(data=data, blob_type=BlobType.BLOCKBLOB, **kwargs)


def _download_to_stream(client: BlobClient, handle: IO[bytes], **kwargs: Any) -> None:
    """
    Download data to specified open file-handle.

    :param BlobClient client: The BlobClient to download with.
    :param Stream handle: A Stream to download the data into.
    """
    stream = client.download_blob(**kwargs)
    stream.readinto(handle)


def download_blob_from_url(
    blob_url: str,
    output: Union[str, IO[bytes]],
    credential: Optional[Union[str, Dict[str, str], "AzureNamedKeyCredential", "AzureSasCredential", "TokenCredential"]] = None,  # pylint: disable=line-too-long
    **kwargs: Any
) -> None:
    """Download the contents of a blob to a local file or stream.

    :param str blob_url:
        The full URI to the blob. This can also include a SAS token.
    :param output:
        Where the data should be downloaded to. This could be either a file path to write to,
        or an open IO handle to write to.
    :type output: str or IO.
    :param credential:
        The credentials with which to authenticate. This is optional if the
        blob URL already has a SAS token or the blob is public. The value can be a SAS token string,
        an instance of a AzureSasCredential or AzureNamedKeyCredential from azure.core.credentials,
        an account shared access key, or an instance of a TokenCredentials class from azure.identity.
        If the resource URI already contains a SAS token, this will be ignored in favor of an explicit credential
        - except in the case of AzureSasCredential, where the conflicting SAS tokens will raise a ValueError.
        If using an instance of AzureNamedKeyCredential, "name" should be the storage account name, and "key"
        should be the storage account key.
    :type credential:
        ~azure.core.credentials.AzureNamedKeyCredential or
        ~azure.core.credentials.AzureSasCredential or
        ~azure.core.credentials.TokenCredential or
        str or dict[str, str] or None
    :keyword bool overwrite:
        Whether the local file should be overwritten if it already exists. The default value is
        `False` - in which case a ValueError will be raised if the file already exists. If set to
        `True`, an attempt will be made to write to the existing file. If a stream handle is passed
        in, this value is ignored.
    :keyword int max_concurrency:
        The number of parallel connections with which to download.
    :keyword int offset:
        Start of byte range to use for downloading a section of the blob.
        Must be set if length is provided.
    :keyword int length:
        Number of bytes to read from the stream. This is optional, but
        should be supplied for optimal performance.
    :keyword bool validate_content:
        If true, calculates an MD5 hash for each chunk of the blob. The storage
        service checks the hash of the content that has arrived with the hash
        that was sent. This is primarily valuable for detecting bitflips on
        the wire if using http instead of https as https (the default) will
        already validate. Note that this MD5 hash is not stored with the
        blob. Also note that if enabled, the memory-efficient upload algorithm
        will not be used, because computing the MD5 hash requires buffering
        entire blocks, and doing so defeats the purpose of the memory-efficient algorithm.
    :return: None
    :rtype: None
    """
    overwrite = kwargs.pop('overwrite', False)
    with BlobClient.from_blob_url(blob_url, credential=credential) as client:
        if hasattr(output, 'write'):
            _download_to_stream(client, cast(IO[bytes], output), **kwargs)
        else:
            if not overwrite and os.path.isfile(output):
                raise ValueError(f"The file '{output}' already exists.")
            with open(output, 'wb') as file_handle:
                _download_to_stream(client, file_handle, **kwargs)


__all__ = [
    'upload_blob_to_url',
    'download_blob_from_url',
    'BlobServiceClient',
    'ContainerClient',
    'BlobClient',
    'BlobType',
    'BlobLeaseClient',
    'StorageErrorCode',
    'UserDelegationKey',
    'ExponentialRetry',
    'LinearRetry',
    'LocationMode',
    'BlockState',
    'StandardBlobTier',
    'PremiumPageBlobTier',
    'SequenceNumberAction',
    'BlobImmutabilityPolicyMode',
    'ImmutabilityPolicy',
    'PublicAccess',
    'BlobAnalyticsLogging',
    'Metrics',
    'RetentionPolicy',
    'StaticWebsite',
    'CorsRule',
    'ContainerProperties',
    'BlobProperties',
    'BlobPrefix',
    'FilteredBlob',
    'LeaseProperties',
    'ContentSettings',
    'CopyProperties',
    'BlobBlock',
    'PageRange',
    'AccessPolicy',
    'QuickQueryDialect',
    'ContainerSasPermissions',
    'BlobSasPermissions',
    'ResourceTypes',
    'AccountSasPermissions',
    'StorageStreamDownloader',
    'CustomerProvidedEncryptionKey',
    'RehydratePriority',
    'generate_account_sas',
    'generate_container_sas',
    'generate_blob_sas',
    'PartialBatchErrorException',
    'ContainerEncryptionScope',
    'BlobQueryError',
    'DelimitedJsonDialect',
    'DelimitedTextDialect',
    'ArrowDialect',
    'ArrowType',
    'BlobQueryReader',
    'ObjectReplicationPolicy',
    'ObjectReplicationRule',
    'Services',
]
