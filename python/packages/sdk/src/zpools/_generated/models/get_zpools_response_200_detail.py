from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_zpools_response_200_detail_zpools import GetZpoolsResponse200DetailZpools


T = TypeVar("T", bound="GetZpoolsResponse200Detail")


@_attrs_define
class GetZpoolsResponse200Detail:
    """
    Attributes:
        zpools (GetZpoolsResponse200DetailZpools | Unset): Dictionary of zpools keyed by zpool_id
    """

    zpools: GetZpoolsResponse200DetailZpools | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        zpools: dict[str, Any] | Unset = UNSET
        if not isinstance(self.zpools, Unset):
            zpools = self.zpools.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if zpools is not UNSET:
            field_dict["zpools"] = zpools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_zpools_response_200_detail_zpools import GetZpoolsResponse200DetailZpools

        d = dict(src_dict)
        _zpools = d.pop("zpools", UNSET)
        zpools: GetZpoolsResponse200DetailZpools | Unset
        if isinstance(_zpools, Unset):
            zpools = UNSET
        else:
            zpools = GetZpoolsResponse200DetailZpools.from_dict(_zpools)

        get_zpools_response_200_detail = cls(
            zpools=zpools,
        )

        get_zpools_response_200_detail.additional_properties = d
        return get_zpools_response_200_detail

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
