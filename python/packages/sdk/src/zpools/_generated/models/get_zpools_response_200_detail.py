from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_zpools_response_200_detail_zpools_item import GetZpoolsResponse200DetailZpoolsItem


T = TypeVar("T", bound="GetZpoolsResponse200Detail")


@_attrs_define
class GetZpoolsResponse200Detail:
    """
    Attributes:
        zpools (list[GetZpoolsResponse200DetailZpoolsItem] | Unset):
    """

    zpools: list[GetZpoolsResponse200DetailZpoolsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        zpools: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.zpools, Unset):
            zpools = []
            for zpools_item_data in self.zpools:
                zpools_item = zpools_item_data.to_dict()
                zpools.append(zpools_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if zpools is not UNSET:
            field_dict["zpools"] = zpools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_zpools_response_200_detail_zpools_item import GetZpoolsResponse200DetailZpoolsItem

        d = dict(src_dict)
        _zpools = d.pop("zpools", UNSET)
        zpools: list[GetZpoolsResponse200DetailZpoolsItem] | Unset = UNSET
        if _zpools is not UNSET:
            zpools = []
            for zpools_item_data in _zpools:
                zpools_item = GetZpoolsResponse200DetailZpoolsItem.from_dict(zpools_item_data)

                zpools.append(zpools_item)

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
