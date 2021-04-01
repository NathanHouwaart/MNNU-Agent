import asyncio
import random 
import os
import sys
import subprocess
import functools
import json
from qrcode import QRCode
from urllib.parse import urlparse
import base64
import binascii

from container import Container
from api_handler import ApiHandler
from webhook_server import WebhookServer
from logger import *
from aiohttp import (
    web,
    ClientSession,
    ClientRequest,
    ClientResponse,
    ClientError,
    ClientTimeout,
)


class Agent:
    """
    An Aries CloudAgent object

    This object has all the tools needed to interact with the ledger.
        1. It sets-up a docker container,
        2. It sets-up a webhook server to handle incoming communications
        3. It has a build-in API handler to handle interaction with the ledger
    """
    def __init__(
        self, 
        identity: str, 
        start_port: int, 
        transport_protocol : str,
        ledger_ip: str,
        ledger_port: int,
        wallet_name : str,
        wallet_key : str,
        seed: str = "random",
        public_did: bool = True,
        auto_response: bool = False,
    ):
        # Construct docker container object to maintain a running container
        self.docker_container = Container(
            identity=identity, 
            endpoint=f"{transport_protocol}://{ledger_ip}:{start_port}", 
            seed=seed, 
            indbound_transport_port=start_port, 
            outbound_transport_port=start_port+1, 
            transport_protocol=transport_protocol,
            wallet_name=wallet_name, 
            wallet_key=wallet_key, 
            webhook_url=f"{transport_protocol}://{ledger_ip}:{start_port+2}/webhooks", 
            genesis_url=f"{transport_protocol}://{ledger_ip}:{ledger_port}/genesis"
        )

        # Construct a webhook server object that handles incoming messages
        self.webhook_server = WebhookServer(
            identity=identity,
            webhook_ip=ledger_ip,
            webhook_protocol=transport_protocol,
            webhook_port=start_port+2
        ) #TODO: webhook IP is not per definitie gelijk aan ledger ip
        
        # Construct Api Handler object that handles all Api calls
        self.api_handler = ApiHandler( #TODO: Ledger transport protocol toevoegen
            transport_protocol=transport_protocol,
            api_url=ledger_ip, 
            port=start_port+1
        )
        
        self.identity = identity
        self.start_port = start_port
        self.ledger_ip = ledger_ip
        self.seed = seed
        self.public_did = public_did
        self.auto_response = auto_response
        self.client_session = ClientSession() # TODO: Register DID weghalen en verplaatsen naar api handler
        self.transport_protocol = transport_protocol

        rand_name = str(random.randint(100_000, 999_999)) #TODO: random seed ja?
        self.seed = (
            ("my_seed_000000000000000000000000" + rand_name)[-32:]
            if seed == "random"
            else seed
        )
        
    async def initialize(self):
        """
        Start a webhook server, register a DID and start a docker container process
        
        """
        with log_timer(f"{line_info()}Webhook server startup duration:"): #TODO: Uitzoeken hoe log timer werkt
            await self.webhook_server.start_process()

        await self.register_did()
        
        with log_timer(f"{line_info()}Docker container startup duration:"):
            await self.docker_container.start_process()
        
        if self.api_handler.test_connection() == False: # TODO:  Timeout toevoegen, wanneer verkeerde key wordt gegeven, geeft hij alsog aan dat er een goeie connectie is
            return
        self.admin_url = f"{self.transport_protocol}://{self.ledger_ip}:{self.start_port+1}"
        self.endpoint =  f"{self.transport_protocol}://{self.ledger_ip}:{self.start_port}"
        log_msg(f"{line_info()}Admin URL is at:", self.admin_url)
        log_msg(f"{line_info()}Endpoint URL is at:", self.endpoint)

    async def create_schema(self, schema: dict) -> dict:
        return self.api_handler.create_schema(schema)

    async def connections(self, *,alias_query: str=None, invitation_key_query: str=None, my_did_query: str=None, connection_state_query: str=None, their_did_query: str=None, their_role_query: str=None) -> dict:
        return self.api_handler.connections(alias_query=alias_query, invitation_key_query=invitation_key_query, connection_state_query=connection_state_query, their_did_query=their_did_query, their_role_query=their_did_query)
    
    async def generate_invitation(self, auto_accept: bool = True, multi_use: bool = False, display_qr: bool = False) ->tuple:
        invitation_id, invitation =  self.api_handler.create_invitation(alias=self.identity, multi_use=multi_use, auto_accept=auto_accept)
        if display_qr:
            qr = QRCode(border=1)
            qr.add_data(json.dumps(invitation))
            log_msg(f"{line_info()}Use the following JSON to accept the invite from another demo agent. Or use the QR code to connect from a mobile agent.")
            log_msg(f"{line_info()}Invitation Data:",json.dumps(invitation))
            qr.print_ascii(invert=True)
        return invitation_id, invitation

    async def send_message(self, connection_id: str, message: str):
        connection_id = await prompt("Send message to <connection id> :") #TODO: Throw exception when invitation is invalid
        message = await prompt("Message <message>:") #TODO: Throw exception when invitation is invalid
        self.api_handler.send_message(connection_id, message)

    async def register_did( #TODO: verplaatsen
        self,
        ledger_ip: str = None,
        alias: str = None,
        did: str = None,
        verkey: str = None,
        role: str = "TRUST_ANCHOR",
    ):
        log_msg(f"{line_info()}Registering {self.identity} ...")
        data = {"alias": alias or self.identity, "role": role}
        if did and verkey:
            data["did"] = did
            data["verkey"] = verkey
        else:
            data["seed"] = self.seed
        async with self.client_session.post(
            f"{self.transport_protocol}://{self.ledger_ip}" + ":9000/register", json=data # TODO: PORT niet hardcoden
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Error registering DID, response code {resp.status}")
            nym_info = await resp.json()
            self.did = nym_info["did"]
            log_msg(f"{line_info()}nym_info: {nym_info}")
        log_msg(f"{line_info()}Registered DID: {self.did}")

    
    async def receive_invitation(self, invitation, alias=None, auto_accept=False):
        invitation = await prompt("Invite details: ") #TODO: Throw exception when invitation is invalid
        auto_accept = await prompt("n/y: ") #TODO: Throw exception when invitation is invalid
        if auto_accept == "y":
            auto_accept = True
        else:
            auto_accept = False
        connection_id = self.api_handler.receive_invitation(invitation_url=invitation, alias=self.identity, auto_accept=True)



    async def terminate(self):
        log_msg(f"{line_info()}Shutting down {self.identity}")
        
        await self.client_session.close()       # Close session to admin api
        await self.webhook_server.terminate()   # Shut down web hooks first
        await self.docker_container.terminate() # now shut down the agent
        
        return True
        
