from fastapi import APIRouter, Depends, HTTPException
from ..auth import verify_token
from .. import db

router = APIRouter(prefix="/config", tags=["config"])

PROFILES = {
    "sap_ecc": {
        "name": "SAP ECC 6.0",
        "description": "SAP ECC 6.0 EHP8 — legacy system with 15+ years of accumulated data",
    },
    "oracle_ebs": {
        "name": "Oracle E-Business Suite",
        "description": "Oracle E-Business Suite 12.2.10",
    },
    "dynamics_ax": {
        "name": "Microsoft Dynamics AX",
        "description": "Microsoft Dynamics AX 2012 R3",
    },
    "generic": {
        "name": "Generic Legacy ERP",
        "description": "Generic legacy ERP — simplified flat schema",
    },
}


@router.get("/profiles", dependencies=[Depends(verify_token)])
async def list_profiles():
    return [
        {
            "id": pid,
            "name": meta["name"],
            "description": meta["description"],
            "active": pid == db.active_profile_id,
        }
        for pid, meta in PROFILES.items()
    ]


@router.post("/profiles/{profile_id}/activate", dependencies=[Depends(verify_token)])
async def activate_profile(profile_id: str):
    if profile_id not in PROFILES:
        raise HTTPException(404, f"Profile {profile_id} not found")

    if profile_id == "sap_ecc":
        from ..profiles.sap_ecc import SapEccProfile
        new_profile = SapEccProfile()
    elif profile_id == "oracle_ebs":
        from ..profiles.oracle_ebs import OracleEbsProfile
        new_profile = OracleEbsProfile()
    elif profile_id == "dynamics_ax":
        from ..profiles.dynamics_ax import DynamicsAxProfile
        new_profile = DynamicsAxProfile()
    else:
        from ..profiles.generic import GenericProfile
        new_profile = GenericProfile()

    if db.current_profile is not None:
        await db.current_profile.drop_tables(db.engine)
    await new_profile.create_tables(db.engine)
    await new_profile.seed_data(db.engine)

    db.active_profile_id = profile_id
    db.current_profile = new_profile

    return {"activated": profile_id, "tables": new_profile.get_tables()}
