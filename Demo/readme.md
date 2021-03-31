# MNNU-Agent
This repository contains all the modules and tools needed to setup one or multiple agent containers.

## Summary 
An agent is used to represent an individual in the digital world. It helps individuals (persons) to interact with a ledger to store credentials, receive credentials, interact with other agents and much more. In short, an agent is capable of:

1. Connecting with a ledger
2. Receiving and accepting invitations from other agents
3. Messaging other agents
3. Receiving and accepting credentials

## Requirements
In order to run an agent, a few things are required
1. Git (bash)
2. Docker
3. A working internet conneciton

## Run Demo
Running a demo is key in understanding the blockchain interaction. For this demo, two agents are setup

### Start Agent 1
1. `docker run --name alice --rm -it  --entrypoint /bin/bash --network=bridge   -p 0.0.0.0:8030-8037:8030-8037   -v /Users/nathanhouwaart/Documents/HBO-ICT/jaar3/Innovation/debug-environment/MNNU-Agent:/home/indy/MNNU-Agent   -e LOG_LEVEL= -e RUNMODE=docker -e DOCKERHOST=192.168.65.3 -e AGENT_PORT=8020 -e TRACE_TARGET=log -e TRACE_TAG=acapy.events -e TRACE_ENABLED=   demo-agent:1.0`
2. `cd MNNU_Agent/Demo`
3. `python3 demo-agent_1.py --port 8030 --identity Alice --ledger-ip 192.168.65.3 --seed d_000000000000000000000000Test01 --wallet-name Test01.Wallet --wallet-key test123`

### Start Agent 2
1. `docker run --name faber --rm -it  --entrypoint /bin/bash --network=bridge   -p 0.0.0.0:8020-8027:8020-8027   -v /Users/nathanhouwaart/Documents/HBO-ICT/jaar3/Innovation/debug-environment/MNNU-Agent:/home/indy/MNNU-Agent   -e LOG_LEVEL= -e RUNMODE=docker -e DOCKERHOST=192.168.65.3 -e AGENT_PORT=8020 -e TRACE_TARGET=log -e TRACE_TAG=acapy.events -e TRACE_ENABLED=   demo-agent:1.0`
2. `cd MNNU_Agent/Demo`
3. `python3 demo-agent_2.py --port 8020 --identity Nathan --ledger-ip 192.168.65.3 --seed d_000000000000000000000000Test00 --wallet-name Test00.Wallet --wallet-key test123`

