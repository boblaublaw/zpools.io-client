from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_zpool_zpool_id_modify_body_volume_type import PostZpoolZpoolIdModifyBodyVolumeType

T = TypeVar("T", bound="PostZpoolZpoolIdModifyBody")


@_attrs_define
class PostZpoolZpoolIdModifyBody:
    """
    Attributes:
        volume_type (PostZpoolZpoolIdModifyBodyVolumeType): Target EBS volume type
    """

    volume_type: PostZpoolZpoolIdModifyBodyVolumeType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        volume_type = self.volume_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "volume_type": volume_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        volume_type = PostZpoolZpoolIdModifyBodyVolumeType(d.pop("volume_type"))

        post_zpool_zpool_id_modify_body = cls(
            volume_type=volume_type,
        )

        post_zpool_zpool_id_modify_body.additional_properties = d
        return post_zpool_zpool_id_modify_body

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
