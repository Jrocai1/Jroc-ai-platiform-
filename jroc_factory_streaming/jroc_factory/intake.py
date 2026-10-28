from dataclasses import dataclass
from .schemas import AssetBasis, AssetIntake

COMPATIBLE_LICENSES={"MIT","Apache-2.0","BSD-2-Clause","BSD-3-Clause","ISC","MPL-2.0","Unlicense","CC0-1.0"}

@dataclass(frozen=True)
class Decision:
    accepted: bool
    state: str
    reasons: list[str]
    required_actions: list[str]

def evaluate(asset: AssetIntake) -> Decision:
    reasons=[]; actions=[]
    if asset.bypasses_access_controls: reasons.append("Access-control bypass is prohibited.")
    if asset.removes_license_enforcement: reasons.append("License-enforcement removal is prohibited.")
    if asset.contains_secrets: reasons.append("Secrets must be removed and rotated before intake.")
    if not asset.preserves_attribution: reasons.append("Attribution and license notices must be preserved.")
    if asset.legal_basis == AssetBasis.OPEN_SOURCE:
        if not asset.license_spdx: reasons.append("An SPDX license identifier is required.")
        elif asset.license_spdx not in COMPATIBLE_LICENSES: reasons.append("License requires manual legal compatibility review.")
    if asset.legal_basis in {AssetBasis.OWNED, AssetBasis.AUTHORIZED} and not asset.authorization_reference:
        reasons.append("Ownership or authorization evidence is required.")
    if reasons: return Decision(False,"REJECTED",reasons,[])
    actions=["Verify provenance and artifact hash.","Scan dependencies, malware, secrets, and vulnerabilities.","Preserve license and attribution files.","Obtain human approval before integration."]
    return Decision(True,"PENDING_APPROVAL",["Automated policy checks passed."],actions)
