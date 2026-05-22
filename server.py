import json
import asyncio
from aiohttp import web

bot_instance = None


async def handle_post_request(request):
    """Обработчик POST-запросов на сервер"""
    try:
        data = await request.json()

        print("\n[Получен JSON]:", json.dumps(data, indent=2, ensure_ascii=False))

        if bot_instance:
            from bot_logic import send_game_request_to_admin
            await send_game_request_to_admin(bot_instance, data)
        else:
            print("[Ошибка] экземпляр бота еще не создан!")

        return web.Response(text="OK", status=200)

    except json.JSONDecodeError:
        print("[Ошибка] не удалось декодировать JSON")
        return web.Response(text="Invalid JSON", status=400)
    except Exception as e:
        print(f"[Ошибка] при обработке запроса: {e}")
        return web.Response(text="Internal Server Error", status=500)


async def start_http_server():
    """Запускает HTTP-сервер для приема заявок"""
    app = web.Application()
    app.router.add_post('/dnd_request', handle_post_request)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("запущен на http://localhost:8080/dnd_request")

    await asyncio.Future()
