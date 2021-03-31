# TODO: Docstrings

import asyncio
import random 
import os
import sys
import subprocess
import functools
import json

from container import Container
from api_handler import ApiHandler
from logger import log_msg, log_timer, output_reader, default_timer, line_info, repr_json
from aiohttp import (
    web,
    ClientSession,
    ClientRequest,
    ClientResponse,
    ClientError,
    ClientTimeout,
)

class WebhookServer():
    def __init__(
        self,
        identity,
        webhook_ip,
        webhook_protocol,
        webhook_port,
    ):
        self.identity = identity
        self.webhook_ip = webhook_ip
        self.webhook_protocol = webhook_protocol
        self.webhook_port = webhook_port
        self.webhook_url = f"{webhook_protocol}://{webhook_ip}:{webhook_port}/webhooks"
    
    async def start_process(self):
        app = web.Application()
        app.add_routes([web.post("/webhooks/topic/{topic}/", self._receive_webhook)])
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        self.webhook_site = web.TCPSite(runner, "0.0.0.0", self.webhook_port)
        await self.webhook_site.start()

    async def _receive_webhook(self, request: ClientRequest):
        topic = request.match_info["topic"].replace("-", "_")
        payload = await request.json()
        await self.handle_webhook(topic, payload, request.headers)
        return web.Response(status=200)

    async def handle_webhook(self, topic: str, payload, headers: dict):
        if topic != "webhook":  # would recurse
            handler = f"handle_{topic}"
            wallet_id = headers.get("x-wallet-id")
            method = getattr(self, handler, None)
            if method:
                log_msg(f"{line_info()}"
                    "Agent called controller webhook: %s%s%s%s",
                    handler,
                    f"\nPOST {self.webhook_url}/topic/{topic}/",
                    (f" for wallet: {wallet_id}" if wallet_id else ""),
                    (f" with payload: \n{repr_json(payload)}\n" if payload else ""),
                )
                asyncio.get_event_loop().create_task(method(payload))
            else:
                log_msg(f"{line_info()}"
                    f"Error: agent {self.identity} "
                    f"has no method {handler} "
                    f"to handle webhook on topic {topic}"
                )

    async def handle_basicmessages(self, message):
        self.log(f"{line_info()}Received message:", message["content"])
    
    async def handle_connections(self, test):
        print("test", test)
    
    async def terminate(self):
        log_msg(f"{line_info()}Shutting down web hooks site")
        if self.webhook_site:
            await self.webhook_site.stop()
            await asyncio.sleep(0.5)
