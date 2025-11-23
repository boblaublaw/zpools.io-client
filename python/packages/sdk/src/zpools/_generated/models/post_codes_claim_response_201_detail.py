from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_codes_claim_response_201_detail_claim import PostCodesClaimResponse201DetailClaim


T = TypeVar("T", bound="PostCodesClaimResponse201Detail")


@_attrs_define
class PostCodesClaimResponse201Detail:
    """
    Attributes:
        balance_after_cents (int | Unset): Balance after claim
        claim (PostCodesClaimResponse201DetailClaim | Unset):
        dev_mode (bool | Unset): Whether in development mode
        pool_remaining_cents (int | Unset): Remaining pool credits
    """

    balance_after_cents: int | Unset = UNSET
    claim: PostCodesClaimResponse201DetailClaim | Unset = UNSET
    dev_mode: bool | Unset = UNSET
    pool_remaining_cents: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        balance_after_cents = self.balance_after_cents

        claim: dict[str, Any] | Unset = UNSET
        if not isinstance(self.claim, Unset):
            claim = self.claim.to_dict()

        dev_mode = self.dev_mode

        pool_remaining_cents = self.pool_remaining_cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if balance_after_cents is not UNSET:
            field_dict["balance_after_cents"] = balance_after_cents
        if claim is not UNSET:
            field_dict["claim"] = claim
        if dev_mode is not UNSET:
            field_dict["dev_mode"] = dev_mode
        if pool_remaining_cents is not UNSET:
            field_dict["pool_remaining_cents"] = pool_remaining_cents

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_codes_claim_response_201_detail_claim import PostCodesClaimResponse201DetailClaim

        d = dict(src_dict)
        balance_after_cents = d.pop("balance_after_cents", UNSET)

        _claim = d.pop("claim", UNSET)
        claim: PostCodesClaimResponse201DetailClaim | Unset
        if isinstance(_claim, Unset):
            claim = UNSET
        else:
            claim = PostCodesClaimResponse201DetailClaim.from_dict(_claim)

        dev_mode = d.pop("dev_mode", UNSET)

        pool_remaining_cents = d.pop("pool_remaining_cents", UNSET)

        post_codes_claim_response_201_detail = cls(
            balance_after_cents=balance_after_cents,
            claim=claim,
            dev_mode=dev_mode,
            pool_remaining_cents=pool_remaining_cents,
        )

        post_codes_claim_response_201_detail.additional_properties = d
        return post_codes_claim_response_201_detail

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
