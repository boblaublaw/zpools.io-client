from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetPatResponse200DetailItemsItem")


@_attrs_define
class GetPatResponse200DetailItemsItem:
    """
    Attributes:
        created_at (datetime.datetime | Unset): Creation timestamp
        expiry_at (datetime.datetime | Unset): Soft expiry timestamp
        hard_expiry_at (datetime.datetime | Unset): Hard expiry timestamp
        key_id (str | Unset): Unique key identifier
        label (str | Unset): Token label
        last_ip (str | Unset): Last IP address used from
        last_ua (str | Unset): Last user agent
        last_used_at (datetime.datetime | Unset): Last usage timestamp
        scopes (list[str] | Unset): List of scopes
        status (str | Unset): Token status (active, revoked, expired)
        token_ver (int | Unset): Token version
        usage_count (int | Unset): Number of times used
    """

    created_at: datetime.datetime | Unset = UNSET
    expiry_at: datetime.datetime | Unset = UNSET
    hard_expiry_at: datetime.datetime | Unset = UNSET
    key_id: str | Unset = UNSET
    label: str | Unset = UNSET
    last_ip: str | Unset = UNSET
    last_ua: str | Unset = UNSET
    last_used_at: datetime.datetime | Unset = UNSET
    scopes: list[str] | Unset = UNSET
    status: str | Unset = UNSET
    token_ver: int | Unset = UNSET
    usage_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        expiry_at: str | Unset = UNSET
        if not isinstance(self.expiry_at, Unset):
            expiry_at = self.expiry_at.isoformat()

        hard_expiry_at: str | Unset = UNSET
        if not isinstance(self.hard_expiry_at, Unset):
            hard_expiry_at = self.hard_expiry_at.isoformat()

        key_id = self.key_id

        label = self.label

        last_ip = self.last_ip

        last_ua = self.last_ua

        last_used_at: str | Unset = UNSET
        if not isinstance(self.last_used_at, Unset):
            last_used_at = self.last_used_at.isoformat()

        scopes: list[str] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        status = self.status

        token_ver = self.token_ver

        usage_count = self.usage_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if expiry_at is not UNSET:
            field_dict["expiry_at"] = expiry_at
        if hard_expiry_at is not UNSET:
            field_dict["hard_expiry_at"] = hard_expiry_at
        if key_id is not UNSET:
            field_dict["key_id"] = key_id
        if label is not UNSET:
            field_dict["label"] = label
        if last_ip is not UNSET:
            field_dict["last_ip"] = last_ip
        if last_ua is not UNSET:
            field_dict["last_ua"] = last_ua
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if status is not UNSET:
            field_dict["status"] = status
        if token_ver is not UNSET:
            field_dict["token_ver"] = token_ver
        if usage_count is not UNSET:
            field_dict["usage_count"] = usage_count

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

        _expiry_at = d.pop("expiry_at", UNSET)
        expiry_at: datetime.datetime | Unset
        if isinstance(_expiry_at, Unset):
            expiry_at = UNSET
        else:
            expiry_at = isoparse(_expiry_at)

        _hard_expiry_at = d.pop("hard_expiry_at", UNSET)
        hard_expiry_at: datetime.datetime | Unset
        if isinstance(_hard_expiry_at, Unset):
            hard_expiry_at = UNSET
        else:
            hard_expiry_at = isoparse(_hard_expiry_at)

        key_id = d.pop("key_id", UNSET)

        label = d.pop("label", UNSET)

        last_ip = d.pop("last_ip", UNSET)

        last_ua = d.pop("last_ua", UNSET)

        _last_used_at = d.pop("last_used_at", UNSET)
        last_used_at: datetime.datetime | Unset
        if isinstance(_last_used_at, Unset):
            last_used_at = UNSET
        else:
            last_used_at = isoparse(_last_used_at)

        scopes = cast(list[str], d.pop("scopes", UNSET))

        status = d.pop("status", UNSET)

        token_ver = d.pop("token_ver", UNSET)

        usage_count = d.pop("usage_count", UNSET)

        get_pat_response_200_detail_items_item = cls(
            created_at=created_at,
            expiry_at=expiry_at,
            hard_expiry_at=hard_expiry_at,
            key_id=key_id,
            label=label,
            last_ip=last_ip,
            last_ua=last_ua,
            last_used_at=last_used_at,
            scopes=scopes,
            status=status,
            token_ver=token_ver,
            usage_count=usage_count,
        )

        get_pat_response_200_detail_items_item.additional_properties = d
        return get_pat_response_200_detail_items_item

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
