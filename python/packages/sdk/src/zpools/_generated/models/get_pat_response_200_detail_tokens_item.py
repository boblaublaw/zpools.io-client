from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetPatResponse200DetailTokensItem")


@_attrs_define
class GetPatResponse200DetailTokensItem:
    """
    Attributes:
        created_at (datetime.datetime | Unset):
        key_id (str | Unset):
        last_used (datetime.datetime | Unset):
        name (str | Unset): Token name/description
    """

    created_at: datetime.datetime | Unset = UNSET
    key_id: str | Unset = UNSET
    last_used: datetime.datetime | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        key_id = self.key_id

        last_used: str | Unset = UNSET
        if not isinstance(self.last_used, Unset):
            last_used = self.last_used.isoformat()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if key_id is not UNSET:
            field_dict["key_id"] = key_id
        if last_used is not UNSET:
            field_dict["last_used"] = last_used
        if name is not UNSET:
            field_dict["name"] = name

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

        key_id = d.pop("key_id", UNSET)

        _last_used = d.pop("last_used", UNSET)
        last_used: datetime.datetime | Unset
        if isinstance(_last_used, Unset):
            last_used = UNSET
        else:
            last_used = isoparse(_last_used)

        name = d.pop("name", UNSET)

        get_pat_response_200_detail_tokens_item = cls(
            created_at=created_at,
            key_id=key_id,
            last_used=last_used,
            name=name,
        )

        get_pat_response_200_detail_tokens_item.additional_properties = d
        return get_pat_response_200_detail_tokens_item

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
