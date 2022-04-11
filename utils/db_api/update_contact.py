from main.databases import database
from main.models import *


async def update_contact_image_uz(message, image):
    try:
        query = contacts.update().values(
            image_uz=image,
            updated_at=message.date
        ).where(contacts.c.status == True)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_contact_image_ru(message, image):
    try:
        query = contacts.update().values(
            image_ru=image,
            updated_at=message.date
        ).where(contacts.c.status == True)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_contact_contact_uz(message, contact):
    try:
        query = contacts.update().values(
            contact_uz=contact,
            updated_at=message.date
        ).where(contacts.c.status == True)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_contact_contact_ru(message, contact):
    try:
        query = contacts.update().values(
            contact_ru=contact,
            updated_at=message.date
        ).where(contacts.c.status == True)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False
