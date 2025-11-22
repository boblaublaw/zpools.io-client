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
        balance_cents (int | Unset): Balance in cents
        currency (str | Unset): Currency code (USD)
        last_updated (datetime.datetime | Unset):
        username (str | Unset):
    """

    balance_cents: int | Unset = UNSET
    currency: str | Unset = UNSET
    last_updated: datetime.datetime | Unset = UNSET
    username: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        balance_cents = self.balance_cents

        currency = self.currency

        last_updated: str | Unset = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if balance_cents is not UNSET:
            field_dict["balance_cents"] = balance_cents
        if currency is not UNSET:
            field_dict["currency"] = currency
        if last_updated is not UNSET:
            field_dict["last_updated"] = last_updated
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        balance_cents = d.pop("balance_cents", UNSET)

        currency = d.pop("currency", UNSET)

        _last_updated = d.pop("last_updated", UNSET)
        last_updated: datetime.datetime | Unset
        if isinstance(_last_updated, Unset):
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)

        username = d.pop("username", UNSET)

        get_billing_balance_response_200_detail_balance = cls(
            balance_cents=balance_cents,
            currency=currency,
            last_updated=last_updated,
            username=username,
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
