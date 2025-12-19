from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostZpoolZpoolIdExpandBody")


@_attrs_define
class PostZpoolZpoolIdExpandBody:
    """
    Attributes:
        new_size_in_gib (int): New size in GiB (increases only)
    """

    new_size_in_gib: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_size_in_gib = self.new_size_in_gib

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_size_in_gib": new_size_in_gib,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        new_size_in_gib = d.pop("new_size_in_gib")

        post_zpool_zpool_id_expand_body = cls(
            new_size_in_gib=new_size_in_gib,
        )

        post_zpool_zpool_id_expand_body.additional_properties = d
        return post_zpool_zpool_id_expand_body

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
