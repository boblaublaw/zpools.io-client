from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBillingSummaryResponse200DetailSummaryTotals")


@_attrs_define
class GetBillingSummaryResponse200DetailSummaryTotals:
    """
    Attributes:
        credits_applied (float | Unset):
        ending_balance (float | Unset):
        period_net (float | Unset):
        storage_charges (float | Unset):
        time_of_use_charges (float | Unset):
    """

    credits_applied: float | Unset = UNSET
    ending_balance: float | Unset = UNSET
    period_net: float | Unset = UNSET
    storage_charges: float | Unset = UNSET
    time_of_use_charges: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        credits_applied = self.credits_applied

        ending_balance = self.ending_balance

        period_net = self.period_net

        storage_charges = self.storage_charges

        time_of_use_charges = self.time_of_use_charges

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if credits_applied is not UNSET:
            field_dict["credits_applied"] = credits_applied
        if ending_balance is not UNSET:
            field_dict["ending_balance"] = ending_balance
        if period_net is not UNSET:
            field_dict["period_net"] = period_net
        if storage_charges is not UNSET:
            field_dict["storage_charges"] = storage_charges
        if time_of_use_charges is not UNSET:
            field_dict["time_of_use_charges"] = time_of_use_charges

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credits_applied = d.pop("credits_applied", UNSET)

        ending_balance = d.pop("ending_balance", UNSET)

        period_net = d.pop("period_net", UNSET)

        storage_charges = d.pop("storage_charges", UNSET)

        time_of_use_charges = d.pop("time_of_use_charges", UNSET)

        get_billing_summary_response_200_detail_summary_totals = cls(
            credits_applied=credits_applied,
            ending_balance=ending_balance,
            period_net=period_net,
            storage_charges=storage_charges,
            time_of_use_charges=time_of_use_charges,
        )

        get_billing_summary_response_200_detail_summary_totals.additional_properties = d
        return get_billing_summary_response_200_detail_summary_totals

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
