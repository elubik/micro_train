import requests
import logging
import os

HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", 5002)


def handle_result(result, logger):
    if result.status_code == 200:
        result = result.json()
        return result
    else:
        logger.error("HTTP error")
        raise ConnectionError


def raise_exception(exception, logger):
    message = f"Sorry, requests.get() crashed during execution.\n{exception}"
    logger.error(message)
    raise Exception(message)


def barrier_get(station_name: str, logger: logging) -> dict:
    try:
        result = requests.get(f"http://{HOST}:{PORT}/{station_name}")
        return handle_result(result, logger)

    except Exception as ex:
        raise_exception(ex, logger)


def barrier_post(station_name: str, data: dict, logger: logging) -> None:
    try:
        result = requests.put(f"http://{HOST}:{PORT}/{station_name}", data=data)
        return handle_result(result, logger)

    except Exception as ex:
        raise_exception(ex, logger)
