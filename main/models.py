import sqlalchemy
from sqlalchemy import DateTime

from main.databases import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("full_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("location", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("language", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("telegram_id", sqlalchemy.BigInteger),
    sqlalchemy.Column("phone_number", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)

competitions = sqlalchemy.Table(
    "competitions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("code", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("conditions_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("conditions_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("gifts_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("gifts_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("gifts_image_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("gifts_image_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)

contacts = sqlalchemy.Table(
    "contacts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("contact_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("contact_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)

showrooms = sqlalchemy.Table(
    "showrooms",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("info_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("name_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("name_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("location_link", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)


posts_and_like = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("like", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("telegram_id", sqlalchemy.BigInteger, nullable=True),
    sqlalchemy.Column("user_post_id", sqlalchemy.Integer, nullable=True),
)

user_post = sqlalchemy.Table(
    "user_post",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("comp_id", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("telegram_id", sqlalchemy.BigInteger, nullable=True),
    sqlalchemy.Column("images", sqlalchemy.JSON, nullable=True),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)
