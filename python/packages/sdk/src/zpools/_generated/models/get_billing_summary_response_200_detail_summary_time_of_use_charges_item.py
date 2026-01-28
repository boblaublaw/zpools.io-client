from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBillingSummaryResponse200DetailSummaryTimeOfUseChargesItem")


@_attrs_define
class GetBillingSummaryResponse200DetailSummaryTimeOfUseChargesItem:
    """
    Attributes:
        amount_usd (float | Unset):
        note (str | Unset):
        posted_ts (str | Unset):
        source (str | Unset):
        zpool_id (str | Unset):
    """

    amount_usd: float | Unset = UNSET
    note: str | Unset = UNSET
    posted_ts: str | Unset = UNSET
    source: str | Unset = UNSET
    zpool_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_usd = self.amount_usd

        note = self.note

        posted_ts = self.posted_ts

        source = self.source

        zpool_id = self.zpool_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount_usd is not UNSET:
            field_dict["amount_usd"] = amount_usd
        if note is not UNSET:
            field_dict["note"] = note
        if posted_ts is not UNSET:
            field_dict["posted_ts"] = posted_ts
        if source is not UNSET:
            field_dict["source"] = source
        if zpool_id is not UNSET:
            field_dict["zpool_id"] = zpool_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_usd = d.pop("amount_usd", UNSET)

        note = d.pop("note", UNSET)

        posted_ts = d.pop("posted_ts", UNSET)

        source = d.pop("source", UNSET)

        zpool_id = d.pop("zpool_id", UNSET)

        get_billing_summary_response_200_detail_summary_time_of_use_charges_item = cls(
            amount_usd=amount_usd,
            note=note,
            posted_ts=posted_ts,
            source=source,
            zpool_id=zpool_id,
        )

        get_billing_summary_response_200_detail_summary_time_of_use_charges_item.additional_properties = d
        return get_billing_summary_response_200_detail_summary_time_of_use_charges_item

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
