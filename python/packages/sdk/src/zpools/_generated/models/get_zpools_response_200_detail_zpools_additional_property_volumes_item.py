from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetZpoolsResponse200DetailZpoolsAdditionalPropertyVolumesItem")


@_attrs_define
class GetZpoolsResponse200DetailZpoolsAdditionalPropertyVolumesItem:
    """
    Attributes:
        can_modify_now (bool | Unset):
        create_time (datetime.datetime | Unset):
        mod_last_time (datetime.datetime | None | Unset):
        mod_progress (int | None | Unset):
        mod_state (str | Unset):
        size (int | Unset): Volume size in GiB (1024³ bytes)
        state (str | Unset):
        volume_type (str | Unset):
    """

    can_modify_now: bool | Unset = UNSET
    create_time: datetime.datetime | Unset = UNSET
    mod_last_time: datetime.datetime | None | Unset = UNSET
    mod_progress: int | None | Unset = UNSET
    mod_state: str | Unset = UNSET
    size: int | Unset = UNSET
    state: str | Unset = UNSET
    volume_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        can_modify_now = self.can_modify_now

        create_time: str | Unset = UNSET
        if not isinstance(self.create_time, Unset):
            create_time = self.create_time.isoformat()

        mod_last_time: None | str | Unset
        if isinstance(self.mod_last_time, Unset):
            mod_last_time = UNSET
        elif isinstance(self.mod_last_time, datetime.datetime):
            mod_last_time = self.mod_last_time.isoformat()
        else:
            mod_last_time = self.mod_last_time

        mod_progress: int | None | Unset
        if isinstance(self.mod_progress, Unset):
            mod_progress = UNSET
        else:
            mod_progress = self.mod_progress

        mod_state = self.mod_state

        size = self.size

        state = self.state

        volume_type = self.volume_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if can_modify_now is not UNSET:
            field_dict["CanModifyNow"] = can_modify_now
        if create_time is not UNSET:
            field_dict["CreateTime"] = create_time
        if mod_last_time is not UNSET:
            field_dict["ModLastTime"] = mod_last_time
        if mod_progress is not UNSET:
            field_dict["ModProgress"] = mod_progress
        if mod_state is not UNSET:
            field_dict["ModState"] = mod_state
        if size is not UNSET:
            field_dict["Size"] = size
        if state is not UNSET:
            field_dict["State"] = state
        if volume_type is not UNSET:
            field_dict["VolumeType"] = volume_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        can_modify_now = d.pop("CanModifyNow", UNSET)

        _create_time = d.pop("CreateTime", UNSET)
        create_time: datetime.datetime | Unset
        if isinstance(_create_time, Unset):
            create_time = UNSET
        else:
            create_time = isoparse(_create_time)

        def _parse_mod_last_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mod_last_time_type_0 = isoparse(data)

                return mod_last_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        mod_last_time = _parse_mod_last_time(d.pop("ModLastTime", UNSET))

        def _parse_mod_progress(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        mod_progress = _parse_mod_progress(d.pop("ModProgress", UNSET))

        mod_state = d.pop("ModState", UNSET)

        size = d.pop("Size", UNSET)

        state = d.pop("State", UNSET)

        volume_type = d.pop("VolumeType", UNSET)

        get_zpools_response_200_detail_zpools_additional_property_volumes_item = cls(
            can_modify_now=can_modify_now,
            create_time=create_time,
            mod_last_time=mod_last_time,
            mod_progress=mod_progress,
            mod_state=mod_state,
            size=size,
            state=state,
            volume_type=volume_type,
        )

        get_zpools_response_200_detail_zpools_additional_property_volumes_item.additional_properties = d
        return get_zpools_response_200_detail_zpools_additional_property_volumes_item

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
