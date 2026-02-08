from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostCodesClaimBodyTos")


@_attrs_define
class PostCodesClaimBodyTos:
    """Terms of Service acceptance (required if code requires ToS)

    Attributes:
        accepted_at (datetime.datetime | Unset): ISO8601 timestamp of acceptance
        url (str | Unset): ToS URL being accepted
    """

    accepted_at: datetime.datetime | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accepted_at: str | Unset = UNSET
        if not isinstance(self.accepted_at, Unset):
            accepted_at = self.accepted_at.isoformat()

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accepted_at is not UNSET:
            field_dict["accepted_at"] = accepted_at
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _accepted_at = d.pop("accepted_at", UNSET)
        accepted_at: datetime.datetime | Unset
        if isinstance(_accepted_at, Unset):
            accepted_at = UNSET
        else:
            accepted_at = isoparse(_accepted_at)

        url = d.pop("url", UNSET)

        post_codes_claim_body_tos = cls(
            accepted_at=accepted_at,
            url=url,
        )

        post_codes_claim_body_tos.additional_properties = d
        return post_codes_claim_body_tos

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
