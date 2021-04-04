import asyncio
import random 
import os
import sys
import subprocess
import functools
import json

from utilities import log_msg
from aiohttp import (
    web,
    ClientSession,
    ClientRequest,
    ClientResponse,
    ClientError,
    ClientTimeout,
)

LOG_COLOR= "violet"

class Container:
    """Container class to represent, initialize and maintain a running docker container"""

    def __init__(
        self,
        identity                    : str,
        endpoint                    : str,
        seed                        : str,
        indbound_transport_port     : int,
        outbound_transport_port     : int,
        transport_protocol          : str,
        wallet_name                 : str,
        wallet_key                  : str,
        webhook_url                 : str,
        genesis_url                 : str
    ):
        """Constructor of the container class. """
        self.identity                = identity
        self.endpoint                = endpoint
        self.seed                    = seed
        self.indbound_transport_port = indbound_transport_port
        self.outbound_transport_port = outbound_transport_port
        self.transport_protocol      = transport_protocol
        self.wallet_name             = wallet_name
        self.wallet_key              = wallet_key
        self.webhook_url             = webhook_url
        self.genesis_url             = genesis_url


    async def start_process(self, wait: bool = True):
        log_msg("Start Docker container", color=LOG_COLOR)

        agent_args = self.get_process_args()
        log_msg(f"Starting agent with args: {agent_args}", color=LOG_COLOR)
        
        self.container_process = await asyncio.create_subprocess_exec(  # TODO: Catch invalid key/ arguments error.
            *agent_args
        )
        if wait: 
            await asyncio.sleep(10.0)                                    #TODO: Timeout verplaatsen naar api handler
        log_msg("Docker container started", color=LOG_COLOR)

    def get_process_args(self):
        # TODO: goed implementeren 
        # TODO: LEDGER IP !+ ENDPOINT IP (DENK IK)
        result = [
            "python3", "-m", "aries_cloudagent", "start", 
            "--endpoint" , f"{self.endpoint}", 
            "--label", f"{self.identity}.Agent", 
            "--auto-ping-connection", 
            "--auto-respond-messages", 
            "--inbound-transport", f"{self.transport_protocol}", "0.0.0.0", f"{self.indbound_transport_port}" ,
            "--outbound-transport", f"{self.transport_protocol}", 
            "--admin", "0.0.0.0", f"{self.outbound_transport_port}",
            "--admin-insecure-mode",
            "--wallet-type","indy",                                     #TODO: niet hardcoden 
            "--wallet-name",f"{self.wallet_name}", 
            "--wallet-key", f"{self.wallet_key}",
            "--preserve-exchange-records", 
            "--auto-provision",
            "--genesis-url", f"{self.genesis_url}", 
            "--seed", f"{self.seed}",
            "--webhook-url", f"{self.webhook_url}", 
            "--trace-target", "log", 
            "--trace-tag","acapy.events", 
            "--trace-label", "faber.agent.trace",       #TODO: niet hardcoden
            "--auto-accept-invites", 
            "--auto-accept-requests", 
            "--auto-store-credential"
        ]
        return result

    async def terminate(self):
        log_msg(f"Shutting down agent", color=LOG_COLOR)
        
        # Check if process exists and is running
        if self.container_process and self.container_process.returncode is None:
            try:
                self.container_process.terminate()
                await asyncio.wait_for(self.container_process.communicate(), timeout=1)
                log_msg(f"Docker Container exited with return code {self.container_process.returncode}", color=LOG_COLOR)
            except asyncio.TimeoutError:
                msg = f"Process did not terminate in time"
                log_msg(msg, color=LOG_COLOR)
                await self.container_process.kill()
                raise Exception(msg)