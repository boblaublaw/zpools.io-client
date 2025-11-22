from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostDodoStartResponse200Detail")


@_attrs_define
class PostDodoStartResponse200Detail:
    """
    Attributes:
        payment_url (str | Unset): URL to complete payment
        session_id (str | Unset):
    """

    payment_url: str | Unset = UNSET
    session_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payment_url = self.payment_url

        session_id = self.session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if payment_url is not UNSET:
            field_dict["payment_url"] = payment_url
        if session_id is not UNSET:
            field_dict["session_id"] = session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        payment_url = d.pop("payment_url", UNSET)

        session_id = d.pop("session_id", UNSET)

        post_dodo_start_response_200_detail = cls(
            payment_url=payment_url,
            session_id=session_id,
        )

        post_dodo_start_response_200_detail.additional_properties = d
        return post_dodo_start_response_200_detail

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
