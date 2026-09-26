import datetime
from sqlalchemy import Select
from sqlalchemy.orm import Session
from src.models.refresh_token import RefreshToken

def create_refresh_token(db:Session, refresh_token_hash:str, user_id:int, expires_at: datetime.datetime):
    refresh_token = RefreshToken(
        token_hash = refresh_token_hash,
        user_id = user_id,
        expires_at = expires_at
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token

def get_refresh_token_by_hash(db: Session, refresh_token_hash:str) -> RefreshToken | None:
    statement = Select(RefreshToken).where(
        RefreshToken.token_hash == refresh_token_hash
    )

    return db.scalar(statement)

def revoke_refresh_token(db:Session, refresh_token:RefreshToken):
    refresh_token.revoked_at = datetime.datetime.now(datetime.timezone.utc)

    db.commit()
    db.refresh(refresh_token)

    return refresh_token