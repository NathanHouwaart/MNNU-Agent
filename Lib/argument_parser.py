import argparse
from logger import line_info, log_msg

LOG_COLOR = "fg:magenta"


def log_args(args):
    log_msg(f"{line_info()}Starting Agent with args:", color=LOG_COLOR)
    for arg in vars(args):
        log_msg(f"{line_info()}\t{arg:<30}{getattr(args, arg)}", color=LOG_COLOR) #TODO: ledger port als argument toevoegen
    log_msg(f"{line_info()}", color=LOG_COLOR)


def argument_parser(port: int = 8020):
    """
    Standard command-line arguements.

    identity: the name of the agent that will run
    port: the start port of the agent that will run. Note, an agent will occupy up to port+9.
    """
    parser = argparse.ArgumentParser(
        description="Runs an aries agent with a given identity on a specified portrange"
    )
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    
    #### Required arguments ####
    required.add_argument(
        "--identity",
        type=str,
        metavar="<ident>",
        help="Agent identity (label)",
        required=True
    )
    required.add_argument(
        "--port",
        type=int,
        default=port,
        metavar=("<port>"),
        help="Choose the starting port number to listen on",
        required=True
    )
    required.add_argument(
        "--ledger-ip",
        type=str,
        metavar=("<ledger-ip>"),
        help="The url of the ledger",
        required=True
    )
    required.add_argument(
        "--wallet-name",
        type=str,
        metavar=("<name>"),
        help="The name of the wallet",
        required=True
    )
    required.add_argument(
        "--wallet-key",
        type=str,
        metavar=("<key>"),
        help="The key of the wallet. Can be set to 'random' to generate new key'", #TODO: implement key generation
        required=True
    )

    #### Optional Arguments ####
    optional.add_argument(
        "--public-did",
        action="store_true",
        help="Create a public DID for the agent"
    )
    optional.add_argument(
        "--transport-protocol",
        type=str,
        metavar=("<protocol>"),
        default="http",
        help="Internet protocol to use"
    )
    optional.add_argument(
        "--no-auto",
        action="store_true",
        help="Disable auto issuance",
    )
    optional.add_argument(
        "--did-exchange",
        action="store_true",
        help="Use DID-Exchange protocol for connections",
    )
    optional.add_argument(
        "--revocation", 
        action="store_true", 
        help="Enable credential revocation"
    )
    optional.add_argument(
        "--tails-server-base-url",
        type=str,
        metavar=("<tails-server-base-url>"),
        help="Tals server base url",
    )
    optional.add_argument(
        "--timing", 
        action="store_true", 
        help="Enable timing information"
    )
    optional.add_argument(
        "--multitenant", 
        action="store_true", 
        help="Enable multitenancy options"
    )
    optional.add_argument(
        "--mediation", 
        action="store_true", 
        help="Enable mediation functionality"
    )
    optional.add_argument(
        "--wallet-type",
        type=str,
        default="indy",
        metavar="<wallet-type>",
        help="Set the agent wallet type",
    )
    optional.add_argument(
        "--seed",
        type=str,
        metavar="<seed>",
        help="Seed to create a wallet with",
        default="random"
    )

    return parser