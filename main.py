import vk_api
import vk_api.bot_longpoll
import config
import server
import threading
import asyncio
import random
from bot_logic import send_game_request_to_admin

vk_session = vk_api.VkApi(token=config.VK_TOKEN)
vk = vk_session.get_api()
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, group_id=238963448)

def get_random_id():
    return random.randint(1, 2**63 - 1)

def run_bot():
    print("[Бот] запущен и слушает сообщения...")
    for event in longpoll.listen():
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            msg = event.object.message
            peer_id = msg['peer_id']
            text = msg.get('text', '').lower()

            print(f'[Бот] получено сообщение от {peer_id}: "{text}"')

            if text == 'гол':
                print('[Бот] обнаружено "гол", отправляю ответ')
                try:
                    vk.messages.send(
                        peer_id=peer_id,
                        message='я бутерброд',
                        random_id=get_random_id()
                    )
                    print('[Бот] ответ отправлен!')
                except Exception as e:
                    print(f'[Бот] ошибка: {e}')

            elif text.startswith('/заявка') or 'заявка' in text:
                print('[Бот] обнаружена заявка, обрабатываю...')

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                test_data = {
                    'demands': [{
                        'first_name': 'писькин',
                        'last_name': 'попин',
                        'vk_id': peer_id,
                        'for_week': '2026-06-01',
                        'slots': [{'name': 'Вечер', 'valid_from': '18:00', 'valid_until': '22:00'}]
                    }]
                }

                loop.run_until_complete(
                    send_game_request_to_admin(vk_session, test_data)
                )
                loop.close()
                print('[Бот] Заявка отправлена админу!')


def run_server():
    asyncio.run(server.start_http_server())


server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

if __name__ == "__main__":
    print("[Бот] запуск...")
    run_bot()
