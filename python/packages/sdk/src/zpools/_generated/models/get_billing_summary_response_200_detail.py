from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_billing_summary_response_200_detail_summary import GetBillingSummaryResponse200DetailSummary


T = TypeVar("T", bound="GetBillingSummaryResponse200Detail")


@_attrs_define
class GetBillingSummaryResponse200Detail:
    """
    Attributes:
        note (str | Unset): Clarification about ending_balance vs current balance
        summary (GetBillingSummaryResponse200DetailSummary | Unset):
    """

    note: str | Unset = UNSET
    summary: GetBillingSummaryResponse200DetailSummary | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        note = self.note

        summary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.summary, Unset):
            summary = self.summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if note is not UNSET:
            field_dict["note"] = note
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_billing_summary_response_200_detail_summary import GetBillingSummaryResponse200DetailSummary

        d = dict(src_dict)
        note = d.pop("note", UNSET)

        _summary = d.pop("summary", UNSET)
        summary: GetBillingSummaryResponse200DetailSummary | Unset
        if isinstance(_summary, Unset):
            summary = UNSET
        else:
            summary = GetBillingSummaryResponse200DetailSummary.from_dict(_summary)

        get_billing_summary_response_200_detail = cls(
            note=note,
            summary=summary,
        )

        get_billing_summary_response_200_detail.additional_properties = d
        return get_billing_summary_response_200_detail

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
