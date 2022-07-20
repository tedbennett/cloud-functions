import json
import httpx
import asyncio

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    if (
        "token" not in event
        or "device" not in event
        or "topic" not in event
        or "body" not in event
    ):
        logger.info("Failed to parse event")
        return False

    token = event["token"]
    device = event["device"]
    topic = event["topic"]
    body = event["body"]
    logger.info("Sending notification")

    client = httpx.AsyncClient(http2=True)
    asyncio.get_event_loop().run_until_complete(
        client.post(
            f"https://api.sandbox.push.apple.com/3/device/{device}",
            headers={
                "Content-Type": "application/json",
                "apns-priority": "10",
                "apns-topic": topic,
                "authorization": f"bearer {token}",
            },
            data=json.dumps(body),
        )
    )
    logger.info("Sent notification")
    return True
