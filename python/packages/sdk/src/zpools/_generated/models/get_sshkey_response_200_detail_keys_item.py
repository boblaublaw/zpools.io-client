from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSshkeyResponse200DetailKeysItem")


@_attrs_define
class GetSshkeyResponse200DetailKeysItem:
    """
    Attributes:
        created_at (datetime.datetime | Unset):
        pubkey (str | Unset): SSH public key
        pubkey_id (str | Unset): Unique key identifier
    """

    created_at: datetime.datetime | Unset = UNSET
    pubkey: str | Unset = UNSET
    pubkey_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        pubkey = self.pubkey

        pubkey_id = self.pubkey_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if pubkey is not UNSET:
            field_dict["pubkey"] = pubkey
        if pubkey_id is not UNSET:
            field_dict["pubkey_id"] = pubkey_id

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

        pubkey = d.pop("pubkey", UNSET)

        pubkey_id = d.pop("pubkey_id", UNSET)

        get_sshkey_response_200_detail_keys_item = cls(
            created_at=created_at,
            pubkey=pubkey,
            pubkey_id=pubkey_id,
        )

        get_sshkey_response_200_detail_keys_item.additional_properties = d
        return get_sshkey_response_200_detail_keys_item

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
