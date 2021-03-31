import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../lib')

from argument_parser import argument_parser, log_args
from agent import Agent
from logger import log_msg, line_info

async def main(aries_cloudagent_agent):

    # Initialize object
    await aries_cloudagent_agent.initialize()
    inv_id, invitation = await aries_cloudagent_agent.generate_invitation(display_qr=True)
    # log_msg(f"{line_info()}Invitation: {invitation}")

    while True:
        await asyncio.sleep(1.0)


if __name__ == "__main__":
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
        log_msg(f"{line_info()}Sutting down agent...",color=LOG_COLOR)
    finally:
        loop.run_until_complete(aries_cloudagent_agent.terminate())
        loop.close()
        os._exit(1)
    
