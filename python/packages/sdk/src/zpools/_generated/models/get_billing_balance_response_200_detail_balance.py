from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetBillingBalanceResponse200DetailBalance")


@_attrs_define
class GetBillingBalanceResponse200DetailBalance:
    """
    Attributes:
        balance_usd (float | Unset): Balance in USD
        customer (str | Unset): Customer username
        first_transaction (datetime.datetime | Unset): First transaction timestamp
        last_reconciliation (datetime.datetime | Unset): Last reconciliation timestamp
        last_transaction (datetime.datetime | Unset): Last transaction timestamp
        last_update_ts (datetime.datetime | Unset): Last update timestamp
    """

    balance_usd: float | Unset = UNSET
    customer: str | Unset = UNSET
    first_transaction: datetime.datetime | Unset = UNSET
    last_reconciliation: datetime.datetime | Unset = UNSET
    last_transaction: datetime.datetime | Unset = UNSET
    last_update_ts: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        balance_usd = self.balance_usd

        customer = self.customer

        first_transaction: str | Unset = UNSET
        if not isinstance(self.first_transaction, Unset):
            first_transaction = self.first_transaction.isoformat()

        last_reconciliation: str | Unset = UNSET
        if not isinstance(self.last_reconciliation, Unset):
            last_reconciliation = self.last_reconciliation.isoformat()

        last_transaction: str | Unset = UNSET
        if not isinstance(self.last_transaction, Unset):
            last_transaction = self.last_transaction.isoformat()

        last_update_ts: str | Unset = UNSET
        if not isinstance(self.last_update_ts, Unset):
            last_update_ts = self.last_update_ts.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if balance_usd is not UNSET:
            field_dict["balance_usd"] = balance_usd
        if customer is not UNSET:
            field_dict["customer"] = customer
        if first_transaction is not UNSET:
            field_dict["first_transaction"] = first_transaction
        if last_reconciliation is not UNSET:
            field_dict["last_reconciliation"] = last_reconciliation
        if last_transaction is not UNSET:
            field_dict["last_transaction"] = last_transaction
        if last_update_ts is not UNSET:
            field_dict["last_update_ts"] = last_update_ts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        balance_usd = d.pop("balance_usd", UNSET)

        customer = d.pop("customer", UNSET)

        _first_transaction = d.pop("first_transaction", UNSET)
        first_transaction: datetime.datetime | Unset
        if isinstance(_first_transaction, Unset):
            first_transaction = UNSET
        else:
            first_transaction = isoparse(_first_transaction)

        _last_reconciliation = d.pop("last_reconciliation", UNSET)
        last_reconciliation: datetime.datetime | Unset
        if isinstance(_last_reconciliation, Unset):
            last_reconciliation = UNSET
        else:
            last_reconciliation = isoparse(_last_reconciliation)

        _last_transaction = d.pop("last_transaction", UNSET)
        last_transaction: datetime.datetime | Unset
        if isinstance(_last_transaction, Unset):
            last_transaction = UNSET
        else:
            last_transaction = isoparse(_last_transaction)

        _last_update_ts = d.pop("last_update_ts", UNSET)
        last_update_ts: datetime.datetime | Unset
        if isinstance(_last_update_ts, Unset):
            last_update_ts = UNSET
        else:
            last_update_ts = isoparse(_last_update_ts)

        get_billing_balance_response_200_detail_balance = cls(
            balance_usd=balance_usd,
            customer=customer,
            first_transaction=first_transaction,
            last_reconciliation=last_reconciliation,
            last_transaction=last_transaction,
            last_update_ts=last_update_ts,
        )

        get_billing_balance_response_200_detail_balance.additional_properties = d
        return get_billing_balance_response_200_detail_balance

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
