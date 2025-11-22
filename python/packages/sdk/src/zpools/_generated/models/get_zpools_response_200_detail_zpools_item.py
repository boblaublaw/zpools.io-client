from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetZpoolsResponse200DetailZpoolsItem")


@_attrs_define
class GetZpoolsResponse200DetailZpoolsItem:
    """
    Attributes:
        created_at (datetime.datetime | Unset):
        name (str | Unset):
        size_gb (int | Unset):
        status (str | Unset):
        zpool_id (str | Unset):
    """

    created_at: datetime.datetime | Unset = UNSET
    name: str | Unset = UNSET
    size_gb: int | Unset = UNSET
    status: str | Unset = UNSET
    zpool_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        name = self.name

        size_gb = self.size_gb

        status = self.status

        zpool_id = self.zpool_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if name is not UNSET:
            field_dict["name"] = name
        if size_gb is not UNSET:
            field_dict["size_gb"] = size_gb
        if status is not UNSET:
            field_dict["status"] = status
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

        name = d.pop("name", UNSET)

        size_gb = d.pop("size_gb", UNSET)

        status = d.pop("status", UNSET)

        zpool_id = d.pop("zpool_id", UNSET)

        get_zpools_response_200_detail_zpools_item = cls(
            created_at=created_at,
            name=name,
            size_gb=size_gb,
            status=status,
            zpool_id=zpool_id,
        )

        get_zpools_response_200_detail_zpools_item.additional_properties = d
        return get_zpools_response_200_detail_zpools_item

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
