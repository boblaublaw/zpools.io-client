from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_codes_claim_body_tos import PostCodesClaimBodyTos


T = TypeVar("T", bound="PostCodesClaimBody")


@_attrs_define
class PostCodesClaimBody:
    """
    Attributes:
        code (str): Credit code to redeem
        tos (PostCodesClaimBodyTos | Unset): Terms of Service acceptance (required if code requires ToS)
    """

    code: str
    tos: PostCodesClaimBodyTos | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        tos: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tos, Unset):
            tos = self.tos.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
            }
        )
        if tos is not UNSET:
            field_dict["tos"] = tos

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_codes_claim_body_tos import PostCodesClaimBodyTos

        d = dict(src_dict)
        code = d.pop("code")

        _tos = d.pop("tos", UNSET)
        tos: PostCodesClaimBodyTos | Unset
        if isinstance(_tos, Unset):
            tos = UNSET
        else:
            tos = PostCodesClaimBodyTos.from_dict(_tos)

        post_codes_claim_body = cls(
            code=code,
            tos=tos,
        )

        post_codes_claim_body.additional_properties = d
        return post_codes_claim_body

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
