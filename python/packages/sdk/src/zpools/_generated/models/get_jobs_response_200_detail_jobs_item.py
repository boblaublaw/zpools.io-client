from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_jobs_response_200_detail_jobs_item_status import GetJobsResponse200DetailJobsItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetJobsResponse200DetailJobsItem")


@_attrs_define
class GetJobsResponse200DetailJobsItem:
    """
    Attributes:
        created_at (datetime.datetime | Unset):
        job_id (str | Unset):
        operation (str | Unset): Operation type (create, delete, scrub, modify)
        status (GetJobsResponse200DetailJobsItemStatus | Unset): Job status. Accepted values: pending, running,
            completed, failed
        updated_at (datetime.datetime | Unset):
        zpool_id (str | Unset):
    """

    created_at: datetime.datetime | Unset = UNSET
    job_id: str | Unset = UNSET
    operation: str | Unset = UNSET
    status: GetJobsResponse200DetailJobsItemStatus | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    zpool_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        job_id = self.job_id

        operation = self.operation

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        zpool_id = self.zpool_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if operation is not UNSET:
            field_dict["operation"] = operation
        if status is not UNSET:
            field_dict["status"] = status
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if zpool_id is not UNSET:
            field_dict["zpool_id"] = zpool_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        job_id = d.pop("job_id", UNSET)

        operation = d.pop("operation", UNSET)

        _status = d.pop("status", UNSET)
        status: GetJobsResponse200DetailJobsItemStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GetJobsResponse200DetailJobsItemStatus(_status)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        zpool_id = d.pop("zpool_id", UNSET)

        get_jobs_response_200_detail_jobs_item = cls(
            created_at=created_at,
            job_id=job_id,
            operation=operation,
            status=status,
            updated_at=updated_at,
            zpool_id=zpool_id,
        )

        get_jobs_response_200_detail_jobs_item.additional_properties = d
        return get_jobs_response_200_detail_jobs_item

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
