from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBillingLedgerResponse200DetailEntriesItem")


@_attrs_define
class GetBillingLedgerResponse200DetailEntriesItem:
    """
    Attributes:
        amount_cents (int | Unset): Amount in cents (negative for charges)
        balance_cents (int | Unset): Running balance after transaction
        description (str | Unset):
        timestamp (datetime.datetime | Unset):
    """

    amount_cents: int | Unset = UNSET
    balance_cents: int | Unset = UNSET
    description: str | Unset = UNSET
    timestamp: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_cents = self.amount_cents

        balance_cents = self.balance_cents

        description = self.description

        timestamp: str | Unset = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount_cents is not UNSET:
            field_dict["amount_cents"] = amount_cents
        if balance_cents is not UNSET:
            field_dict["balance_cents"] = balance_cents
        if description is not UNSET:
            field_dict["description"] = description
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_cents = d.pop("amount_cents", UNSET)

        balance_cents = d.pop("balance_cents", UNSET)

        description = d.pop("description", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: datetime.datetime | Unset
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        get_billing_ledger_response_200_detail_entries_item = cls(
            amount_cents=amount_cents,
            balance_cents=balance_cents,
            description=description,
            timestamp=timestamp,
        )

        get_billing_ledger_response_200_detail_entries_item.additional_properties = d
        return get_billing_ledger_response_200_detail_entries_item

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
