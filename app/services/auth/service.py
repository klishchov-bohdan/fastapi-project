import pickle
import uuid

from fastapi import HTTPException, status, Depends
from fastapi.security import SecurityScopes
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.config import SECRET_KEY, ALGORITHM
from app.db_conn import get_async_session
from app.redis_conn import cache
from app.services.auth.constants import oauth_2_scheme
from app.services.auth.models import Session
from app.services.auth.schemas import TokenDataSchema
from app.services.auth.utils import verify_password
from app.services.user.models import User


async def authenticate_user(username: str, password: str, session: AsyncSession):
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    first_user = result.first()
    if first_user is None:
        return False
    user = first_user.User
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_session_by_client(client_unique_string: str, session:AsyncSession):
    query = select(Session).where(Session.client_unique_string == client_unique_string)
    result = await session.execute(query)
    first_session = result.first()
    if first_session is None:
        return False
    return first_session.Session


async def delete_session_if_exists(session_id: uuid.UUID, session: AsyncSession):
    query = select(Session).where(Session.id == session_id)
    result = await session.execute(query)
    first_session = result.first()
    if first_session is not None:
        await session.delete(first_session.Session)
        await session.commit()


async def delete_session_by_token_if_exists(token: str, session: AsyncSession):
    query = select(Session).where(Session.token == token)
    result = await session.execute(query)
    first_session = result.first()
    if first_session is not None:
        await session.delete(first_session.Session)
        await session.commit()


async def validate_session(token: str, session: AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get('id')
        client_id: str = payload.get('client_id')
        if id is None or client_id is None:
            raise credentials_exception
        client_session = await get_session_by_client(client_unique_string=client_id, session=session)
        if not client_session:
            raise credentials_exception
        if client_session.expires_in <= int(datetime.utcnow().timestamp()):
            await delete_session_if_exists(session_id=client_session.id, session=session)
            return False
        if token != client_session.token:
            await delete_session_if_exists(session_id=client_session.id, session=session)
            return False
        return client_session
    except (JWTError, ValidationError):
        await delete_session_by_token_if_exists(token, session)
        return False


async def create_session(user_id: int, token: str, client_unique_string: str, expires_in: int, session: AsyncSession):
    try:
        query = select(Session).where(Session.client_unique_string == client_unique_string)
        result = await session.execute(query)
        first_session = result.first()
        if first_session is not None and user_id == first_session.Session.user_id:
            old_session = first_session.Session
            stmt = update(Session).where(Session.id == old_session.id).values(token=token, expires_in=expires_in)
            await session.execute(stmt)
            await session.commit()
            old_session.token = token
            old_session.expires_in = expires_in
            return old_session

        new_session = Session(
            id=uuid.uuid4(),
            user_id=user_id,
            token=token,
            client_unique_string=client_unique_string,
            expires_in=expires_in
        )
        session.add(new_session)
        await session.commit()
        return new_session
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def logout_current_user(security_scopes: SecurityScopes, session: AsyncSession = Depends(get_async_session), redis_client: cache = Depends(cache), token: str = Depends(oauth_2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        if not await validate_session(token, session):
            raise credentials_exception
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get('id')
        client_id: str = payload.get('client_id')
        if id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenDataSchema(id=id, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    await delete_session_by_token_if_exists(token, session)
    deleted_session = await get_session_by_client(client_id, session)
    if deleted_session:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong when logout",
                headers={"WWW-Authenticate": authenticate_value},
            )
    redis_client.delete(f'profile_{token_data.id}')
    return client_id
