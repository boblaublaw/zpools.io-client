import datetime
from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...models.get_billing_ledger_response_200 import GetBillingLedgerResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    since: datetime.date | Unset = UNSET,
    until: datetime.date | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_since: str | Unset = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    json_until: str | Unset = UNSET
    if not isinstance(until, Unset):
        json_until = until.isoformat()
    params["until"] = json_until

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/billing/ledger",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GetBillingLedgerResponse200:
    if response.status_code == 200:
        response_200 = GetBillingLedgerResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    response_default = cast(Any, None)
    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | GetBillingLedgerResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    since: datetime.date | Unset = UNSET,
    until: datetime.date | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Any | GetBillingLedgerResponse200]:
    """Get billing ledger

     Retrieve billing transaction history with optional date filters.

    Args:
        since (datetime.date | Unset):
        until (datetime.date | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetBillingLedgerResponse200]
    """

    kwargs = _get_kwargs(
        since=since,
        until=until,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    since: datetime.date | Unset = UNSET,
    until: datetime.date | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Any | GetBillingLedgerResponse200 | None:
    """Get billing ledger

     Retrieve billing transaction history with optional date filters.

    Args:
        since (datetime.date | Unset):
        until (datetime.date | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GetBillingLedgerResponse200
    """

    return sync_detailed(
        client=client,
        since=since,
        until=until,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    since: datetime.date | Unset = UNSET,
    until: datetime.date | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Any | GetBillingLedgerResponse200]:
    """Get billing ledger

     Retrieve billing transaction history with optional date filters.

    Args:
        since (datetime.date | Unset):
        until (datetime.date | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetBillingLedgerResponse200]
    """

    kwargs = _get_kwargs(
        since=since,
        until=until,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    since: datetime.date | Unset = UNSET,
    until: datetime.date | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Any | GetBillingLedgerResponse200 | None:
    """Get billing ledger

     Retrieve billing transaction history with optional date filters.

    Args:
        since (datetime.date | Unset):
        until (datetime.date | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GetBillingLedgerResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            since=since,
            until=until,
            limit=limit,
        )
    ).parsed
