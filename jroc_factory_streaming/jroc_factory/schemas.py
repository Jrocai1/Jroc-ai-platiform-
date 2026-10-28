from enum import StrEnum
from typing import Annotated, Literal, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints

SafeText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)]
IdText = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")]

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class AssetBasis(StrEnum):
    OWNED = "owned"
    AUTHORIZED = "authorized"
    OPEN_SOURCE = "open_source"
    PUBLIC_DOMAIN = "public_domain"

class AuthMessage(StrictModel):
    action: Literal["AUTH"]
    token: Annotated[str, StringConstraints(min_length=16, max_length=4096)]

class AssetIntake(StrictModel):
    asset_id: IdText
    name: SafeText
    source_url: HttpUrl | None = None
    legal_basis: AssetBasis
    license_spdx: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)] | None = None
    authorization_reference: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)] | None = None
    intended_use: SafeText
    preserves_attribution: bool = True
    bypasses_access_controls: bool = False
    removes_license_enforcement: bool = False
    contains_secrets: bool = False

class SubmitAsset(StrictModel):
    action: Literal["SUBMIT_ASSET"]
    request_id: IdText
    asset: AssetIntake

class ApproveAsset(StrictModel):
    action: Literal["APPROVE_ASSET"]
    request_id: IdText
    asset_id: IdText
    approver: SafeText

class DeployMission(StrictModel):
    action: Literal["DEPLOY_SALVAGE_MISSION"]
    request_id: IdText
    mission_id: IdText
    asset_id: IdText
    target_component: SafeText

class GetState(StrictModel):
    action: Literal["GET_STATE"]
    request_id: IdText

IncomingMessage = Annotated[Union[SubmitAsset, ApproveAsset, DeployMission, GetState], Field(discriminator="action")]

class Envelope(StrictModel):
    event: str
    request_id: str | None = None
    data: dict = Field(default_factory=dict)
