import vk_api
import vk_api.bot_longpoll
import config
import server
import threading
import asyncio
import random

vk_session = vk_api.VkApi(token=config.VK_TOKEN)
vk = vk_session.get_api()
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, group_id=238963448)


def get_random_id():
    return random.randint(1, 2**63 - 1)


def run_bot():
    print("[Бот] Запущен и слушает сообщения...")
    for event in longpoll.listen():
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            msg = event.object.message
            peer_id = msg['peer_id']
            text = msg.get('text', '').lower()
            
            print(f'[Бот] Получено сообщение от {peer_id}: "{text}"')
            
            if text == 'гол':
                print('[Бот] Обнаружено "гол", отправляю ответ...')
                try:
                    vk.messages.send(
                        peer_id=peer_id,
                        message='я бутерброд',
                        random_id=get_random_id()
                    )
                    print('[Бот] Ответ отправлен!')
                except Exception as e:
                    print(f'[Бот] Ошибка: {e}')

def run_server():
    asyncio.run(server.start_http_server())

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

if __name__ == "__main__":
    print("[Бот] Запуск...")
    run_bot()