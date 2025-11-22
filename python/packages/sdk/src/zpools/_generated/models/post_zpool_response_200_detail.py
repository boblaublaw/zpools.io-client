from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostZpoolResponse200Detail")


@_attrs_define
class PostZpoolResponse200Detail:
    """
    Attributes:
        job_id (str | Unset): Job ID for tracking creation progress
        zpool_id (str | Unset):
    """

    job_id: str | Unset = UNSET
    zpool_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        zpool_id = self.zpool_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if zpool_id is not UNSET:
            field_dict["zpool_id"] = zpool_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id", UNSET)

        zpool_id = d.pop("zpool_id", UNSET)

        post_zpool_response_200_detail = cls(
            job_id=job_id,
            zpool_id=zpool_id,
        )

        post_zpool_response_200_detail.additional_properties = d
        return post_zpool_response_200_detail

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
