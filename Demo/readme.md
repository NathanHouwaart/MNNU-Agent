docker run --name faber --rm -it  --entrypoint /bin/bash --network=bridge   -p 0.0.0.0:8020-8027:8020-8027   -v /Users/nathanhouwaart/Documents/HBO-ICT/jaar3/Innovation/debug-environment/MNNU-Agent:/home/indy/MNNU-Agent   -e LOG_LEVEL= -e RUNMODE=docker -e DOCKERHOST=192.168.65.3 -e AGENT_PORT=8020 -e TRACE_TARGET=log -e TRACE_TAG=acapy.events -e TRACE_ENABLED=   demo-agent:1.0


## Start Agent 1
1. `docker run --name alice --rm -it  --entrypoint /bin/bash --network=bridge   -p 0.0.0.0:8030-8037:8030-8037   -v /Users/nathanhouwaart/Documents/HBO-ICT/jaar3/Innovation/debug-environment/DemoAgent/runners:/home/indy/DemoAgent/runners   -e LOG_LEVEL= -e RUNMODE=docker -e DOCKERHOST=192.168.65.3 -e AGENT_PORT=8020 -e TRACE_TARGET=log -e TRACE_TAG=acapy.events -e TRACE_ENABLED=   demo-agent:1.0`

2. `python3 demo-agent_1.py --port 8030 --identity Alice --ledger-ip 192.168.65.3 --seed d_000000000000000000000000Test01 --wallet-name Test01.Wallet --wallet-key test123`

## Start Agent 2
1. `docker run --name faber --rm -it  --entrypoint /bin/bash --network=bridge   -p 0.0.0.0:8020-8027:8020-8027   -v /Users/nathanhouwaart/Documents/HBO-ICT/jaar3/Innovation/debug-environment/MNNU-Agent:/home/indy/MNNU-Agent   -e LOG_LEVEL= -e RUNMODE=docker -e DOCKERHOST=192.168.65.3 -e AGENT_PORT=8020 -e TRACE_TARGET=log -e TRACE_TAG=acapy.events -e TRACE_ENABLED=   demo-agent:1.0`

2. `python3 demo-agent_2.py --port 8020 --identity Nathan --ledger-ip 192.168.65.3 --seed d_000000000000000000000000Test00 --wallet-name Test00.Wallet --wallet-key test123`

