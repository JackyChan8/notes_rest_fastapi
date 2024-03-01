from fastapi import HTTPException, status

from sqlalchemy import insert, select, update, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.notes.models import Note
from src.notes.schemas import NoteCreate, NoteUpdate, NoteGet


async def create_note(user_id: int, note: NoteCreate, session: AsyncSession) -> NoteGet:
    """Create Note By User"""
    query = insert(Note).values(text=note.text, author_id=user_id).returning(Note)
    note_db = await session.scalar(query, execution_options={'synchronize_session': 'fetch'})
    session.add(note_db)
    await session.commit()
    await session.refresh(note_db)
    return NoteGet(
        id=note_db.id,
        text=note_db.text,
        is_published=note_db.is_published,
        author_id=note_db.author_id,
        created_at=note_db.created_at,
    )


async def update_note(note_id: int, user_id: int, note: NoteUpdate, session: AsyncSession):
    """Update Note"""
    note = note.dict(exclude_none=True)
    query = select(exists(Note.id).where(Note.id == note_id, Note.author_id == user_id))
    is_author = await session.execute(query)
    if not is_author.scalar():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t update a note that isn\'t yours')
    if not note:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Fill in the field to change the note')
    note = await session.scalar(
        update(Note).where(Note.id == note_id).values(**note).returning(Note),
        execution_options={'synchronize_session': 'fetch'}
    )
    session.add(note)
    await session.commit()
    await session.refresh(note)


async def delete_note(note_id: int, user_id: int, session: AsyncSession):
    """Delete Note"""
    query = select(exists(Note.id).where(Note.id == note_id, Note.author_id == user_id))
    is_author = await session.execute(query)
    if not is_author.scalar():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can\'t delete a note that isn\'t yours')

    note = await session.scalar(select(Note).where(Note.id == note_id))
    await session.delete(note)
    await session.commit()


async def get_notes(session: AsyncSession):
    """Get All notes published"""
    notes = await session.execute(select(Note).where(Note.is_published == True))
    notes = notes.scalars().all()
    return notes


async def get_note_by_id(note_id: int, user_id: int | None, session: AsyncSession) -> Note:
    """Get Not by ID"""
    note = await session.scalar(select(Note).where(Note.id == note_id))
    if note:
        if note.is_published:
            return note

        if user_id:
            if note.author_id == int(user_id):
                return note

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authenticated')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
