from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.wirepas_error_code import WirepasErrorCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_response_details import ErrorResponseDetails
    from ..models.error_response_service_ref import ErrorResponseServiceRef


T = TypeVar("T", bound="ErrorResponse")


@_attrs_define
class ErrorResponse:
    """Common error response resource sent in case of server error

    Attributes:
        error_code (WirepasErrorCode): More detailed error codes describing the reason for failures. These error codes
            are specific
            to Wirepas backend services. The main objective of the error codes is to give more information
            related to the potential cause of an failure in operation. These can be then benefit e.g. when
            giving error indications to actual end users, in internalization of error responses etc.

            The error codes are mainly related to the scenarios, where server returns HTTP error 400 (Bad
            Request) or 500 (Internal Server Error). However, an Wirepas error code might be included also in
            other errors, but the added information in these cases might be quite minimal.

            The Wirepas error codes can be categorized to following groups:
            * **Client data errors**: Error codes describing the erroneous data provided by the client
            * **Client request errors**: Other client request related error codes
            * **System error codes**: Error codes giving some background on potential system level problems

            In some of the cases, the details field may contain more information about the error. The details
            field is encoded in JSON format. The contents do not have standard format, thus parsing it is not
            recommended. Instead, it is purposed mainly for development time and debug purposes for providing
            more insights to the actual cause of the error.

            The actual error codes are listed below per category.

            **Client data errors**:
            * `WERR_UNKNOWN_RESOURCE`: Identified request object(s) are not found from the system. Details field
              in the response may identify the unknown resources.
            * `WERR_UNKNOWN_FIELD`: Request object(s) contain unknown fields. Details field in the response may
              identify the unknown resources.
            * `WERR_INVALID_FIELD_VALUE`: Values of field(s) in the request is not acceptable. Details may contain
              information identifying the resources and fields involved.
            * `WERR_INVALID_IDENTIFIER`: The value given for the identifier field in an object is invalid. This does not
              refer to the UUID of the object but the real world identifiers (such as network or node addresses). Details
              field may contain additional information about the error.
            * `WERR_DUPLICATE_IDENTIFIER`: The identifier for an object is already allocated and therefore does not meet
              the unique constraint. This does not refer to the UUID of the object but the real world identifiers (such
              as network and node addresses). Details field may contain additional information about the error.
            * `WERR_INVALID_REFERENCE`: The reference object identifier given in the request is invalid or cannot be
              found. Details may contain more information about erroneous objects and references.
            * `WERR_RESOURCE_IN_USE`: The resource being deleted is in use or referenced by another object so that it
              cannot be deleted before it is freed or references removed.

            **Client request errors**:
            * `WERR_API_VALIDATION`: The request does not meet the requirements and constraints defined by the API
              specification. Typical causes are e.g. malformed content, missing required fields, incorrect types or enum
              fields, or illegal values not meeting the given (e.g. min/max) constraints.
            * `WERR_INVALID_CREDENTIALS`: The credentials provided with the client request are not available or invalid.
            * `WERR_ACCESS_NOT_ALLOWED_OPERATION`: The client does not have enough rights to perform the requested
            operation.
            * `WERR_ACCESS_NOT_ALLOWED_DATA`: The client does not have rights to access the requested resource.
            * `WERR_INVALID_PARAMETERS`: The URL parameters given for the request are invalid. The details may contain
              a list of invalid parameters (InvalidParams).
            * `WERR_INVALID_HEADERS`: The header fields in request are invalid, contain invalid values, etc. The details
              may contain a list of invalid parameters (InvalidParams).
            * `WERR_INVALID_CONTENT`: The content body of the request has invalid format / encoding.
            * `WERR_CONTENT_TOO_LARGE`: The provided content body is too large for the service to handle.
            * `WERR_MISSING_CONTENT`: The content is missing for a request that expects to have content.
            * `WERR_INVALID_QUERY`: The query filter given as a parameter for GET or advanced search request has invalid
              syntax or contain invalid fields. Details may contain a list of invalid fields (errorFields).
            * `WERR_INVALID_QUERY_PARAMETERS`: Some of the other parameters for the search query (limit, sortBy, order,
              or cursor) is incorrect or mismatches against other fields (e.g. cursor not matching the current parameters).
            * `WERR_INVALID_STATE`: The requested state change operation of an object is not allowed given the current
              state of the target resource.
            * `WERR_STATE_CHANGE_NOT_ALLOWED`: The requested state change operation was not allowed (see message for further
            details).
            * `WERR_FAILED_RESOURCES`: The requested operation failed because there are or were failed resources or
            operations that
              need to be managed before continuing.
            * `WERR_OVERLAPPING_OPERATION`: The requested operation failed, since there is an overlapping operation
            preventing the
              requested operation.
            * `WERR_PRECONDITION_ERROR`: The requested operation failed because needed preconditions were not met.
              The error cannot be bypassed with the force flag, instead the fulfilling of the preconditions must be waited
            on.
            * `WERR_PRECONDITION_VALIDATION`: The requested operation failed because needed preconditions were not met,
              but the error can be bypassed using the force flag.

            **System error codes**:
            * `WERR_DATABASE_ERROR`: The requested operation failed due to a database connection or request failure. See
              more details on the backend system logs.
            * `WERR_MESSAGING_ERROR`: The requested operation failed due to an internal messaging error at the backend. See
              more details on the backend system logs.
            * `WERR_OPERATION_TIMEOUT`: The requested operation failed due to an internal operation timeout. See more
              details on the backend system logs.
            * `WERR_GENERAL_ERROR`: The requested operation failed due to an unknown internal error at the backend. See
              more details on the backend system logs.
        message (str): Short descriptive error message in English
        service_ref (ErrorResponseServiceRef): Error reference identifier, which makes it possible locate related error
            message from server side logs.
            This is mainly purposed for development time use, but can be benefit also when tracking production system
            problems.
        details (ErrorResponseDetails | Unset):
    """

    error_code: WirepasErrorCode
    message: str
    service_ref: ErrorResponseServiceRef
    details: ErrorResponseDetails | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error_code = self.error_code.value

        message = self.message

        service_ref = self.service_ref.to_dict()

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errorCode": error_code,
                "message": message,
                "serviceRef": service_ref,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_response_details import ErrorResponseDetails
        from ..models.error_response_service_ref import ErrorResponseServiceRef

        d = dict(src_dict)
        error_code = WirepasErrorCode(d.pop("errorCode"))

        message = d.pop("message")

        service_ref = ErrorResponseServiceRef.from_dict(d.pop("serviceRef"))

        _details = d.pop("details", UNSET)
        details: ErrorResponseDetails | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = ErrorResponseDetails.from_dict(_details)

        error_response = cls(
            error_code=error_code,
            message=message,
            service_ref=service_ref,
            details=details,
        )

        error_response.additional_properties = d
        return error_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
