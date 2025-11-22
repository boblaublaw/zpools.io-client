from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostLoginResponse200Detail")


@_attrs_define
class PostLoginResponse200Detail:
    """
    Attributes:
        access_token (str | Unset): JWT access token
        expires_in (int | Unset): Token expiration in seconds
        id_token (str | Unset): JWT ID token
        refresh_token (str | Unset): JWT refresh token
    """

    access_token: str | Unset = UNSET
    expires_in: int | Unset = UNSET
    id_token: str | Unset = UNSET
    refresh_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        expires_in = self.expires_in

        id_token = self.id_token

        refresh_token = self.refresh_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if access_token is not UNSET:
            field_dict["access_token"] = access_token
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if id_token is not UNSET:
            field_dict["id_token"] = id_token
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_token = d.pop("access_token", UNSET)

        expires_in = d.pop("expires_in", UNSET)

        id_token = d.pop("id_token", UNSET)

        refresh_token = d.pop("refresh_token", UNSET)

        post_login_response_200_detail = cls(
            access_token=access_token,
            expires_in=expires_in,
            id_token=id_token,
            refresh_token=refresh_token,
        )

        post_login_response_200_detail.additional_properties = d
        return post_login_response_200_detail

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
