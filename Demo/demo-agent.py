import os
import sys
import asyncio
import json
import textwrap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../Lib')

from argument_parser import argument_parser, log_args
from agent import Agent
from logger import log_msg, line_info, prompt_loop

LOG_COLOR="aqua"

async def main(aries_cloudagent_agent):
    """
    Main function that: initializes the aries agent and
    show a prompt loop to interact with the agent
    """
    await aries_cloudagent_agent.initialize()

    options =  (
"1. Show Connections\n\
2. Generate invitation\n\
3. Receive inivtaiotn\n\
4. Send Message\n\
5. Exit\n")
    
    async for option in prompt_loop(options):
        if int(option) == 1:
            connections = await aries_cloudagent_agent.connections()
            log_msg(f"{line_info()}{json.dumps(connections, indent=4, sort_keys=True)}", color=LOG_COLOR)
            log_msg(f"{line_info()}Total connections:", len(connections["results"]), color=LOG_COLOR)
        elif int(option) == 2:
            await aries_cloudagent_agent.generate_invitation(display_qr=True)
        elif int(option) == 3:
            await aries_cloudagent_agent.receive_invitation(invitation=None, alias=None, auto_accept=None)
        elif int(option) == 4:
            await aries_cloudagent_agent.send_message(connection_id=None, message=None)
        elif int(option) ==5:
            return
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
    aries_cloudagent_agent = Agent(
        identity=args.identity,
        start_port=args.port,
        transport_protocol=args.transport_protocol,
        ledger_ip=args.ledger_ip,       # Check of dit goed gaat bij een publieke ledger
        ledger_port=9000,               # TODO: is dit nodig? bij een publieke ledger staat er geen port achter de url.
        wallet_name=args.wallet_name,
        wallet_key=args.wallet_key,
        seed=args.seed,
        public_did=args.public_did,
        auto_response=args.no_auto
    )
    
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(aries_cloudagent_agent))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        exception_name, exception_value, _ = sys.exc_info()
        raise
    finally:
        loop.run_until_complete(aries_cloudagent_agent.terminate())
        loop.close()
        os._exit(1)
    
