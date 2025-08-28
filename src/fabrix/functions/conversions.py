"""
Implements conversion and casting functions for Fabric expressions.
"""

import base64
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Any

from fabrix.registry import registry
from fabrix.utils import as_bool, as_float, as_int, as_string


@registry.register("array")
def array(value: Any) -> list[Any]:
    """
    Return an array from a single specified input.

    Parameters
    ----------
    value : Any
        Value to wrap in an array.

    Returns
    -------
    list
        A list containing the value.
    """
    return [value]


@registry.register("base64")
def base64_func(value: str) -> str:
    """
    Return the base64-encoded version for a string.

    Parameters
    ----------
    value : str
        String to encode.

    Returns
    -------
    str
        Base64-encoded string.
    """
    return base64.b64encode(str(value).encode("utf-8")).decode("utf-8")


@registry.register("base64ToBinary")
def base64_to_binary(value: str) -> bytes:
    """
    Return the binary version for a base64-encoded string.

    Parameters
    ----------
    value : str
        Base64-encoded string.

    Returns
    -------
    bytes
        Decoded binary data.
    """
    return base64.b64decode(value)


@registry.register("base64ToString")
def base64_to_string(value: str) -> str:
    """
    Return the string version for a base64-encoded string.

    Parameters
    ----------
    value : str
        Base64-encoded string.

    Returns
    -------
    str
        Decoded string.
    """
    return base64.b64decode(value).decode("utf-8")


@registry.register("binary")
def binary(value: Any) -> bytes:
    """
    Return the binary version for an input value.

    Parameters
    ----------
    value : Any
        Input value (string or bytes).

    Returns
    -------
    bytes
        The value as bytes.
    """
    if isinstance(value, bytes):
        return value
    return str(value).encode("utf-8")


@registry.register("bool")
def bool_func(value: Any) -> bool:
    """
    Return the Boolean version for an input value.

    Parameters
    ----------
    value : Any
        Input value.

    Returns
    -------
    bool
        Boolean value.
    """
    return as_bool(value)


@registry.register("coalesce")
def coalesce(*args: Any) -> Any:
    """
    Return the first non-null value from one or more parameters.

    Parameters
    ----------
    *args : Any
        Parameters to check.

    Returns
    -------
    Any
        The first non-null argument, or None if all are null.
    """
    for arg in args:
        if arg is not None:
            return arg
    return None


@registry.register("createArray")
def create_array(*args: Any) -> list[Any]:
    """
    Return an array from multiple inputs.

    Parameters
    ----------
    *args : Any
        Values to wrap in an array.

    Returns
    -------
    list
        List of all input values.
    """
    return list(args)


@registry.register("dataUri")
def data_uri(value: Any) -> str:
    """
    Return the data URI for an input value.

    Parameters
    ----------
    value : Any
        Input value.

    Returns
    -------
    str
        Data URI as a string.
    """
    # Assume text/plain and utf-8 for simplicity
    b64 = base64.b64encode(str(value).encode("utf-8")).decode("utf-8")
    return f"data:text/plain;base64,{b64}"


@registry.register("dataUriToBinary")
def data_uri_to_binary(value: str) -> bytes:
    """
    Return the binary version for a data URI.

    Parameters
    ----------
    value : str
        Data URI.

    Returns
    -------
    bytes
        Decoded binary data.
    """
    prefix = "base64,"
    if prefix not in value:
        raise ValueError("No base64 prefix found in data URI.")
    b64 = value.split(prefix, 1)[1]
    return base64.b64decode(b64)


@registry.register("dataUriToString")
def data_uri_to_string(value: str) -> str:
    """
    Return the string version for a data URI.

    Parameters
    ----------
    value : str
        Data URI.

    Returns
    -------
    str
        Decoded string.
    """
    return data_uri_to_binary(value).decode("utf-8")


@registry.register("decodeBase64")
def decode_base64(value: str) -> str:
    """
    Return the string version for a base64-encoded string.

    Parameters
    ----------
    value : str
        Base64-encoded string.

    Returns
    -------
    str
        Decoded string.
    """
    return base64.b64decode(value).decode("utf-8")


@registry.register("decodeDataUri")
def decode_data_uri(value: str) -> bytes:
    """
    Return the binary version for a data URI.

    Parameters
    ----------
    value : str
        Data URI.

    Returns
    -------
    bytes
        Decoded binary data.
    """
    return data_uri_to_binary(value)


@registry.register("decodeUriComponent")
def decode_uri_component(value: str) -> str:
    """
    Return a string that replaces escape characters with decoded versions.

    Parameters
    ----------
    value : str
        URI-encoded string.

    Returns
    -------
    str
        Decoded URI component.
    """
    return urllib.parse.unquote(str(value))


@registry.register("encodeUriComponent")
def encode_uri_component(value: str) -> str:
    """
    Return a string that replaces URL-unsafe characters with escape characters.

    Parameters
    ----------
    value : str
        The string to encode.

    Returns
    -------
    str
        URI-encoded string.
    """
    return urllib.parse.quote(str(value), safe="")


@registry.register("float")
def float_func(value: Any) -> float:
    """
    Return a floating point number for an input value.

    Parameters
    ----------
    value : Any
        Value to convert.

    Returns
    -------
    float
        Floating-point number.
    """
    return as_float(value)


@registry.register("int")
def int_func(value: Any) -> int:
    """
    Return the integer version for a string.

    Parameters
    ----------
    value : Any
        Value to convert.

    Returns
    -------
    int
        Integer value.
    """

    return as_int(value)


@registry.register("string")
def string_func(value: Any) -> str:
    """
    Return the string version for an input value.

    Parameters
    ----------
    value : Any
        Value to convert.

    Returns
    -------
    str
        String value.
    """
    return as_string(value)


@registry.register("uriComponent")
def uri_component(value: str) -> str:
    """
    Return the URI-encoded version for an input value by replacing URL-unsafe characters with escape characters.

    Parameters
    ----------
    value : str
        The string to encode.

    Returns
    -------
    str
        URI-encoded string.
    """
    return urllib.parse.quote(str(value), safe="")


@registry.register("uriComponentToBinary")
def uri_component_to_binary(value: str) -> bytes:
    """
    Return the binary version for a URI-encoded string.

    Parameters
    ----------
    value : str
        URI-encoded string.

    Returns
    -------
    bytes
        Decoded binary data.
    """
    return urllib.parse.unquote_to_bytes(str(value))


@registry.register("uriComponentToString")
def uri_component_to_string(value: str) -> str:
    """
    Return the string version for a URI-encoded string.

    Parameters
    ----------
    value : str
        URI-encoded string.

    Returns
    -------
    str
        Decoded string.
    """
    return urllib.parse.unquote(str(value))


@registry.register("xml")
def xml_func(value: str) -> ET.Element:
    """
    Return the XML version for a string.

    Parameters
    ----------
    value : str
        XML string.

    Returns
    -------
    xml.etree.ElementTree.Element
        XML Element.
    """
    return ET.fromstring(str(value))


@registry.register("xpath")
def xpath(xml_value: Any, xpath_expr: str) -> list[Any]:
    """
    Check XML for nodes or values that match an XPath expression, and return the matching nodes or values.

    Parameters
    ----------
    xml_value : Any
        XML Element or XML string.
    xpath_expr : str
        XPath expression.

    Returns
    -------
    list
        List of matching nodes or values.
    """
    # Accept ET.Element or string
    if isinstance(xml_value, str):
        elem = ET.fromstring(xml_value)
    else:
        elem = xml_value
    # Basic XPath support
    return elem.findall(xpath_expr)
