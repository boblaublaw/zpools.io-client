from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostCodesClaimResponse428Detail")


@_attrs_define
class PostCodesClaimResponse428Detail:
    """
    Attributes:
        tos_url (str | Unset): URL of terms that must be accepted
    """

    tos_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tos_url = self.tos_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tos_url is not UNSET:
            field_dict["tos_url"] = tos_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tos_url = d.pop("tos_url", UNSET)

        post_codes_claim_response_428_detail = cls(
            tos_url=tos_url,
        )

        post_codes_claim_response_428_detail.additional_properties = d
        return post_codes_claim_response_428_detail

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
