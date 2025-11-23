from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...models.post_zpool_zpool_id_scrub_response_202 import PostZpoolZpoolIdScrubResponse202
from ...types import Response


def _get_kwargs(
    zpool_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/zpool/{zpool_id}/scrub",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | PostZpoolZpoolIdScrubResponse202:
    if response.status_code == 202:
        response_202 = PostZpoolZpoolIdScrubResponse202.from_dict(response.json())

        return response_202

    response_default = cast(Any, None)
    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | PostZpoolZpoolIdScrubResponse202]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    zpool_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | PostZpoolZpoolIdScrubResponse202]:
    """Start zpool scrub

     Initiate a data integrity scrub on the specified zpool.

    Args:
        zpool_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostZpoolZpoolIdScrubResponse202]
    """

    kwargs = _get_kwargs(
        zpool_id=zpool_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    zpool_id: str,
    *,
    client: AuthenticatedClient,
) -> Any | PostZpoolZpoolIdScrubResponse202 | None:
    """Start zpool scrub

     Initiate a data integrity scrub on the specified zpool.

    Args:
        zpool_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostZpoolZpoolIdScrubResponse202
    """

    return sync_detailed(
        zpool_id=zpool_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    zpool_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | PostZpoolZpoolIdScrubResponse202]:
    """Start zpool scrub

     Initiate a data integrity scrub on the specified zpool.

    Args:
        zpool_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostZpoolZpoolIdScrubResponse202]
    """

    kwargs = _get_kwargs(
        zpool_id=zpool_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    zpool_id: str,
    *,
    client: AuthenticatedClient,
) -> Any | PostZpoolZpoolIdScrubResponse202 | None:
    """Start zpool scrub

     Initiate a data integrity scrub on the specified zpool.

    Args:
        zpool_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostZpoolZpoolIdScrubResponse202
    """

    return (
        await asyncio_detailed(
            zpool_id=zpool_id,
            client=client,
        )
    ).parsed
