# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------
import base64
import logging
import threading
import uuid
from typing import TypeVar, Generic, Any, Callable, Optional, Tuple, List
from azure.core.exceptions import AzureError
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.common import with_current_context


PollingReturnType_co = TypeVar("PollingReturnType_co", covariant=True)
DeserializationCallbackType = Any

_LOGGER = logging.getLogger(__name__)


class PollingMethod(Generic[PollingReturnType_co]):
    """ABC class for polling method."""

    def initialize(
        self,
        client: Any,
        initial_response: Any,
        deserialization_callback: DeserializationCallbackType,
    ) -> None:
        raise NotImplementedError("This method needs to be implemented")

    def run(self) -> None:
        """Run the polling method.
        This method should be implemented to perform the actual polling logic.

        :return: None
        :rtype: None
        """
        raise NotImplementedError("This method needs to be implemented")

    def status(self) -> str:
        """Return the current status of the polling operation.

        :rtype: str
        :return: The current status of the polling operation.
        """
        raise NotImplementedError("This method needs to be implemented")

    def finished(self) -> bool:
        """Check if the polling operation is finished.

        :rtype: bool
        :return: True if the polling operation is finished, False otherwise.
        """
        raise NotImplementedError("This method needs to be implemented")

    def resource(self) -> PollingReturnType_co:
        """Return the resource built by the polling operation.

        :rtype: any
        :return: The resource built by the polling operation.
        """
        raise NotImplementedError("This method needs to be implemented")

    def get_continuation_token(self) -> str:
        """Return a continuation token that allows to restart the poller later.

        :rtype: str
        :return: An opaque continuation token.
        """
        raise TypeError("Polling method '{}' doesn't support get_continuation_token".format(self.__class__.__name__))

    @classmethod
    def from_continuation_token(
        cls, continuation_token: str, **kwargs: Any
    ) -> Tuple[Any, Any, DeserializationCallbackType]:
        """Recreate the poller from a continuation token.

        :param continuation_token: The continuation token to recreate the poller from.
        :type continuation_token: str
        :rtype: Tuple[Any, Any, DeserializationCallbackType]
        :return: A tuple containing the client, initial response, and deserialization callback.
        """
        raise TypeError("Polling method '{}' doesn't support from_continuation_token".format(cls.__name__))


class _SansIONoPolling(Generic[PollingReturnType_co]):
    _deserialization_callback: Callable[[Any], PollingReturnType_co]
    """Deserialization callback passed during initialization"""

    def __init__(self):
        self._initial_response = None

    def initialize(
        self,
        _: Any,
        initial_response: Any,
        deserialization_callback: Callable[[Any], PollingReturnType_co],
    ) -> None:
        """Initialize the poller with the initial response and deserialization callback.

        :param _: The client, not used in this polling method.
        :type _: Any
        :param initial_response: The initial response from the long-running operation.
        :type initial_response: Any
        :param deserialization_callback: A callback that takes a response and returns a deserialized object.
        :type deserialization_callback: Callable[[Any], PollingReturnType_co]
        :return: None
        :rtype: None
        """
        self._initial_response = initial_response
        self._deserialization_callback = deserialization_callback

    def status(self) -> str:
        """Return the current status.

        :rtype: str
        :return: The current status
        """
        return "succeeded"

    def finished(self) -> bool:
        """Is this polling finished?

        :rtype: bool
        :return: Whether this polling is finished
        """
        return True

    def resource(self) -> PollingReturnType_co:
        """Return the built resource.

        :rtype: any
        :return: The built resource.
        """
        return self._deserialization_callback(self._initial_response)

    def get_continuation_token(self) -> str:
        """Return a continuation token that allows to restart the poller later.

        :rtype: str
        :return: An opaque continuation token
        """
        import pickle

        return base64.b64encode(pickle.dumps(self._initial_response)).decode("ascii")

    @classmethod
    def from_continuation_token(
        cls, continuation_token: str, **kwargs: Any
    ) -> Tuple[Any, Any, Callable[[Any], PollingReturnType_co]]:
        """Recreate the poller from a continuation token.

        :param continuation_token: The continuation token to recreate the poller from.
        :type continuation_token: str
        :rtype: Tuple[Any, Any, Callable[[Any], PollingReturnType_co]]
        :return: A tuple containing the client, initial response, and deserialization callback.
        :raises ValueError: If 'deserialization_callback' is not provided in kwargs.
        """
        try:
            deserialization_callback = kwargs["deserialization_callback"]
        except KeyError:
            raise ValueError("Need kwarg 'deserialization_callback' to be recreated from continuation_token") from None
        import pickle

        initial_response = pickle.loads(base64.b64decode(continuation_token))  # nosec
        return None, initial_response, deserialization_callback


class NoPolling(_SansIONoPolling[PollingReturnType_co], PollingMethod[PollingReturnType_co]):
    """An empty poller that returns the deserialized initial response."""

    def run(self) -> None:
        """Empty run, no polling."""


