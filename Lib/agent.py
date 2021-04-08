import asyncio
import random
import os
import sys
import json
from qrcode import QRCode

from container import Container
from api_handler import ApiHandler
from webhook_server import WebhookServer
from utilities import log_msg, prompt, prompt_loop
from aiohttp import (
    web,
    ClientSession,
    ClientRequest,
    ClientResponse,
    ClientError,
    ClientTimeout,
)

LOG_COLOR = "cyan"


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
        transport_protocol: str,
        ledger_url: str,
        local_ip: str,
        wallet_name: str,
        wallet_key: str,
        seed: str = "random",
        public_did: bool = True,
        auto_response: bool = False,
    ):
        # Construct docker container object to maintain a running container
        self.docker_container = Container(
            identity=identity,
            endpoint=f"{transport_protocol}://{local_ip}:{start_port}", #TODO:
            seed=seed,
            indbound_transport_port=start_port,
            outbound_transport_port=start_port + 1,
            transport_protocol=transport_protocol,
            wallet_name=wallet_name,
            wallet_key=wallet_key,
            webhook_url=f"{transport_protocol}://{local_ip}:{start_port+2}/webhooks", #TODO:
            genesis_url=f"{ledger_url}/genesis"
        )

        # Construct a webhook server object that handles incoming messages
        self.webhook_server = WebhookServer(
            identity=identity,
            webhook_ip=local_ip,
            webhook_protocol=transport_protocol,
            webhook_port=start_port + 2
        )  # TODO: webhook IP is not per definitie gelijk aan ledger ip

        # Construct Api Handler object that handles all Api calls
        self.api_handler = ApiHandler(  # TODO: Ledger transport protocol toevoegen
            api_url=local_ip,
            port=start_port + 1
        )

        self.identity = identity
        self.start_port = start_port
        self.ledger_url = ledger_url
        self.local_ip = local_ip
        self.seed = seed
        self.public_did = public_did
        self.auto_response = auto_response
        # TODO: Register DID weghalen en verplaatsen naar api handler
        self.client_session = ClientSession()
        self.transport_protocol = transport_protocol

        # TODO: random seed ja?
        rand_name = str(random.randint(100_000, 999_999))
        self.seed = (
            ("my_seed_000000000000000000000000" + rand_name)[-32:]
            if seed == "random"
            else seed
        )

    async def initialize(self) -> None:
        """
        Start a webhook server, register a DID and start a docker container process
        """
        await self.webhook_server.start_process()
        await self.register_did()
        await self.docker_container.start_process()

        # TODO:  Timeout toevoegen, wanneer verkeerde key wordt gegeven, geeft hij alsog aan dat er een goeie connectie is
        if self.api_handler.test_connection() is False:
            return
        self.admin_url = f"{self.transport_protocol}://{self.local_ip}:{self.start_port+1}"
        self.endpoint = f"{self.transport_protocol}://{self.local_ip}:{self.start_port}"
        log_msg(f"Admin URL is at: {self.admin_url}", color=LOG_COLOR)
        log_msg(f"Endpoint URL is at: {self.endpoint}", color=LOG_COLOR)

    async def create_schema(self, schema: dict) -> dict:
        """
        Create a schema on the ACA-Py instance

        :param schema: The schema to create
        :return: The created schema as a dict
        """
        return self.api_handler.create_schema(schema)

    async def connections(self, *, alias_query: str = None, invitation_key_query: str = None, my_did_query: str = None, connection_state_query: str = None, their_did_query: str = None, their_role_query: str = None) -> dict:
        """
        List and Query agent-to-agent connections

        Function can be called with no KWARGS to list ALL conenctions
        Function can also be called with KWARGS to query the list of connections

        :param alias_query: Only list connections with this alias
        :param invitation_key_query: Only list connections with this invitation key
        :param my_did_query: Only list connections with this "my did" value
        :param connection_state_query: Only list connections with this connection state
        :param their_did_query: Only list connections with this "their did" value
        :param their_role_query: Only list connections with this "their role" value
        :return: Queried list of agent-to-agent connections with their states
        """
        return self.api_handler.connections(alias_query=alias_query, invitation_key_query=invitation_key_query, connection_state_query=connection_state_query, their_did_query=their_did_query, their_role_query=their_did_query)

    async def generate_invitation(self, auto_accept: bool = True, multi_use: bool = False, display_qr: bool = False) -> tuple:
        """
        Create a connection invitation

        :param auto_accept: Auto accept connection handshake?
        :param multi_use: Can this invite be used multiple times?
        :param display_qr: Bool to indicate whether a QR code should be displayed in the terminal
        :return: A tuple containing the connection id and base64 encoded invite url
        """
        invitation_id, invitation = self.api_handler.create_invitation(
            alias=self.identity, multi_use=multi_use, auto_accept=auto_accept)
        if display_qr:
            qr = QRCode(border=1)
            qr.add_data(json.dumps(invitation))
            log_msg(f"Use the following JSON to accept the invite from another demo agent. Or use the QR code to connect from a mobile agent.", color=LOG_COLOR)
            log_msg(f"Invitation Data:", json.dumps(
                invitation), color=LOG_COLOR)
            qr.print_ascii(invert=True)
        return invitation_id, invitation

    async def send_message(self, connection_id: str, message: str):
        """
        Send a message to another connected agent

        :param connection_id: The connection id of the connection between this agent and the connected agent
        :param message: Message to send to the other agent
        :return: Response of the operation
        """
        connection_id = await prompt("Send message to <connection id> :")  # TODO: Throw exception when invitation is invalid
        message = await prompt("Message <message>:")
        self.api_handler.send_message(connection_id, message)

    async def register_did(self, ledger_url: str = None, alias: str = None, did: str = None, verkey: str = None, role: str = "TRUST_ANCHOR"):
        """
        Function registers a DID on the ledger

        :param ledger_url: The ledger_url of the ledger
        :param alias: The alias to gerister on the ledger
        :param did: Did to register
        :param verkey: Verkey to register
        :param role: role of the registered DID
        :raises Exception: raises an exception when an invalid response is given by the ledger
        """
        log_msg(f"Registering {self.identity} ...", color=LOG_COLOR)
        data = {"alias": alias or self.identity, "role": role}
        if did and verkey:
            data["did"] = did
            data["verkey"] = verkey
        else:
            data["seed"] = self.seed
        async with self.client_session.post(
            f"{self.ledger_url}/register", json=data
        ) as resp:
            if resp.status != 200:
                raise Exception(
                    f"Error registering DID, response code {resp.status}")
            nym_info = await resp.json()
            self.did = nym_info["did"]
            log_msg(f"nym_info: {nym_info}", color=LOG_COLOR)
        log_msg(f"Registered DID: {self.did}", color=LOG_COLOR)

    async def receive_invitation(self, invitation, alias=None, auto_accept=False) -> str:
        """
        Receive invitation url

        :param invitation: The base64 encoded invite url str
        :param alias: The alias to give to the connection as a str
        :param auto_accept: Auto accept connection handshake?
        :return: The connection id as a str
        """
        # TODO: Throw exception when invitation is invalid
        invitation = await prompt("Invite details: ")
        auto_accept = await prompt("Auto accept invitation? n/y: ")
        if auto_accept == "y":
            auto_accept = True
        else:
            auto_accept = False
        return self.api_handler.receive_invitation(
            invitation_url=invitation, alias=self.identity, auto_accept=True)

    async def get_connection_state(self, connection_id) -> int:
        """
        Get the connection state of a given connection id

        :param connection_id: The connection id
        :return: The state (see states dict)
        """
        # TODO: Throw exception when connection_id is invalid
        connection_id = await prompt("Connection state: ")
        return self.api_handler.get_connection_state(connection_id)

    async def terminate(self):
        """
        Terminate the Agent by closing the admin API, webhook server and docker container.

        :return: True if termination is complete
        """
        log_msg(f"Shutting down {self.identity}", color=LOG_COLOR)

        await self.client_session.close()       # Close session to admin api
        await self.webhook_server.terminate()   # Shut down web hooks first
        await self.docker_container.terminate()  # now shut down the agent

        return True
