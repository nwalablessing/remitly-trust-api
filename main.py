from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import random

from database import FlaggedUser, SessionLocal

app = FastAPI(title="Remitly Trust Platform Demo")

class IdentityData(BaseModel):
    full_name: str
    date_of_birth: str
    id_number: str
    address: Optional[str] = None

@app.post("/verify/")
def verify_identity(data: IdentityData):
    trust_score = random.randint(60, 100)

    if len(data.id_number) < 5 or not data.id_number.isdigit():
        raise HTTPException(status_code=400, detail="Invalid ID number format")

    if trust_score < 70:
        # Log to database
        db = SessionLocal()
        flagged = FlaggedUser(
            full_name=data.full_name,
            id_number=data.id_number,
            trust_score=trust_score,
            message="Verification needs manual review"
        )
        db.add(flagged)
        db.commit()
        db.close()

        return {
            "status": "flagged",
            "message": "Verification needs manual review",
            "trust_score": trust_score
        }

    return {
        "status": "verified",
        "message": "Identity verified successfully",
        "trust_score": trust_score
    }
