
import os
import sys
import asyncio
import json
import textwrap
from qrcode import QRCode

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../Lib')

from localtunnel import LocalTunnel
from utilities import log_msg, prompt_loop
from api_handler import ApiHandler

LOG_COLOR = "hot pink"

if __name__ == "__main__":
    print(sys.argv[1], sys.argv[2])
    api_handler = ApiHandler(sys.argv[1], sys.argv[2])

    options = ("1. Show Connections\n2. Generate invitation\n3. Receive inivtaiotn\n4. Send Message\n5. Get connection state\n6. Create Schema\n7. Create credential definition\n8. Issue credential\n9. Get credentials\n10. Exit\n")
    alias = "api_handler_test"
    
    while True:
        option = input(options)
        try:
            if int(option) == 1:
                connections = api_handler.connections()
                log_msg(f"{json.dumps(connections, indent=4, sort_keys=True)}", color=LOG_COLOR)
                log_msg(f"Total connections:", len(connections["results"]), color=LOG_COLOR)
            elif int(option) == 2:
                invitation_id, invitation = api_handler.create_invitation(alias=alias, multi_use=False, auto_accept=True)
                qr = QRCode(border=1)
                qr.add_data(json.dumps(invitation))
                log_msg(f"Use the following JSON to accept the invite from another demo agent. Or use the QR code to connect from a mobile agent.", color=LOG_COLOR)
                log_msg(f"Invitation Data:", json.dumps(
                    invitation), color=LOG_COLOR)
                qr.print_ascii(invert=True)

            elif int(option) == 3:
                invitation = input("Invite details: ")
                auto_accept = input("Auto accept invitation? n/y: ")
                if auto_accept == "y":
                    auto_accept = True
                else:
                    auto_accept = False
                api_handler.receive_invitation(invitation_url=invitation, alias=alias, auto_accept=True)
            
            elif int(option) == 4:
                connection_id = input("Send message to <connection id> :")
                message = input("Message <message>:")
                api_handler.send_message(connection_id, message)
                
            elif int(option) == 5:
                connection_id = input("Connection state: ")
                connection_state = api_handler.get_connection_state(connection_id)
                log_msg(f"Connection state", connection_state, color=LOG_COLOR)
            
            elif int(option) == 6:
                schema = input("Schema :")  # TODO: Throw exception when schema is invalid
                schema = json.loads(schema)
                schema_id = api_handler.create_schema(schema)
                log_msg(f"schema id: {schema_id}", color=LOG_COLOR)
            
            elif int(option) == 7:
                schema_id = input("Schema ID <id>:")     # TODO: Throw exception when invitation is invalid
                schema_tag= input("Schema tag <tag>:")   # TODO: Throw exception when invitation is invalid
                cred_def_id = api_handler.create_credential_definition(schema_id, schema_tag, False)
                log_msg(f"credential def id: {cred_def_id}", color=LOG_COLOR)
            
            elif int(option) == 8:
                connection_id = input("Connection ID <id>: ")
                cred_def_id = input("Connection definition ID <id>: ")
                schema = json.loads(input("Schema <schema>: ").replace("'", '"'))
                log_msg(schema)
                attributes = json.loads(input("Attributes <attributes>: "))
                log_msg(attributes)
                credential = api_handler.issue_credential(connection_id, cred_def_id, attributes, schema)
                log_msg(f"Credential exchange id: {credential['credential_exchange_id']}", color=LOG_COLOR)
            
            elif int(option) == 9:
                credentials = api_handler.get_credentials()
                log_msg(f"There is/are {len(credentials['results'])} credential(s)", color=LOG_COLOR)
                for i in range(len(credentials['results'])):
                    log_msg(f"\tCredential: {credentials['results'][i]['attrs']}", color=LOG_COLOR)
            
            elif int(option) == 10:
                break
        except:
            pass