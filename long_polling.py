# long_polling.py
import asyncio
import aiohttp
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


async def get_updates(offset=None, timeout=30):
    async with aiohttp.ClientSession() as session:
        params = {"timeout": timeout}
        if offset is not None:
            params["offset"] = offset
        async with session.get(f"{BASE_URL}/getUpdates", params=params) as resp:
            return await resp.json()


async def start_long_polling(dispatcher):
    offset = None
    print("🍕 Pizza Bot запущен. Ожидание заказов...")
    while True:
        try:
            updates = await get_updates(offset)
            for update in updates.get("result", []):
                await dispatcher.process_update(update)
                offset = update["update_id"] + 1
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(3)
