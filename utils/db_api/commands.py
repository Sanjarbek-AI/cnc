from main.databases import database
from main.models import *


async def get_user(telegram_id):
    try:
        query = users.select().where(users.c.telegram_id == telegram_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_users_list(id_list):
    try:
        query = users.select().where(users.c.telegram_id in id_list)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_users():
    try:
        query = users.select().where(users.c.status == UserStatus.active)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_top_users():
    try:
        query = posts_and_like.select().where().order_by('like')
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_users_status_false():
    try:
        query = users.select().where(users.c.status == UserStatus.inactive)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def register(message, state):
    try:
        data = await state.get_data()
        query = users.insert().values(
            telegram_id=data.get("telegram_id"),
            full_name=data.get("full_name"),
            location=data.get("location"),
            language=data.get("language"),
            phone_number=data.get("phone_number"),
            status=UserStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def register_start(message):
    try:
        query = users.insert().values(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            language="uz",
            status=UserStatus.inactive,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_competitions():
    try:
        query = competitions.select().where(competitions.c.status == CompetitionStatus.active)
        comp = await database.fetch_one(query=query)
        return comp
    except Exception as exc:
        print(exc)
        return False


async def get_showrooms():
    try:
        query = showrooms.select().where(showrooms.c.status == ShowroomStatus.active,
                                         showrooms.c.type == ShowroomType.showroom)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_dealers():
    try:
        query = showrooms.select().where(showrooms.c.status == ShowroomStatus.active,
                                         showrooms.c.type == ShowroomType.dealer)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_showroom(showroom_id):
    try:
        query = showrooms.select().where(showrooms.c.id == showroom_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_dealer(dealer_id):
    try:
        query = showrooms.select().where(showrooms.c.id == dealer_id, showrooms.c.type == ShowroomType.dealer)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_contact():
    try:
        query = contacts.select().where(contacts.c.status == ContactStatus.active)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def add_contact(message, state):
    try:
        data = await state.get_data()
        query = contacts.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            contact_uz=data.get("contact_uz"),
            contact_ru=data.get("contact_ru"),
            status=ContactStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def add_comp(message, state):
    try:
        data = await state.get_data()
        query = competitions.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            conditions_uz=data.get("conditions_uz"),
            conditions_ru=data.get("conditions_ru"),
            gifts_image_uz=data.get("gifts_image_uz"),
            gifts_image_ru=data.get("gifts_image_ru"),
            gifts_uz=data.get("gifts_uz"),
            gifts_ru=data.get("gifts_ru"),
            status=CompetitionStatus.deleted,
            created_at=message.date,
            updated_at=message.date
        )
        return await database.execute(query=query)
    except Exception as exc:
        print(exc)
        return False


async def update_comp_status(message, comp_id):
    try:
        query = competitions.update().values(
            status=CompetitionStatus.active,
            updated_at=message.date
        ).where(competitions.c.id == comp_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def add_showroom(message, state):
    try:
        data = await state.get_data()
        query = showrooms.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            info_uz=data.get("info_uz"),
            info_ru=data.get("info_ru"),
            name_uz=data.get("name_uz"),
            name_ru=data.get("name_ru"),
            location_link=data.get("link"),
            status=ShowroomStatus.active,
            type=ShowroomType.showroom,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def add_dealer(message, state):
    try:
        data = await state.get_data()
        query = showrooms.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            info_uz=data.get("info_uz"),
            info_ru=data.get("info_ru"),
            name_uz=data.get("name_uz"),
            name_ru=data.get("name_ru"),
            location_link=data.get("link"),
            status=ShowroomStatus.active,
            type=ShowroomType.dealer,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False
