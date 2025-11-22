from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetJobJobIdResponse200Detail")


@_attrs_define
class GetJobJobIdResponse200Detail:
    """
    Attributes:
        error (str | Unset): Error message if failed
        job_id (str | Unset):
        progress (int | Unset): Progress percentage
        status (str | Unset):
    """

    error: str | Unset = UNSET
    job_id: str | Unset = UNSET
    progress: int | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        job_id = self.job_id

        progress = self.progress

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if progress is not UNSET:
            field_dict["progress"] = progress
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error", UNSET)

        job_id = d.pop("job_id", UNSET)

        progress = d.pop("progress", UNSET)

        status = d.pop("status", UNSET)

        get_job_job_id_response_200_detail = cls(
            error=error,
            job_id=job_id,
            progress=progress,
            status=status,
        )

        get_job_job_id_response_200_detail.additional_properties = d
        return get_job_job_id_response_200_detail

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
