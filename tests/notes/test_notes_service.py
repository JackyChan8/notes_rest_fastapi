from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, exists

from src.notes import services
from src.notes.models import Note
from src.notes.schemas import NoteCreate, NoteUpdate
from tests.auth.test_auth_service import test_create_user, get_user


class NoteTest:
    text = 'My Testing Note'
    is_published = True


async def get_note(db_session: AsyncSession) -> Note:
    note = await db_session.scalar(select(Note))
    return note


async def check_update(note: Note, note_update: NoteUpdate):
    note_dict = note.__dict__
    note_update_dict = note_update.dict(exclude_none=True)

    for field in note_update_dict.keys():
        assert note_dict.get(field) == note_update_dict.get(field)


async def update_note(db_session: AsyncSession, update_field='all'):
    change_note_text = 'My Testing Note Update'
    is_published = True

    await test_create_note(db_session)
    user_created = await get_user(db_session)
    note = await get_note(db_session)
    note_in = None

    match update_field:
        case 'all':
            note_in = NoteUpdate(text=change_note_text, is_published=is_published)
        case 'text':
            note_in = NoteUpdate(text=change_note_text)
        case 'published':
            note_in = NoteUpdate(is_published=is_published)
        case _:
            pass

    await services.update_note(note.id, user_created.id, note_in, db_session)

    # Check Update Text
    if note_in:
        updated_note = await get_note(db_session)
        await check_update(updated_note, note_in)


async def test_create_note(db_session: AsyncSession):
    await test_create_user(db_session)
    user_created = await get_user(db_session)
    note_in = NoteCreate(text=NoteTest.text)

    note = await services.create_note(user_created.id, note_in, db_session)
    assert note.id


async def test_update_note_all(db_session: AsyncSession):
    await update_note(db_session, update_field='all')


async def test_update_note_only_text(db_session: AsyncSession):
    await update_note(db_session, update_field='text')


async def test_update_note_only_published(db_session: AsyncSession):
    await update_note(db_session, update_field='published')


async def test_delete_note(db_session: AsyncSession):
    await test_create_note(db_session)

    user_created = await get_user(db_session)
    note = await get_note(db_session)

    await services.delete_note(note.id, user_created.id, db_session)

    # Check Delete Note
    is_exist_note = await db_session.scalar(select(exists(Note.id).where(Note.id == note.id)))
    assert is_exist_note is False


async def test_get_notes(db_session: AsyncSession):
    await test_create_user(db_session)
    notes = [NoteCreate(text='My Testing Note 1'), NoteCreate(text='My Testing Note 2')]

    # Create Notes
    query = insert(Note).values([{'text': note.text, 'is_published': True} for note in notes]).returning(Note)
    notes_db = await db_session.scalars(query, execution_options={'synchronize_session': 'fetch'})
    for note in notes_db.all():
        db_session.add(note)
    await db_session.commit()

    # Check Count Get Notes
    notes_check = await services.get_notes(db_session)
    assert len(notes_check) == len(notes)

    # Check Text Notes
    for note_create, note_scheme in zip(notes_check, notes):
        assert note_create.text == note_scheme.text
