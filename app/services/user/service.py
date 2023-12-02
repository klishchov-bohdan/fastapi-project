import datetime
import pickle

from fastapi import HTTPException, status, Depends
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import SECRET_KEY, ALGORITHM
from app.db_conn import get_async_session
from app.redis_conn import cache
from app.services.auth.constants import oauth_2_scheme
from app.services.auth.schemas import TokenDataSchema
from app.services.auth.service import validate_session
from app.services.auth.utils import get_password_hash, verify_password

from app.services.user.models import User
from app.services.user.schemas import UserSchema


async def get_user_by_username(username: str, session: AsyncSession):
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    first = result.first()
    if first is None:
        return
    user = first.User
    return user

async def get_user_by_id(id: int, session: AsyncSession):
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    first = result.first()
    if first is None:
        return
    user = first.User
    return user


async def is_admin_check(user: User):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Not enough permissions",
        )


async def get_current_user(security_scopes: SecurityScopes, session: AsyncSession = Depends(get_async_session), redis_client: cache = Depends(cache), token: str = Depends(oauth_2_scheme)) -> User:
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get('id')
        if id is None:
            raise credentials_exception
        if not await validate_session(token, session):
            redis_client.delete(f'profile_{id}')
            raise credentials_exception
        # username: str = payload.get('username')
        token_scopes = payload.get("scopes", [])
        token_data = TokenDataSchema(id=id, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception
    if (cached_profile := redis_client.get(f"profile_{token_data.id}")) is not None:
        # print(pickle.loads(cached_profile))
        return pickle.loads(cached_profile)
    user = await get_user_by_id(token_data.id, session)
    if user is None:
        redis_client.delete(f'profile_{token_data.id}')
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            redis_client.delete(f'profile_{token_data.id}')
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    redis_client.set(name=f"profile_{user.id}", value=pickle.dumps(user), ex=300)
    return user


async def registrate_user(username: str, email: str, password: str, session: AsyncSession):
    try:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        if result.first() is not None:
            return False
        new_user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            disabled=False,
            verified=False,
            is_admin=False
        )
        session.add(new_user)
        await session.commit()
        return new_user
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def delete_user(id: int, session: AsyncSession):
    try:
        user = await get_user_by_id(id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await session.delete(user)
        await session.commit()
        return user
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def update_email(id: int, email: str, session: AsyncSession):
    try:
        stmt = update(User).where(User.id == id).values(email=email)
        await session.execute(stmt)
        await session.commit()
        user = await get_user_by_id(id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def update_username(id: int, username: str, session: AsyncSession):
    try:
        stmt = update(User).where(User.id == id).values(username=username)
        await session.execute(stmt)
        await session.commit()
        user = await get_user_by_id(id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def update_password(id: int, password: str, new_password: str, session: AsyncSession):
    try:
        user = await get_user_by_id(id, session)
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
        stmt = update(User).where(User.id == id).values(hashed_password=get_password_hash(new_password))
        await session.execute(stmt)
        await session.commit()
        new_user = await get_user_by_id(id, session)
        if new_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return new_user
    except SQLAlchemyError as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

