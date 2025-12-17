# utils.py
import logging
import time
from functools import wraps

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def log_execution_time(func):
    """
    Декоратор для логирования времени выполнения асинхронной функции.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        logger.info(f"✅ {func.__qualname__} completed in {elapsed:.4f} seconds")
        return result
    return wrapper