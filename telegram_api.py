# telegram_api.py
import os
import json
import urllib.request
import urllib.parse
from typing import Any, Dict, Optional
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в .env")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message_with_inline_keyboard(chat_id: int, text: str, buttons: list):
    """
    Отправляет сообщение с инлайн-клавиатурой.
    
    :param chat_id: ID чата
    :param text: Текст сообщения
    :param buttons: Список кнопок в формате:
        [
            [{"text": "Кнопка 1", "callback_data": "data1"}],
            [{"text": "Кнопка 2", "callback_data": "data2"}]
        ]
    """
    reply_markup = {"inline_keyboard": buttons}
    return send_message(chat_id, text, reply_markup=reply_markup)

def _make_request(method: str, params: Optional[Dict[str, Any]] = None) -> Dict:
    """Универсальный метод для вызова Telegram Bot API."""
    url = f"{BASE_URL}/{method}"
    data = None
    if params:
        if any(isinstance(v, (dict, list)) for v in params.values()):
            data = json.dumps(params).encode("utf-8")
            headers = {"Content-Type": "application/json"}
        else:
            data = urllib.parse.urlencode(params).encode("utf-8")
            headers = {}
    else:
        headers = {}

    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if not result.get("ok"):
                print(f"Telegram API error: {result.get('description')}")
            return result
    except Exception as e:
        print(f"Request failed: {e}")
        return {"ok": False, "error": str(e)}


def get_updates(offset: Optional[int] = None, timeout: int = 30) -> Dict:
    """Получить обновления от Telegram."""
    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    return _make_request("getUpdates", params)


def send_message(
    chat_id: int,
    text: str,
    reply_markup: Optional[Dict] = None,
    parse_mode: Optional[str] = None
) -> Dict:
    """Отправить текстовое сообщение."""
    params = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        params["reply_markup"] = reply_markup
    if parse_mode:
        params["parse_mode"] = parse_mode
    return _make_request("sendMessage", params)


def answer_callback_query(callback_query_id: str, text: Optional[str] = None, show_alert: bool = False) -> Dict:
    """Подтвердить callback-запрос."""
    params = {"callback_query_id": callback_query_id}
    if text:
        params["text"] = text
    if show_alert:
        params["show_alert"] = show_alert
    return _make_request("answerCallbackQuery", params)

def delete_message(chat_id: int, message_id: int):
    """Удаляет сообщение по его ID."""
    params = {"chat_id": chat_id, "message_id": message_id}
    return _make_request("deleteMessage", params)