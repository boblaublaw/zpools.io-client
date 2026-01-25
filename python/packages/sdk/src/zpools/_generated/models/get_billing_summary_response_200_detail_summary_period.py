from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBillingSummaryResponse200DetailSummaryPeriod")


@_attrs_define
class GetBillingSummaryResponse200DetailSummaryPeriod:
    """
    Attributes:
        from_date (str | Unset):
        to_date (str | Unset):
    """

    from_date: str | Unset = UNSET
    to_date: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_date = self.from_date

        to_date = self.to_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if from_date is not UNSET:
            field_dict["from_date"] = from_date
        if to_date is not UNSET:
            field_dict["to_date"] = to_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_date = d.pop("from_date", UNSET)

        to_date = d.pop("to_date", UNSET)

        get_billing_summary_response_200_detail_summary_period = cls(
            from_date=from_date,
            to_date=to_date,
        )

        get_billing_summary_response_200_detail_summary_period.additional_properties = d
        return get_billing_summary_response_200_detail_summary_period

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
