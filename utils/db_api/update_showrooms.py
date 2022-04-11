from main.databases import database
from main.models import *


async def update_showroom_image_uz(message, image, sh_id):
    try:
        query = showrooms.update().values(
            image_uz=image,
            updated_at=message.date
        ).where(showrooms.c.id == sh_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_showroom_image_ru(message, image, sh_id):
    try:
        query = showrooms.update().values(
            image_ru=image,
            updated_at=message.date
        ).where(showrooms.c.id == sh_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_showroom_info_uz(message, info, sh_id):
    try:
        query = showrooms.update().values(
            info_uz=info,
            updated_at=message.date
        ).where(showrooms.c.id == sh_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_showroom_info_ru(message, info, sh_id):
    try:
        query = showrooms.update().values(
            info_ru=info,
            updated_at=message.date
        ).where(showrooms.c.id == sh_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_showroom_name_uz(message, name, sh_id):
    try:
        query = showrooms.update().values(
            name_uz=name,
            updated_at=message.date
        ).where(showrooms.c.id == sh_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_showroom_name_ru(message, name, sh_id):
    try:
        query = showrooms.update().values(
            name_ru=name,
            updated_at=message.date
        ).where(showrooms.c.id == sh_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_showroom_link(message, link, sh_id):
    try:
        query = showrooms.update().values(
            location_link=link,
            updated_at=message.date
        ).where(showrooms.c.id == sh_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False
