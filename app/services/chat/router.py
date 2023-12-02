import uuid

from fastapi import APIRouter, Security, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_conn import get_async_session
from app.services.chat.constants import GPT_MESSAGE_TEMPLATE
from app.services.chat.models import Chat
from app.services.chat.schemas import SendingMessage, AnswerMessage
from app.services.user.models import User
from app.services.user.service import get_current_user
import g4f

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)


@router.post('/get-gpt-answer')
async def get_gpt_answer(message: SendingMessage = Depends(), current_user: User = Security(get_current_user, scopes=["me", "chat"]), session: AsyncSession = Depends(get_async_session)):
    response = ''
    ctr = 3
    while len(response) == 0 or message.message in response:
        response = await g4f.ChatCompletion.create_async(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": GPT_MESSAGE_TEMPLATE + message.message}],
        )
        ctr = ctr - 1
        if ctr == 0:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cant choose the method")
        session.add(Chat(
            id=uuid.uuid4(),
            user_id=current_user.id,
            message=message.message,
            gpt_answer=response
        ))
        await session.commit()
    return AnswerMessage(user_id=current_user.id, message=response)
