
import asyncio
import httpx
import logging
from threading import Thread, Event

from src.config import settings

class BackendChecker:
    def __init__(self, check_interval: int = 5):
        self.backend_url = f"{settings.BACKEND_URL}/health"
        self.check_interval = check_interval
        self._is_backend_available = Event()
        self._stop_event = Event()
        self._thread = Thread(target=self.run_periodic_check)

    @property
    def is_available(self) -> bool:
        return self._is_backend_available.is_set()

    async def check_backend(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.backend_url)
                if response.status_code == 200:
                    if not self.is_available:
                        self._is_backend_available.set()
                        logging.info("Backend is now available.")
                else:
                    if self.is_available:
                        self._is_backend_available.clear()
                        logging.warning(f"Backend is down. Status code: {response.status_code}")
        except httpx.RequestError:
            if self.is_available:
                self._is_backend_available.clear()
                logging.warning("Backend is down. Connection error.")

    def run_periodic_check(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while not self._stop_event.is_set():
            loop.run_until_complete(self.check_backend())
            self._stop_event.wait(self.check_interval)
        loop.close()

    def start(self):
        if not self._thread.is_alive():
            self._stop_event.clear()
            self._thread.start()
            logging.info("Backend checker started.")

    def stop(self):
        if self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()
            logging.info("Backend checker stopped.")

backend_checker = BackendChecker()
