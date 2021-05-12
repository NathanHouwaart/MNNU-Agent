import os
import sys
import asyncio
import json
import textwrap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../Lib')

from argument_parser import argument_parser, log_args
from localtunnel import LocalTunnel
from agent import Agent
from utilities import log_msg, prompt_loop

LOG_COLOR = "hot pink"
# docker run --name test1 --rm -it -p 0.0.0.0:8010-8011:8010-8011 -v C:\Users\Nathan\Documents\Innovation\MNNU-Agent:/home/indy/MNNU-Agent -w /home/indy/MNNU-Agent/Demo mnnu-agent:0.5 "python3 demo-agent.py --port 8010 --identity test --ledger-url http://greenlight.bcovrin.vonx.io --endpoint https://curly-kangaroo-33.loca.lt --local-ip 127.0.0.1 --seed lMotigUUBzcqZl9BIx3103IfUN9Mjq82 --wallet-name test.Wallet --wallet-key test123"
# docker run --name test2 --rm -it -p 0.0.0.0:8012-8013:8012-8013 -v /home/nathan/MNNU-Agent:/home/indy/MNNU-Agent -w /home/indy/MNNU-Agent/Demo mnnu-agent:0.5 "python3 demo-agent.py --port 8012 --identity test2 --ledger-url http://greenlight.bcovrin.vonx.io --endpoint https://mean-chipmunk-98.loca.lt --local-ip 127.0.0.1 --seed lMotigUUBzcqZl9BIx3103IfUN9Mjq83 --wallet-name test2.Wallet --wallet-key test2123"

async def main(args):
    """
    Main function that: initializes the aries agent and
    show a prompt loop to interact with the agent
    """
    global aries_cloudagent_agent

    incoming_tunnel = LocalTunnel(args.port)
    api_tunnel = LocalTunnel(args.port+1)
    
    await incoming_tunnel.start_local_tunnel()
    await api_tunnel.start_local_tunnel()
    
    log_msg("incoming_tunnel_url: ", incoming_tunnel.tunnel_url, color=LOG_COLOR)
    log_msg("api_tunnel_url: ", api_tunnel.tunnel_url, color=LOG_COLOR)
    
    aries_cloudagent_agent = Agent(
        identity=args.identity,
        start_port=args.port,
        transport_protocol=args.transport_protocol,
        endpoint=incoming_tunnel.tunnel_url,
        ledger_url=args.ledger_url,
        local_ip=args.local_ip,
        wallet_name=args.wallet_name,
        wallet_key=args.wallet_key,
        seed=args.seed,
        public_did=args.public_did,
        auto_response=args.no_auto
    )

    await aries_cloudagent_agent.initialize()

    options = ("1. Show Connections\n2. Generate invitation\n3. Receive inivtaiotn\n4. Send Message\n5. Get connection state\n6. Create Schema\n7. Create credential definition\n8. Issue credential\n9. Get credentials\n10. Exit\n")

    # async for option in prompt_loop(options):
    #     # try:
    #     if int(option) == 1:
    #         connections = await aries_cloudagent_agent.connections()
    #         log_msg(f"{json.dumps(connections, indent=4, sort_keys=True)}", color=LOG_COLOR)
    #         log_msg(f"Total connections:", len(connections["results"]), color=LOG_COLOR)
    #     elif int(option) == 2:
    #         await aries_cloudagent_agent.generate_invitation(display_qr=True)
    #     elif int(option) == 3:
    #         await aries_cloudagent_agent.receive_invitation(invitation=None, alias=None, auto_accept=None)
    #     elif int(option) == 4:
    #         await aries_cloudagent_agent.send_message(connection_id=None, message=None)
    #     elif int(option) == 5:
    #         connection_state = await aries_cloudagent_agent.get_connection_state(connection_id=None)
    #         log_msg(f"Connection state", connection_state, color=LOG_COLOR)
    #     elif int(option) == 6:
    #         schema_id = await aries_cloudagent_agent.create_schema()
    #         log_msg(f"schema id: {schema_id}", color=LOG_COLOR)
    #     elif int(option) == 7:
    #         cred_def_id = await aries_cloudagent_agent.create_credential_definition()
    #         log_msg(f"credential def id: {cred_def_id}", color=LOG_COLOR)
    #     elif int(option) == 8:
    #         credential = await aries_cloudagent_agent.issue_credential()
    #         log_msg(f"Credential exchange id: {credential['credential_exchange_id']}", color=LOG_COLOR)
    #     elif int(option) == 9:
    #         credentials = await aries_cloudagent_agent.get_credentials()
    #         log_msg(f"There is/are {len(credentials['results'])} credential(s)", color=LOG_COLOR)
    #         for i in range(len(credentials['results'])):
    #             log_msg(f"\tCredential: {credentials['results'][i]['attrs']}", color=LOG_COLOR)
    #     elif int(option) == 10:
    #         return
    #     # except:
    #     #     pass
    while True:
        await asyncio.sleep(1.0)

if __name__ == "__main__":
    """
    Entrypoint of application
    """

    parser = argument_parser()
    args = parser.parse_args()
    log_args(args)

    # Construct Aries cloud agent object

    aries_cloudagent_agent = None 

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(args))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        exception_name, exception_value, _ = sys.exc_info()
        raise
    finally:
        loop.run_until_complete(aries_cloudagent_agent.terminate())
        loop.close()
        os._exit(1)