class LROPoller(Generic[PollingReturnType_co]):
    """Poller for long running operations.

    :param client: A pipeline service client
    :type client: ~azure.core.PipelineClient
    :param initial_response: The initial call response
    :type initial_response: ~azure.core.pipeline.PipelineResponse
    :param deserialization_callback: A callback that takes a Response and return a deserialized object.
                                     If a subclass of Model is given, this passes "deserialize" as callback.
    :type deserialization_callback: callable or msrest.serialization.Model
    :param polling_method: The polling strategy to adopt
    :type polling_method: ~azure.core.polling.PollingMethod
    """

    def __init__(
        self,
        client: Any,
        initial_response: Any,
        deserialization_callback: Callable[[Any], PollingReturnType_co],
        polling_method: PollingMethod[PollingReturnType_co],
    ) -> None:
        self._callbacks: List[Callable] = []
        self._polling_method = polling_method

        # This implicit test avoids bringing in an explicit dependency on Model directly
        try:
            deserialization_callback = deserialization_callback.deserialize  # type: ignore
        except AttributeError:
            pass

        # Might raise a CloudError
        self._polling_method.initialize(client, initial_response, deserialization_callback)

        # Prepare thread execution
        self._thread = None
        self._done = threading.Event()
        self._exception = None
        if self._polling_method.finished():
            self._done.set()
        else:
            self._thread = threading.Thread(
                target=with_current_context(self._start),
                name="LROPoller({})".format(uuid.uuid4()),
            )
            self._thread.daemon = True
            self._thread.start()

    def _start(self):
        """Start the long running operation.
        On completion, runs any callbacks.
        """
        try:
            self._polling_method.run()
        except AzureError as error:
            if not error.continuation_token:
                try:
                    error.continuation_token = self.continuation_token()
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.warning("Unable to retrieve continuation token.")
                    error.continuation_token = None

            self._exception = error
        except Exception as error:  # pylint: disable=broad-except
            self._exception = error

        finally:
            self._done.set()

        callbacks, self._callbacks = self._callbacks, []
        while callbacks:
            for call in callbacks:
                call(self._polling_method)
            callbacks, self._callbacks = self._callbacks, []

    def polling_method(self) -> PollingMethod[PollingReturnType_co]:
        """Return the polling method associated to this poller.

        :return: The polling method
        :rtype: ~azure.core.polling.PollingMethod
        """
        return self._polling_method

    def continuation_token(self) -> str:
        """Return a continuation token that allows to restart the poller later.

        :returns: An opaque continuation token
        :rtype: str
        """
        return self._polling_method.get_continuation_token()

    @classmethod
    def from_continuation_token(
        cls, polling_method: PollingMethod[PollingReturnType_co], continuation_token: str, **kwargs: Any
    ) -> "LROPoller[PollingReturnType_co]":
        """Create a poller from a continuation token.

        :param polling_method: The polling strategy to adopt
        :type polling_method: ~azure.core.polling.PollingMethod
        :param continuation_token: An opaque continuation token
        :type continuation_token: str
        :return: An instance of LROPoller
        :rtype: ~azure.core.polling.LROPoller
        :raises ~azure.core.exceptions.HttpResponseError: If the continuation token is invalid.
        """
        (
            client,
            initial_response,
            deserialization_callback,
        ) = polling_method.from_continuation_token(continuation_token, **kwargs)
        return cls(client, initial_response, deserialization_callback, polling_method)

    def status(self) -> str:
        """Returns the current status string.

        :returns: The current status string
        :rtype: str
        """
        return self._polling_method.status()

    def result(self, timeout: Optional[float] = None) -> PollingReturnType_co:
        """Return the result of the long running operation, or
        the result available after the specified timeout.

        :param float timeout: Period of time to wait before getting back control.
        :returns: The deserialized resource of the long running operation, if one is available.
        :rtype: any or None
        :raises ~azure.core.exceptions.HttpResponseError: Server problem with the query.
        """
        self.wait(timeout)
        return self._polling_method.resource()

    @distributed_trace
    def wait(self, timeout: Optional[float] = None) -> None:
        """Wait on the long running operation for a specified length
        of time. You can check if this call as ended with timeout with the
        "done()" method.

        :param float timeout: Period of time to wait for the long running
         operation to complete (in seconds).
        :raises ~azure.core.exceptions.HttpResponseError: Server problem with the query.
        """
        if self._thread is None:
            return
        self._thread.join(timeout=timeout)
        try:
            # Let's handle possible None in forgiveness here
            # https://github.com/python/mypy/issues/8165
            raise self._exception  # type: ignore
        except TypeError:  # Was None
            pass

    def done(self) -> bool:
        """Check status of the long running operation.

        :returns: 'True' if the process has completed, else 'False'.
        :rtype: bool
        """
        return self._thread is None or not self._thread.is_alive()

    def add_done_callback(self, func: Callable) -> None:
        """Add callback function to be run once the long running operation
        has completed - regardless of the status of the operation.

        :param callable func: Callback function that takes at least one
         argument, a completed LongRunningOperation.
        """
        # Still use "_done" and not "done", since CBs are executed inside the thread.
        if self._done.is_set():
            func(self._polling_method)
        # Let's add them still, for consistency (if you wish to access to it for some reasons)
        self._callbacks.append(func)

    def remove_done_callback(self, func: Callable) -> None:
        """Remove a callback from the long running operation.

        :param callable func: The function to be removed from the callbacks.
        :raises ValueError: if the long running operation has already completed.
        """
        if self._done is None or self._done.is_set():
            raise ValueError("Process is complete.")
        self._callbacks = [c for c in self._callbacks if c != func]
