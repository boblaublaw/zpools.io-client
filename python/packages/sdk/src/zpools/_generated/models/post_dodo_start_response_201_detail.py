from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostDodoStartResponse201Detail")


@_attrs_define
class PostDodoStartResponse201Detail:
    """
    Attributes:
        payment_link (str | Unset): URL to complete payment
        purchase_id (str | Unset):
    """

    payment_link: str | Unset = UNSET
    purchase_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payment_link = self.payment_link

        purchase_id = self.purchase_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if payment_link is not UNSET:
            field_dict["payment_link"] = payment_link
        if purchase_id is not UNSET:
            field_dict["purchase_id"] = purchase_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        payment_link = d.pop("payment_link", UNSET)

        purchase_id = d.pop("purchase_id", UNSET)

        post_dodo_start_response_201_detail = cls(
            payment_link=payment_link,
            purchase_id=purchase_id,
        )

        post_dodo_start_response_201_detail.additional_properties = d
        return post_dodo_start_response_201_detail

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
