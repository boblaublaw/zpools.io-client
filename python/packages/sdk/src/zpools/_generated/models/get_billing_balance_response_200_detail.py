from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_billing_balance_response_200_detail_balance import GetBillingBalanceResponse200DetailBalance


T = TypeVar("T", bound="GetBillingBalanceResponse200Detail")


@_attrs_define
class GetBillingBalanceResponse200Detail:
    """
    Attributes:
        balance (GetBillingBalanceResponse200DetailBalance | Unset):
    """

    balance: GetBillingBalanceResponse200DetailBalance | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        balance: dict[str, Any] | Unset = UNSET
        if not isinstance(self.balance, Unset):
            balance = self.balance.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if balance is not UNSET:
            field_dict["balance"] = balance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_billing_balance_response_200_detail_balance import GetBillingBalanceResponse200DetailBalance

        d = dict(src_dict)
        _balance = d.pop("balance", UNSET)
        balance: GetBillingBalanceResponse200DetailBalance | Unset
        if isinstance(_balance, Unset):
            balance = UNSET
        else:
            balance = GetBillingBalanceResponse200DetailBalance.from_dict(_balance)

        get_billing_balance_response_200_detail = cls(
            balance=balance,
        )

        get_billing_balance_response_200_detail.additional_properties = d
        return get_billing_balance_response_200_detail

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
