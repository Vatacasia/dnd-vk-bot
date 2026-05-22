import config


async def send_game_request_to_admin(bot, data: dict):
    """
    Отправляет заявку на ДНД.
    """
    if not data or 'demands' not in data or not data['demands']:
        print("неверный формат данных:", data)
        return

    req = data['demands'][0]

    msg = "заява накатана\n\n"
    msg += f"Имя: {req.get('first_name', '—')}\n"
    msg += f"Фамилия:{req.get('last_name', '—')}\n"
    msg += f"VK ID: {req.get('vk_id', '—')}\n"
    msg += f"Предпочитаемая неделя: {req.get('for_week', '—')}\n\n"
    msg += "Доступные слоты:\n"

    slots = req.get('slots', [])
    if not slots:
        msg += "  — не указаны\n"
    else:
        for s in slots:
            msg += f"  - *{s.get('name', 'Без названия')}*\n"
            msg += f"    с {s.get('valid_from', '??')} по {s.get('valid_until', '??')}\n"

    try:
        await bot.vk_request('messages.send', {
            'user_id': config.ADMIN_VK_ID,
            'message': msg,
            'random_id': 0
        })
        print(f"Заявка от {req.get('first_name')} {req.get('last_name')} отправлена админу")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")