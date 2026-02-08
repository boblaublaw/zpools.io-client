from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostPatBody")


@_attrs_define
class PostPatBody:
    """
    Attributes:
        label (str): Token label for identification
        expiry (datetime.date | Unset): Optional soft expiry date (YYYY-MM-DD)
        scopes (list[str] | Unset): Optional list of scopes (e.g., 'pat', 'sshkey', 'job', 'zpool')
        tenant_id (str | Unset): Optional tenant ID for multi-tenant scenarios
    """

    label: str
    expiry: datetime.date | Unset = UNSET
    scopes: list[str] | Unset = UNSET
    tenant_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        expiry: str | Unset = UNSET
        if not isinstance(self.expiry, Unset):
            expiry = self.expiry.isoformat()

        scopes: list[str] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
            }
        )
        if expiry is not UNSET:
            field_dict["expiry"] = expiry
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        _expiry = d.pop("expiry", UNSET)
        expiry: datetime.date | Unset
        if isinstance(_expiry, Unset):
            expiry = UNSET
        else:
            expiry = isoparse(_expiry).date()

        scopes = cast(list[str], d.pop("scopes", UNSET))

        tenant_id = d.pop("tenant_id", UNSET)

        post_pat_body = cls(
            label=label,
            expiry=expiry,
            scopes=scopes,
            tenant_id=tenant_id,
        )

        post_pat_body.additional_properties = d
        return post_pat_body

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
