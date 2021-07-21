from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..callbacks import checklist_cb


async def make_checklist_keyboard(drink: int = 0, eat: int = 0,
                                  weapon: int = 0, ammo: int = 0,
                                  helm: int = 0, armor: int = 0, headphones: int = 0,
                                  first_aid: int = 0, bandage: int = 0, splint: int = 0, tourniquet: int = 0,
                                  night_raid: int = 0, nv: int = 0, lamp: int = 0,
                                  to_raid: int = 0) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    if drink == 0:
        drink_t = 'Попил?'
    else:
        drink_t = '\U00002705Попил'
    drink_b = InlineKeyboardButton(
        text=drink_t,
        callback_data=checklist_cb.new(
            f'1{eat}{weapon}{ammo}{helm}{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    if eat == 0:
        eat_t = 'Поел?'
    else:
        eat_t = '\U00002705Поел'
    eat_b = InlineKeyboardButton(
        text=eat_t,
        callback_data=checklist_cb.new(
            f'{drink}1{weapon}{ammo}{helm}{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    markup.add(drink_b, eat_b)
    if weapon == 0:
        weapon_t = 'Оружие'
    else:
        weapon_t = '\U00002705Оружие'
    weapon_b = InlineKeyboardButton(
        text=weapon_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}1{ammo}{helm}{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    if ammo == 0:
        ammo_t = 'Боеприпасы'
    else:
        ammo_t = '\U00002705Боеприпасы'
    ammo_b = InlineKeyboardButton(
        text=ammo_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}1{helm}{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    markup.add(weapon_b, ammo_b)
    if helm == 0:
        helm_t = 'Шлем'
    else:
        helm_t = '\U00002705Шлем'
    helm_b = InlineKeyboardButton(
        text=helm_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}{ammo}1{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    if armor == 0:
        armor_t = 'Броня'
    else:
        armor_t = '\U00002705Броня'
    armor_b = InlineKeyboardButton(
        text=armor_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}{ammo}{helm}1{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    if headphones == 0:
        headphones_t = 'Уши'
    else:
        headphones_t = '\U00002705Уши'
    headphones_b = InlineKeyboardButton(
        text=headphones_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}{ammo}{helm}{armor}1{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )

    markup.add(helm_b, armor_b, headphones_b)

    if first_aid == 0:
        first_aid_t = 'Аптечка'
    else:
        first_aid_t = '\U00002705Аптечка'
    first_aid_b = InlineKeyboardButton(
        text=first_aid_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}{ammo}{helm}{armor}{headphones}1{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    if bandage == 0:
        bandage_t = 'Бинт'
    else:
        bandage_t = '\U00002705Бинт'
    bandage_b = InlineKeyboardButton(
        text=bandage_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}{ammo}{helm}{armor}{headphones}{first_aid}1{splint}{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    if splint == 0:
        splint_t = 'Шина'
    else:
        splint_t = '\U00002705Шина'
    splint_b = InlineKeyboardButton(
        text=splint_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}{ammo}{helm}{armor}{headphones}{first_aid}{bandage}1{tourniquet}{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    if tourniquet == 0:
        tourniquet_t = 'Жгут'
    else:
        tourniquet_t = '\U00002705Жгут'
    tourniquet_b = InlineKeyboardButton(
        text=tourniquet_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}{ammo}{helm}{armor}{headphones}{first_aid}{bandage}{splint}1{night_raid}{nv}{lamp}{to_raid}'
        )
    )
    markup.add(first_aid_b, bandage_b, splint_b, tourniquet_b)
    if night_raid == 1:
        if nv == 0:
            nv_t = 'ПНВ'
        else:
            nv_t = '\U00002705ПНВ'
        nv_b = InlineKeyboardButton(
            text=nv_t,
            callback_data=checklist_cb.new(
                f'{drink}{eat}{weapon}{ammo}{helm}{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}1{lamp}{to_raid}'
            )
        )
        if lamp == 0:
            lamp_t = 'Фонарь'
        else:
            lamp_t = '\U00002705Фонарь'
        lamp_b = InlineKeyboardButton(
            text=lamp_t,
            callback_data=checklist_cb.new(
                f'{drink}{eat}{weapon}{ammo}{helm}{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}1{to_raid}'
            )
        )
        markup.add(nv_b, lamp_b)
    else:
        night_raid_t = 'Ночной рейд?'
        night_raid_b = InlineKeyboardButton(
            text=night_raid_t,
            callback_data=checklist_cb.new(
                f'{drink}{eat}{weapon}{ammo}{helm}{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}1{nv}{lamp}{to_raid}'
            )
        )
        markup.add(night_raid_b)

    to_raid_t = 'В рейд!'
    to_raid_b = InlineKeyboardButton(
        text=to_raid_t,
        callback_data=checklist_cb.new(
            f'{drink}{eat}{weapon}{ammo}{helm}{armor}{headphones}{first_aid}{bandage}{splint}{tourniquet}{night_raid}{nv}{lamp}1'
        )
    )
    markup.add(to_raid_b)
    return markup


async def process_checklist(cb_data: dict):
    print(cb_data)
    cb_list = list(cb_data['data'])
    for i in range(len(cb_list)):
        cb_list[i] = int(cb_list[i])
    markup = await make_checklist_keyboard(*cb_list)
    text = 'Пожалуйста, ничего не забудь...'
    if cb_list[-1] == 1:
        return True, InlineKeyboardMarkup(), 'Удачи в рейде!'
    else:
        return False, markup, text
