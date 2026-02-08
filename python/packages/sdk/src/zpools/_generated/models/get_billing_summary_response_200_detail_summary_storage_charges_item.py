from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBillingSummaryResponse200DetailSummaryStorageChargesItem")


@_attrs_define
class GetBillingSummaryResponse200DetailSummaryStorageChargesItem:
    """
    Attributes:
        daily_rate (float | Unset):
        from_ts (str | Unset):
        hourly_rate (float | Unset):
        hours (int | Unset):
        size_gb (int | Unset):
        to_ts (str | Unset):
        total_charges (float | Unset):
        volume_type (str | Unset):
        zpool_id (str | Unset):
    """

    daily_rate: float | Unset = UNSET
    from_ts: str | Unset = UNSET
    hourly_rate: float | Unset = UNSET
    hours: int | Unset = UNSET
    size_gb: int | Unset = UNSET
    to_ts: str | Unset = UNSET
    total_charges: float | Unset = UNSET
    volume_type: str | Unset = UNSET
    zpool_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        daily_rate = self.daily_rate

        from_ts = self.from_ts

        hourly_rate = self.hourly_rate

        hours = self.hours

        size_gb = self.size_gb

        to_ts = self.to_ts

        total_charges = self.total_charges

        volume_type = self.volume_type

        zpool_id = self.zpool_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if daily_rate is not UNSET:
            field_dict["daily_rate"] = daily_rate
        if from_ts is not UNSET:
            field_dict["from_ts"] = from_ts
        if hourly_rate is not UNSET:
            field_dict["hourly_rate"] = hourly_rate
        if hours is not UNSET:
            field_dict["hours"] = hours
        if size_gb is not UNSET:
            field_dict["size_gb"] = size_gb
        if to_ts is not UNSET:
            field_dict["to_ts"] = to_ts
        if total_charges is not UNSET:
            field_dict["total_charges"] = total_charges
        if volume_type is not UNSET:
            field_dict["volume_type"] = volume_type
        if zpool_id is not UNSET:
            field_dict["zpool_id"] = zpool_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        daily_rate = d.pop("daily_rate", UNSET)

        from_ts = d.pop("from_ts", UNSET)

        hourly_rate = d.pop("hourly_rate", UNSET)

        hours = d.pop("hours", UNSET)

        size_gb = d.pop("size_gb", UNSET)

        to_ts = d.pop("to_ts", UNSET)

        total_charges = d.pop("total_charges", UNSET)

        volume_type = d.pop("volume_type", UNSET)

        zpool_id = d.pop("zpool_id", UNSET)

        get_billing_summary_response_200_detail_summary_storage_charges_item = cls(
            daily_rate=daily_rate,
            from_ts=from_ts,
            hourly_rate=hourly_rate,
            hours=hours,
            size_gb=size_gb,
            to_ts=to_ts,
            total_charges=total_charges,
            volume_type=volume_type,
            zpool_id=zpool_id,
        )

        get_billing_summary_response_200_detail_summary_storage_charges_item.additional_properties = d
        return get_billing_summary_response_200_detail_summary_storage_charges_item

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
