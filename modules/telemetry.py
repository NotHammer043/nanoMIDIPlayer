import requests
import time
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://api.nanomidi.net"
PING_URL = f"{BASE_URL}/api/nanomidiplayer/statistics/ping"

def connection():
    logger.info("connection called")
    while True:
        try:
            logger.debug("testing connection to BASE_URL")
            requests.get(BASE_URL, timeout=5)
            logger.info("connection successful")
            return
        except Exception as e:
            logger.warning(f"connection failed: {e}")
            for i in range(50):
                time.sleep(0.1)

def startPing():
    logger.info("startPing called")
    connection()
    while True:
        try:
            logger.debug("sending ping request")
            requests.post(PING_URL, json={}, timeout=10)
            logger.debug("ping successful")
        except Exception as e:
            logger.warning(f"ping failed: {e}")
        for i in range(500):
            time.sleep(0.1)