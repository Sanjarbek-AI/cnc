from main.databases import database
from main.models import *


async def update_comp_all_status(message):
    try:
        query = competitions.update().values(
            status=CompetitionStatus.stopped,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_all_posts(message):
    try:
        query = user_post.update().values(
            status=UserPostStatus.disactive,
            updated_at=message.date
        ).where(user_post.c.status == UserPostStatus.accepted)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_image_uz(message, image):
    try:
        query = competitions.update().values(
            image_uz=image,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_image_ru(message, image):
    try:
        query = competitions.update().values(
            image_ru=image,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_conditions_uz(message, text):
    try:
        query = competitions.update().values(
            conditions_uz=text,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_conditions_ru(message, text):
    try:
        query = competitions.update().values(
            conditions_ru=text,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_gifts_image_uz(message, image):
    try:
        query = competitions.update().values(
            gifts_image_uz=image,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_gifts_image_ru(message, image):
    try:
        query = competitions.update().values(
            gifts_image_ru=image,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_gifts_uz(message, text):
    try:
        query = competitions.update().values(
            gifts_uz=text,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_comp_gifts_ru(message, text):
    try:
        query = competitions.update().values(
            gifts_ru=text,
            updated_at=message.date
        ).where(competitions.c.status == CompetitionStatus.active)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False
