from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db_conn import get_async_session
from app.services.auth.schemas import TokenSchema
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth.service import authenticate_user, get_session_by_client, create_session, validate_session, \
    logout_current_user
from app.services.auth.utils import create_access_token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/token', response_model=TokenSchema)
async def authenticate(form_data: OAuth2PasswordRequestForm = Depends(),
                       session: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'WWW-Authenticate': 'Bearer'})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Account disabled',
                            headers={'WWW-Authenticate': 'Bearer'})
    user_session = await get_session_by_client(form_data.client_id, session)
    if user_session:
        if await validate_session(user_session.token, session) and user_session.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='This client already have a session. Logout first',
                                headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'id': user.id, 'client_id': form_data.client_id, "scopes": form_data.scopes},
        expires_delta=access_token_expires)
    expires_in = datetime.utcnow() + access_token_expires
    new_session = await create_session(user_id=user.id, token=access_token, client_unique_string=form_data.client_id,
                                       expires_in=int(expires_in.timestamp()), session=session)
    return {'access_token': new_session.token, 'token_type': 'bearer'}


@router.post('/logout')
async def authenticate(client_id=Security(logout_current_user, scopes=["me", "admin"])):
    return {'client_id: ': client_id}
