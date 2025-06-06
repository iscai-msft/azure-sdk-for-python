# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from collections.abc import MutableMapping
from io import IOBase
from typing import Any, Callable, Dict, IO, Optional, TypeVar, Union, overload

from azure.core import AsyncPipelineClient
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.rest import AsyncHttpResponse, HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._utils.serialization import Deserializer, Serializer
from ...operations._vault_certificates_operations import build_create_request
from .._configuration import RecoveryServicesClientConfiguration

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class VaultCertificatesOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.recoveryservices.aio.RecoveryServicesClient`'s
        :attr:`vault_certificates` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client: AsyncPipelineClient = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config: RecoveryServicesClientConfiguration = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize: Serializer = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize: Deserializer = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @overload
    async def create(
        self,
        resource_group_name: str,
        vault_name: str,
        certificate_name: str,
        certificate_request: _models.CertificateRequest,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.VaultCertificateResponse:
        """Uploads a certificate for a resource.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param vault_name: The name of the recovery services vault. Required.
        :type vault_name: str
        :param certificate_name: Certificate friendly name. Required.
        :type certificate_name: str
        :param certificate_request: Input parameters for uploading the vault certificate. Required.
        :type certificate_request: ~azure.mgmt.recoveryservices.models.CertificateRequest
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: VaultCertificateResponse or the result of cls(response)
        :rtype: ~azure.mgmt.recoveryservices.models.VaultCertificateResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def create(
        self,
        resource_group_name: str,
        vault_name: str,
        certificate_name: str,
        certificate_request: IO[bytes],
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.VaultCertificateResponse:
        """Uploads a certificate for a resource.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param vault_name: The name of the recovery services vault. Required.
        :type vault_name: str
        :param certificate_name: Certificate friendly name. Required.
        :type certificate_name: str
        :param certificate_request: Input parameters for uploading the vault certificate. Required.
        :type certificate_request: IO[bytes]
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: VaultCertificateResponse or the result of cls(response)
        :rtype: ~azure.mgmt.recoveryservices.models.VaultCertificateResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def create(
        self,
        resource_group_name: str,
        vault_name: str,
        certificate_name: str,
        certificate_request: Union[_models.CertificateRequest, IO[bytes]],
        **kwargs: Any
    ) -> _models.VaultCertificateResponse:
        """Uploads a certificate for a resource.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param vault_name: The name of the recovery services vault. Required.
        :type vault_name: str
        :param certificate_name: Certificate friendly name. Required.
        :type certificate_name: str
        :param certificate_request: Input parameters for uploading the vault certificate. Is either a
         CertificateRequest type or a IO[bytes] type. Required.
        :type certificate_request: ~azure.mgmt.recoveryservices.models.CertificateRequest or IO[bytes]
        :return: VaultCertificateResponse or the result of cls(response)
        :rtype: ~azure.mgmt.recoveryservices.models.VaultCertificateResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.VaultCertificateResponse] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(certificate_request, (IOBase, bytes)):
            _content = certificate_request
        else:
            _json = self._serialize.body(certificate_request, "CertificateRequest")

        _request = build_create_request(
            resource_group_name=resource_group_name,
            vault_name=vault_name,
            certificate_name=certificate_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("VaultCertificateResponse", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore
