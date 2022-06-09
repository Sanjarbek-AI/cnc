from aiogram.dispatcher.filters.state import State, StatesGroup


class Language(StatesGroup):
    select = State()


class AddCompetition(StatesGroup):
    image_uz = State()
    image_ru = State()
    conditions_uz = State()
    conditions_ru = State()
    gifts_uz = State()
    gifts_ru = State()
    gifts_image_uz = State()
    gifts_image_ru = State()


class AddContact(StatesGroup):
    image_uz = State()
    image_ru = State()
    contact_uz = State()
    contact_ru = State()


class SendPost(StatesGroup):
    image_or_file = State()
    image = State()
    file = State()
    text = State()
    text_wait = State()
    link = State()
    button_text = State()
    waiting = State()


class UpdateContact(StatesGroup):
    image_uz = State()
    image_ru = State()
    contact_uz = State()
    contact_ru = State()


class UpdateCompetition(StatesGroup):
    image_uz = State()
    image_ru = State()
    conditions_uz = State()
    conditions_ru = State()
    gifts_uz = State()
    gifts_ru = State()
    gifts_image_uz = State()
    gifts_image_ru = State()


class UpdateShowroom(StatesGroup):
    image_uz = State()
    image_ru = State()
    info_uz = State()
    info_ru = State()
    name_uz = State()
    name_ru = State()
    link = State()


class AddShowroom(StatesGroup):
    image_uz = State()
    image_ru = State()
    info_uz = State()
    info_ru = State()
    name_uz = State()
    name_ru = State()
    link = State()


class AddDealer(StatesGroup):
    image_uz = State()
    image_ru = State()
    info_uz = State()
    info_ru = State()
    name_uz = State()
    name_ru = State()
    link = State()


class UpdateProfile(StatesGroup):
    full_name = State()
    phone_number = State()
    location = State()
    language = State()
