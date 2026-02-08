from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.post_zpool_zpool_id_modify_body import PostZpoolZpoolIdModifyBody
from ...types import Response


def _get_kwargs(
    zpool_id: str,
    *,
    body: PostZpoolZpoolIdModifyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/zpool/{zpool_id}/modify",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any:
    if response.status_code == 202:
        return None

    if response.status_code == 400:
        return None

    if response.status_code == 404:
        return None

    if response.status_code == 409:
        return None

    return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
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
    body: PostZpoolZpoolIdModifyBody,
) -> Response[Any]:
    """Modify zpool volume type

     Change the EBS volume type for all volumes in a zpool (e.g., gp3 to sc1 or vice versa).

    Args:
        zpool_id (str):
        body (PostZpoolZpoolIdModifyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        zpool_id=zpool_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    zpool_id: str,
    *,
    client: AuthenticatedClient,
    body: PostZpoolZpoolIdModifyBody,
) -> Response[Any]:
    """Modify zpool volume type

     Change the EBS volume type for all volumes in a zpool (e.g., gp3 to sc1 or vice versa).

    Args:
        zpool_id (str):
        body (PostZpoolZpoolIdModifyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        zpool_id=zpool_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
