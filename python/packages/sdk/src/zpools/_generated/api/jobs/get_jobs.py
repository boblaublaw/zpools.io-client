import datetime
from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...models.get_jobs_response_200 import GetJobsResponse200
from ...models.get_jobs_sort import GetJobsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
    after: datetime.datetime | Unset = UNSET,
    sort: GetJobsSort | Unset = GetJobsSort.DESC,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    json_before: str | Unset = UNSET
    if not isinstance(before, Unset):
        json_before = before.isoformat()
    params["before"] = json_before

    json_after: str | Unset = UNSET
    if not isinstance(after, Unset):
        json_after = after.isoformat()
    params["after"] = json_after

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | GetJobsResponse200:
    if response.status_code == 200:
        response_200 = GetJobsResponse200.from_dict(response.json())

        return response_200

    response_default = cast(Any, None)
    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | GetJobsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
    after: datetime.datetime | Unset = UNSET,
    sort: GetJobsSort | Unset = GetJobsSort.DESC,
) -> Response[Any | GetJobsResponse200]:
    """List user's jobs

     Retrieve all background jobs (zpool operations) for the authenticated user.

    Args:
        limit (int | Unset):  Default: 100.
        before (datetime.datetime | Unset):
        after (datetime.datetime | Unset):
        sort (GetJobsSort | Unset):  Default: GetJobsSort.DESC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetJobsResponse200]
    """

    kwargs = _get_kwargs(
        limit=limit,
        before=before,
        after=after,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
    after: datetime.datetime | Unset = UNSET,
    sort: GetJobsSort | Unset = GetJobsSort.DESC,
) -> Any | GetJobsResponse200 | None:
    """List user's jobs

     Retrieve all background jobs (zpool operations) for the authenticated user.

    Args:
        limit (int | Unset):  Default: 100.
        before (datetime.datetime | Unset):
        after (datetime.datetime | Unset):
        sort (GetJobsSort | Unset):  Default: GetJobsSort.DESC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GetJobsResponse200
    """

    return sync_detailed(
        client=client,
        limit=limit,
        before=before,
        after=after,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
    after: datetime.datetime | Unset = UNSET,
    sort: GetJobsSort | Unset = GetJobsSort.DESC,
) -> Response[Any | GetJobsResponse200]:
    """List user's jobs

     Retrieve all background jobs (zpool operations) for the authenticated user.

    Args:
        limit (int | Unset):  Default: 100.
        before (datetime.datetime | Unset):
        after (datetime.datetime | Unset):
        sort (GetJobsSort | Unset):  Default: GetJobsSort.DESC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GetJobsResponse200]
    """

    kwargs = _get_kwargs(
        limit=limit,
        before=before,
        after=after,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 100,
    before: datetime.datetime | Unset = UNSET,
    after: datetime.datetime | Unset = UNSET,
    sort: GetJobsSort | Unset = GetJobsSort.DESC,
) -> Any | GetJobsResponse200 | None:
    """List user's jobs

     Retrieve all background jobs (zpool operations) for the authenticated user.

    Args:
        limit (int | Unset):  Default: 100.
        before (datetime.datetime | Unset):
        after (datetime.datetime | Unset):
        sort (GetJobsSort | Unset):  Default: GetJobsSort.DESC.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GetJobsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            before=before,
            after=after,
            sort=sort,
        )
    ).parsed
