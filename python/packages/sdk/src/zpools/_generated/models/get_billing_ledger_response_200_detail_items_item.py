from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBillingLedgerResponse200DetailItemsItem")


@_attrs_define
class GetBillingLedgerResponse200DetailItemsItem:
    """
    Attributes:
        amount_usd (float | Unset): Total amount in USD
        event_ts (str | Unset): Timestamp when the event occurred (ISO-8601). For hourly_ebs: start of billed hour. For
            atomic events (admin, claim): equals posted_ts.
        event_type (str | Unset): Type of event (e.g., debit, credit)
        markup_bps (float | Unset): Markup in basis points
        markup_usd (float | Unset): Markup amount in USD
        note (str | Unset): Additional notes
        posted_ts (str | Unset): Timestamp when the entry was posted/recorded (ISO-8601)
        source (str | Unset): Source of the charge or credit
    """

    amount_usd: float | Unset = UNSET
    event_ts: str | Unset = UNSET
    event_type: str | Unset = UNSET
    markup_bps: float | Unset = UNSET
    markup_usd: float | Unset = UNSET
    note: str | Unset = UNSET
    posted_ts: str | Unset = UNSET
    source: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_usd = self.amount_usd

        event_ts = self.event_ts

        event_type = self.event_type

        markup_bps = self.markup_bps

        markup_usd = self.markup_usd

        note = self.note

        posted_ts = self.posted_ts

        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount_usd is not UNSET:
            field_dict["amount_usd"] = amount_usd
        if event_ts is not UNSET:
            field_dict["event_ts"] = event_ts
        if event_type is not UNSET:
            field_dict["event_type"] = event_type
        if markup_bps is not UNSET:
            field_dict["markup_bps"] = markup_bps
        if markup_usd is not UNSET:
            field_dict["markup_usd"] = markup_usd
        if note is not UNSET:
            field_dict["note"] = note
        if posted_ts is not UNSET:
            field_dict["posted_ts"] = posted_ts
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_usd = d.pop("amount_usd", UNSET)

        event_ts = d.pop("event_ts", UNSET)

        event_type = d.pop("event_type", UNSET)

        markup_bps = d.pop("markup_bps", UNSET)

        markup_usd = d.pop("markup_usd", UNSET)

        note = d.pop("note", UNSET)

        posted_ts = d.pop("posted_ts", UNSET)

        source = d.pop("source", UNSET)

        get_billing_ledger_response_200_detail_items_item = cls(
            amount_usd=amount_usd,
            event_ts=event_ts,
            event_type=event_type,
            markup_bps=markup_bps,
            markup_usd=markup_usd,
            note=note,
            posted_ts=posted_ts,
            source=source,
        )

        get_billing_ledger_response_200_detail_items_item.additional_properties = d
        return get_billing_ledger_response_200_detail_items_item

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
