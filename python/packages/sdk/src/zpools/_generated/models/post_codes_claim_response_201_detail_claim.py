from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostCodesClaimResponse201DetailClaim")


@_attrs_define
class PostCodesClaimResponse201DetailClaim:
    """
    Attributes:
        amount_cents (int | Unset): Credits added in cents
        code (str | Unset): Code that was claimed
        code_type (str | Unset): Type of code
        joined_group (str | Unset): Group joined (if applicable)
    """

    amount_cents: int | Unset = UNSET
    code: str | Unset = UNSET
    code_type: str | Unset = UNSET
    joined_group: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_cents = self.amount_cents

        code = self.code

        code_type = self.code_type

        joined_group = self.joined_group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount_cents is not UNSET:
            field_dict["amount_cents"] = amount_cents
        if code is not UNSET:
            field_dict["code"] = code
        if code_type is not UNSET:
            field_dict["code_type"] = code_type
        if joined_group is not UNSET:
            field_dict["joined_group"] = joined_group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_cents = d.pop("amount_cents", UNSET)

        code = d.pop("code", UNSET)

        code_type = d.pop("code_type", UNSET)

        joined_group = d.pop("joined_group", UNSET)

        post_codes_claim_response_201_detail_claim = cls(
            amount_cents=amount_cents,
            code=code,
            code_type=code_type,
            joined_group=joined_group,
        )

        post_codes_claim_response_201_detail_claim.additional_properties = d
        return post_codes_claim_response_201_detail_claim

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
