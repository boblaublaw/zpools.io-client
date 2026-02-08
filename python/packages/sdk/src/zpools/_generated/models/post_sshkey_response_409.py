from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_sshkey_response_409_detail import PostSshkeyResponse409Detail


T = TypeVar("T", bound="PostSshkeyResponse409")


@_attrs_define
class PostSshkeyResponse409:
    """
    Attributes:
        detail (PostSshkeyResponse409Detail | Unset):
        message (str | Unset): e.g. SSH key already registered
    """

    detail: PostSshkeyResponse409Detail | Unset = UNSET
    message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail: dict[str, Any] | Unset = UNSET
        if not isinstance(self.detail, Unset):
            detail = self.detail.to_dict()

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_sshkey_response_409_detail import PostSshkeyResponse409Detail

        d = dict(src_dict)
        _detail = d.pop("detail", UNSET)
        detail: PostSshkeyResponse409Detail | Unset
        if isinstance(_detail, Unset):
            detail = UNSET
        else:
            detail = PostSshkeyResponse409Detail.from_dict(_detail)

        message = d.pop("message", UNSET)

        post_sshkey_response_409 = cls(
            detail=detail,
            message=message,
        )

        post_sshkey_response_409.additional_properties = d
        return post_sshkey_response_409

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
