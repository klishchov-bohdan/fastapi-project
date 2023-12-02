import random

from fastapi import APIRouter, HTTPException, Security, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_conn import get_async_session
from app.redis_conn import cache
from app.services.user.models import User
from app.services.user.schemas import UserSchema, UserRegistrationForm, UserNameUpdateForm, UserEmailUpdateForm, \
    UserPasswordUpdateForm
from app.services.user.service import get_current_user, get_user_by_id, registrate_user, delete_user, update_email, \
    update_username, update_password, is_admin_check
from app.tasks.tasks import send_email_verification_code

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/registrate', response_model=UserSchema)
async def registrate(form_data: UserRegistrationForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    new_user = await registrate_user(form_data.username, form_data.email, form_data.password, session)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Can`t registrate user',
                            headers={'WWW-Authenticate': 'Bearer'})
    return UserSchema(id=new_user.id, email=new_user.email, username=new_user.username, disabled=new_user.disabled)


@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Security(get_current_user, scopes=["me"])):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return UserSchema(id=current_user.id, username=current_user.username, email=current_user.email,
                      disabled=current_user.disabled, verified=current_user.verified, is_admin=current_user.is_admin)


@router.get("/{id}", response_model=UserSchema)
async def read_user(id: int, current_user: User = Security(get_current_user, scopes=["me", "admin"]), session: AsyncSession = Depends(get_async_session)):
    await is_admin_check(current_user)
    user = await get_user_by_id(id, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserSchema(id=user.id, username=user.username, email=user.email,
                      disabled=user.disabled, verified=user.verified, is_admin=user.is_admin)


@router.delete("/{id}", response_model=UserSchema)
async def delete_user_by_id(id: int, current_user: User = Security(get_current_user, scopes=["me", "admin"]), session: AsyncSession = Depends(get_async_session)):
    await is_admin_check(current_user)
    user = await delete_user(id, session)
    return UserSchema(id=user.id, username=user.username, email=user.email,
                      disabled=user.disabled, verified=user.verified, is_admin=user.is_admin)


@router.patch("/me/email", response_model=UserSchema)
async def update_my_email(email: UserEmailUpdateForm = Depends(), current_user: UserSchema = Security(get_current_user, scopes=["me"]), redis_client: cache = Depends(cache), session: AsyncSession = Depends(get_async_session)):
    if current_user.email == email:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="New email is equal current email")
    user = await update_email(current_user.id, email.new_email, session)
    redis_client.delete(f'profile_{user.id}')
    return UserSchema(id=user.id, username=user.username, email=user.email,
                      disabled=user.disabled, verified=user.verified, is_admin=user.is_admin)


@router.patch("/me/send-verification-code")
async def send_verification_code(current_user: UserSchema = Security(get_current_user, scopes=["me"]), redis_client: cache = Depends(cache), session: AsyncSession = Depends(get_async_session)):
    try:
        code = random.randint(100000, 999999)
        send_email_verification_code.delay(current_user.email, code)
        redis_client.set(f'code_{current_user.id}', str(code), 300)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can`t send verification code")
    return {'status_code': status.HTTP_200_OK, 'message': 'code send'}


@router.patch("/me/username", response_model=UserSchema)
async def update_my_username(username: UserNameUpdateForm = Depends(), current_user: UserSchema = Security(get_current_user, scopes=["me"]), redis_client: cache = Depends(cache), session: AsyncSession = Depends(get_async_session)):
    if current_user.username == username:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="New username is equal username email")
    user = await update_username(current_user.id, username.new_username, session)
    redis_client.delete(f'profile_{user.id}')
    return UserSchema(id=user.id, username=user.username, email=user.email,
                      disabled=user.disabled, verified=user.verified, is_admin=user.is_admin)


@router.patch("/me/password", response_model=UserSchema)
async def update_my_password(password: UserPasswordUpdateForm = Depends(), current_user: UserSchema = Security(get_current_user, scopes=["me"]), redis_client: cache = Depends(cache), session: AsyncSession = Depends(get_async_session)):
    if password.password == password.new_password:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="The passwords can`t be equal")
    user = await update_password(current_user.id, password.password, password.new_password, session)
    redis_client.delete(f'profile_{user.id}')
    return UserSchema(id=user.id, username=user.username, email=user.email,
                      disabled=user.disabled, verified=user.verified, is_admin=user.is_admin)
