from main.databases import database
from main.models import *


async def add_posts(message, state):
    try:
        data = await state.get_data()
        query = user_post.insert().values(
            comp_id=data.get("comp_id"),
            telegram_id=message.from_user.id,
            images=data.get("images"),
            description=data.get("text"),
            status=UserPostStatus.unaccepted,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_comp_user(telegram_id, comp_id):
    try:
        query = user_post.select().where(user_post.c.telegram_id == telegram_id, user_post.c.comp_id == comp_id)
        post = await database.fetch_one(query=query)
        return post
    except Exception as exc:
        print(exc)
        return False


async def get_user_post(post_id):
    try:
        query = user_post.select().where(user_post.c.id == post_id, user_post.c.status == UserPostStatus.accepted)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_user_post_by_id(post_id):
    try:
        query = user_post.select().where(user_post.c.id == post_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def delete_user_post_admin_no(post_id):
    try:
        query = user_post.delete().where(user_post.c.id == post_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_user_post_like(post_id):
    try:
        query = posts_and_like.select().where(posts_and_like.c.user_post_id == post_id,
                                              user_post.c.status == UserPostStatus.accepted)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_post_like(post_id):
    try:
        query = posts_and_like.select().where(posts_and_like.c.user_post_id == post_id)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_user_liked_or_not(post_id, tg_id):
    try:
        query = posts_and_like.select().where(posts_and_like.c.user_post_id == post_id,
                                              posts_and_like.c.telegram_id == tg_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def delete_user_post_like(post_id, user_id):
    try:
        query = posts_and_like.delete().where(
            posts_and_like.c.user_post_id == post_id, posts_and_like.c.telegram_id == user_id
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def add_user_post_like(post_id, user_id):
    try:
        query = posts_and_like.insert().values(
            user_post_id=post_id,
            telegram_id=user_id,
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_all_posts(comp_id):
    try:
        query = user_post.select().where(user_post.c.comp_id == comp_id)
        all_post = await database.fetch_all(query=query)
        return all_post
    except Exception as exc:
        print(exc)
        return False


async def get_all_posts_users(comp_id):
    try:
        query = user_post.select().where(user_post.c.comp_id == comp_id, user_post.c.status == UserPostStatus.accepted)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def update_user_post_status(message, post_id):
    try:
        query = user_post.update().values(
            status=UserPostStatus.accepted,
            updated_at=message.date
        ).where(user_post.c.id == post_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_user_active_comp_post(telegram_id, comp_id):
    try:
        query = user_post.select().where(user_post.c.comp_id == comp_id,
                                         user_post.c.telegram_id == telegram_id,
                                         user_post.c.status == UserPostStatus.accepted)
        post = await database.fetch_one(query=query)
        return post
    except Exception as exc:
        print(exc)
        return False
