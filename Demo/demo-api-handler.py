
import os
import sys
import asyncio
import json
import textwrap
from qrcode import QRCode

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../Lib')

from argument_parser import argument_parser, log_args
from localtunnel import LocalTunnel
from agent import Agent
from utilities import log_msg, prompt_loop
from api_handler import ApiHandler

LOG_COLOR = "hot pink"

if __name__ == "__main__":
    api_handler = ApiHandler("127.0.0.1", 1067)

    options = ("1. Show Connections\n2. Generate invitation\n3. Receive inivtaiotn\n4. Send Message\n5. Get connection state\n6. Create Schema\n7. Create credential definition\n8. Issue credential\n9. Get credentials\n10. Exit\n")
    
    while True:
        option = input(options)
        # try:
        if int(option) == 1:
            connections = api_handler.connections()
            log_msg(f"{json.dumps(connections, indent=4, sort_keys=True)}", color=LOG_COLOR)
            log_msg(f"Total connections:", len(connections["results"]), color=LOG_COLOR)
        elif int(option) == 2:
            invitation_id, invitation = self.api_handler.create_invitation(alias="api_handler_test", multi_use=False, auto_accept=True)
            qr = QRCode(border=1)
            qr.add_data(json.dumps(invitation))
            log_msg(f"Use the following JSON to accept the invite from another demo agent. Or use the QR code to connect from a mobile agent.", color=LOG_COLOR)
            log_msg(f"Invitation Data:", json.dumps(
                invitation), color=LOG_COLOR)
            qr.print_ascii(invert=True)

        # elif int(option) == 3:
        #     await aries_cloudagent_agent.receive_invitation(invitation=None, alias=None, auto_accept=None)
        # elif int(option) == 4:
        #     await aries_cloudagent_agent.send_message(connection_id=None, message=None)
        # elif int(option) == 5:
        #     connection_state = aries_cloudagent_agent.get_connection_state(connection_id=None)
        #     log_msg(f"Connection state", connection_state, color=LOG_COLOR)
        # elif int(option) == 6:
        #     schema_id = aries_cloudagent_agent.create_schema()
        #     log_msg(f"schema id: {schema_id}", color=LOG_COLOR)
        # elif int(option) == 7:
        #     cred_def_id = aries_cloudagent_agent.create_credential_definition()
        #     log_msg(f"credential def id: {cred_def_id}", color=LOG_COLOR)
        # elif int(option) == 8:
        #     credential = aries_cloudagent_agent.issue_credential()
        #     log_msg(f"Credential exchange id: {credential['credential_exchange_id']}", color=LOG_COLOR)
        # elif int(option) == 9:
        #     credentials = aries_cloudagent_agent.get_credentials()
        #     log_msg(f"There is/are {len(credentials['results'])} credential(s)", color=LOG_COLOR)
        #     for i in range(len(credentials['results'])):
        #         log_msg(f"\tCredential: {credentials['results'][i]['attrs']}", color=LOG_COLOR)
        # elif int(option) == 10:
        #     return
        # except:
        #     pass