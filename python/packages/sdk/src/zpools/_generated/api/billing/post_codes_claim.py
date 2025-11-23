from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...models.post_codes_claim_body import PostCodesClaimBody
from ...models.post_codes_claim_response_201 import PostCodesClaimResponse201
from ...models.post_codes_claim_response_428 import PostCodesClaimResponse428
from ...types import Response


def _get_kwargs(
    *,
    body: PostCodesClaimBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/codes/claim",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | PostCodesClaimResponse201 | PostCodesClaimResponse428:
    if response.status_code == 201:
        response_201 = PostCodesClaimResponse201.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409

    if response.status_code == 410:
        response_410 = cast(Any, None)
        return response_410

    if response.status_code == 422:
        response_422 = cast(Any, None)
        return response_422

    if response.status_code == 428:
        response_428 = PostCodesClaimResponse428.from_dict(response.json())

        return response_428

    response_default = cast(Any, None)
    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | PostCodesClaimResponse201 | PostCodesClaimResponse428]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PostCodesClaimBody,
) -> Response[Any | PostCodesClaimResponse201 | PostCodesClaimResponse428]:
    """Redeem credit code

     Apply a promotional or gift credit code to account.

    Args:
        body (PostCodesClaimBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostCodesClaimResponse201 | PostCodesClaimResponse428]
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
    body: PostCodesClaimBody,
) -> Any | PostCodesClaimResponse201 | PostCodesClaimResponse428 | None:
    """Redeem credit code

     Apply a promotional or gift credit code to account.

    Args:
        body (PostCodesClaimBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostCodesClaimResponse201 | PostCodesClaimResponse428
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PostCodesClaimBody,
) -> Response[Any | PostCodesClaimResponse201 | PostCodesClaimResponse428]:
    """Redeem credit code

     Apply a promotional or gift credit code to account.

    Args:
        body (PostCodesClaimBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostCodesClaimResponse201 | PostCodesClaimResponse428]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PostCodesClaimBody,
) -> Any | PostCodesClaimResponse201 | PostCodesClaimResponse428 | None:
    """Redeem credit code

     Apply a promotional or gift credit code to account.

    Args:
        body (PostCodesClaimBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostCodesClaimResponse201 | PostCodesClaimResponse428
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
