```console
argument_parser.py:8          	|  Starting Agent with args:
argument_parser.py:10         	|  	identity                      Nathan 
argument_parser.py:10         	|  	port                          8030 
argument_parser.py:10         	|  	ledger_ip                     192.168.65.3 
argument_parser.py:10         	|  	wallet_name                   Test00.Wallet 
argument_parser.py:10         	|  	wallet_key                    test123
argument_parser.py:10         	|  	public_did                    False
argument_parser.py:10         	|  	transport_protocol            http 
argument_parser.py:10         	|  	no_auto                       False
argument_parser.py:10         	|  	did_exchange                  False
argument_parser.py:10         	|  	revocation                    False
argument_parser.py:10         	|  	tails_server_base_url         None 
argument_parser.py:10         	|  	timing                        False
argument_parser.py:10         	|  	multitenant                   False
argument_parser.py:10         	|  	mediation                     False
argument_parser.py:10         	|  	wallet_type                   indy 
argument_parser.py:10         	|  	seed                          d_000000000000000000000000Test00
webhook_server.py:46          	|  Start webhook server
webhook_server.py:55          	|  Webhook server started 
agent.py:137                  	|  Registering Nathan ... 
agent.py:151                  	|  nym_info: {'did': 'Te9gCxAA5t5oKnRS3PCbnV', 'seed': 'd_000000000000000000000000Test00', 'verkey': 'FXAE2BUEqhe7f7guJZed94qesgRF8znamQBN27LFXxdr'}
agent.py:152                  	|  Registered DID: Te9gCxAA5t5oKnRS3PCbnV
container.py:51               	|  Start Docker container 
container.py:54               	|  Starting agent with args: ['python3', '-m', 'aries_cloudagent', 'start', '--endpoint', 'http://192.168.65.3:8030', '--label', 'Nathan.Agent', '--auto-ping-connection', '--auto-respond-messages', '--inbound-transport', 'http', '0.0.0.0', '8030', '--outbound-transport', 'http', '--admin', '0.0.0.0', '8031', '--admin-insecure-mode', '--wallet-type', 'indy', '--wallet-name', 'Test00.Wallet', '--wallet-key', 'test123', '--preserve-exchange-records', '--auto-provision', '--genesis-url', 'http://192.168.65.3:9000/genesis', '--seed', 'd_000000000000000000000000Test00', '--webhook-url', 'http://192.168.65.3:8032/webhooks', '--trace-target', 'log', '--trace-tag', 'acapy.events', '--trace-label', 'faber.agent.trace', '--auto-accept-invites', '--auto-accept-requests', '--auto-store-credential'] 

::::::::::::::::::::::::::::::::::::::::::::::
:: Nathan.Agent                             ::
::                                          ::
::                                          ::
:: Inbound Transports:                      ::
::                                          ::
::   - http://0.0.0.0:8030                  ::
::                                          ::
:: Outbound Transports:                     ::
::                                          ::
::   - http                                 ::
::   - https                                ::
::                                          ::
:: Public DID Information:                  ::
::                                          ::
::   - DID: Te9gCxAA5t5oKnRS3PCbnV          ::
::                                          ::
:: Administration API:                      ::
::                                          ::
::   - http://0.0.0.0:8031                  ::
::                                          ::
::                               ver: 0.6.0 ::
::::::::::::::::::::::::::::::::::::::::::::::

Listening...

container.py:61                 |  Docker container started
agent.py:104                  	|  Admin URL is at: http://192.168.65.3:8031 
agent.py:105                  	|  Endpoint URL is at: http://192.168.65.3:8030

1. Show Connections
2. Generate invitation
3. Receive inivtaiotn
4. Send Message
5. Get connection state
6. Exit
```