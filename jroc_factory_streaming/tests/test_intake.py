from jroc_factory.intake import evaluate
from jroc_factory.schemas import AssetIntake

def test_open_source_asset_enters_approval():
    a=AssetIntake(asset_id="x",name="x",legal_basis="open_source",license_spdx="MIT",intended_use="test")
    assert evaluate(a).state=="PENDING_APPROVAL"

def test_bypass_is_rejected():
    a=AssetIntake(asset_id="x",name="x",legal_basis="public_domain",intended_use="test",bypasses_access_controls=True)
    assert evaluate(a).state=="REJECTED"

def test_owned_requires_evidence():
    a=AssetIntake(asset_id="x",name="x",legal_basis="owned",intended_use="test")
    assert evaluate(a).state=="REJECTED"
