from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.notes.schemas import NoteCreate, NoteUpdate, NoteGet
from src.notes.services import create_note, update_note, delete_note, get_notes, get_note_by_id
from src.dependencies import async_session
from src.auth.dependencies import current_user, get_user_id_from_jwt
from src.utils.status import auth_status, update_status, delete_status


auth_scheme = HTTPBearer(auto_error=False)

router = APIRouter(prefix='/notes', tags=['notes'])


@router.post('',
             status_code=status.HTTP_201_CREATED,
             responses={**auth_status},
             response_model=NoteGet
             )
async def create(body: NoteCreate, user: current_user, session: async_session):
    """Create Note"""
    return await create_note(user.id, body, session)


@router.patch('/{note_id}',
              status_code=status.HTTP_204_NO_CONTENT,
              responses={**auth_status, **update_status})
async def update(note_id: int, body: NoteUpdate, user: current_user, session: async_session):
    return await update_note(note_id, user.id, body, session)


@router.delete('/{note_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               responses={**auth_status, **delete_status})
async def delete(note_id: int, user: current_user, session: async_session):
    return await delete_note(note_id, user.id, session)


@router.get('',
            status_code=status.HTTP_200_OK,
            response_model=list[NoteGet])
async def find_all(session: async_session):
    """Get All Notes"""
    return await get_notes(session)


@router.get('/{note_id}',
            response_model=NoteGet,
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_403_FORBIDDEN: auth_status.get(status.HTTP_403_FORBIDDEN),
                status.HTTP_404_NOT_FOUND: {
                    'description': 'Note not found',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'detail': 'string'
                                }
                            }
                        }
                    }
                },
            })
async def get_note(note_id: int,
                   session: async_session,
                   token: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]):
    user_id = None
    if token:
        user_id = await get_user_id_from_jwt(token.credentials)
    return await get_note_by_id(note_id, user_id, session)
