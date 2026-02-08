from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...models.post_sshkey_body import PostSshkeyBody
from ...models.post_sshkey_response_201 import PostSshkeyResponse201
from ...models.post_sshkey_response_409 import PostSshkeyResponse409
from ...types import Response


def _get_kwargs(
    *,
    body: PostSshkeyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sshkey",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | PostSshkeyResponse201 | PostSshkeyResponse409:
    if response.status_code == 201:
        response_201 = PostSshkeyResponse201.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 409:
        response_409 = PostSshkeyResponse409.from_dict(response.json())

        return response_409

    response_default = cast(Any, None)
    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | PostSshkeyResponse201 | PostSshkeyResponse409]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PostSshkeyBody,
) -> Response[Any | PostSshkeyResponse201 | PostSshkeyResponse409]:
    """Register SSH public key

     Add a new SSH public key for the authenticated user to enable SSH access to zpools.

    Args:
        body (PostSshkeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostSshkeyResponse201 | PostSshkeyResponse409]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: PostSshkeyBody,
) -> Any | PostSshkeyResponse201 | PostSshkeyResponse409 | None:
    """Register SSH public key

     Add a new SSH public key for the authenticated user to enable SSH access to zpools.

    Args:
        body (PostSshkeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostSshkeyResponse201 | PostSshkeyResponse409
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PostSshkeyBody,
) -> Response[Any | PostSshkeyResponse201 | PostSshkeyResponse409]:
    """Register SSH public key

     Add a new SSH public key for the authenticated user to enable SSH access to zpools.

    Args:
        body (PostSshkeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostSshkeyResponse201 | PostSshkeyResponse409]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PostSshkeyBody,
) -> Any | PostSshkeyResponse201 | PostSshkeyResponse409 | None:
    """Register SSH public key

     Add a new SSH public key for the authenticated user to enable SSH access to zpools.

    Args:
        body (PostSshkeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostSshkeyResponse201 | PostSshkeyResponse409
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
