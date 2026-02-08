from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_zpools_response_200_detail_zpools_additional_property_volumes_item import (
        GetZpoolsResponse200DetailZpoolsAdditionalPropertyVolumesItem,
    )


T = TypeVar("T", bound="GetZpoolsResponse200DetailZpoolsAdditionalProperty")


@_attrs_define
class GetZpoolsResponse200DetailZpoolsAdditionalProperty:
    """
    Attributes:
        create_time (datetime.datetime | Unset):
        last_scrub_time (datetime.datetime | None | Unset):
        username (str | Unset):
        volume_count (int | Unset):
        volumes (list[GetZpoolsResponse200DetailZpoolsAdditionalPropertyVolumesItem] | Unset):
    """

    create_time: datetime.datetime | Unset = UNSET
    last_scrub_time: datetime.datetime | None | Unset = UNSET
    username: str | Unset = UNSET
    volume_count: int | Unset = UNSET
    volumes: list[GetZpoolsResponse200DetailZpoolsAdditionalPropertyVolumesItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        create_time: str | Unset = UNSET
        if not isinstance(self.create_time, Unset):
            create_time = self.create_time.isoformat()

        last_scrub_time: None | str | Unset
        if isinstance(self.last_scrub_time, Unset):
            last_scrub_time = UNSET
        elif isinstance(self.last_scrub_time, datetime.datetime):
            last_scrub_time = self.last_scrub_time.isoformat()
        else:
            last_scrub_time = self.last_scrub_time

        username = self.username

        volume_count = self.volume_count

        volumes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.volumes, Unset):
            volumes = []
            for volumes_item_data in self.volumes:
                volumes_item = volumes_item_data.to_dict()
                volumes.append(volumes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if create_time is not UNSET:
            field_dict["CreateTime"] = create_time
        if last_scrub_time is not UNSET:
            field_dict["LastScrubTime"] = last_scrub_time
        if username is not UNSET:
            field_dict["Username"] = username
        if volume_count is not UNSET:
            field_dict["VolumeCount"] = volume_count
        if volumes is not UNSET:
            field_dict["Volumes"] = volumes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_zpools_response_200_detail_zpools_additional_property_volumes_item import (
            GetZpoolsResponse200DetailZpoolsAdditionalPropertyVolumesItem,
        )

        d = dict(src_dict)
        _create_time = d.pop("CreateTime", UNSET)
        create_time: datetime.datetime | Unset
        if isinstance(_create_time, Unset):
            create_time = UNSET
        else:
            create_time = isoparse(_create_time)

        def _parse_last_scrub_time(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_scrub_time_type_0 = isoparse(data)

                return last_scrub_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_scrub_time = _parse_last_scrub_time(d.pop("LastScrubTime", UNSET))

        username = d.pop("Username", UNSET)

        volume_count = d.pop("VolumeCount", UNSET)

        _volumes = d.pop("Volumes", UNSET)
        volumes: list[GetZpoolsResponse200DetailZpoolsAdditionalPropertyVolumesItem] | Unset = UNSET
        if _volumes is not UNSET:
            volumes = []
            for volumes_item_data in _volumes:
                volumes_item = GetZpoolsResponse200DetailZpoolsAdditionalPropertyVolumesItem.from_dict(
                    volumes_item_data
                )

                volumes.append(volumes_item)

        get_zpools_response_200_detail_zpools_additional_property = cls(
            create_time=create_time,
            last_scrub_time=last_scrub_time,
            username=username,
            volume_count=volume_count,
            volumes=volumes,
        )

        get_zpools_response_200_detail_zpools_additional_property.additional_properties = d
        return get_zpools_response_200_detail_zpools_additional_property

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
