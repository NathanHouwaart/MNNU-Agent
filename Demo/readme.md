# MNNU-Agent Python
This repository contains all the modules and tools needed to setup one or multiple cloud based agent containers.

## Summary 
An agent is a piece of software used to represent an individual or organisation in the digital world. For example, an individual might have a mobile agent app running on their smartphone. An agent helps individuals or organisations to interact with a ledger to store credentials, receive credentials, interact with other agents and much more. All agents (with rare exceptions) have secure storage for securing identity-related data including DIDs, keys and verifiable credentials. 

All Aries Agents have two logical components: a **framework** and a **controller**

![Aries Agent Architecture](../Resources/The_Logical_Components_of_an_Aries_Agent.png)


An Aries Agent Framework contains all the standard capabilities that enable an Aries agent to interact with its surroundings—ledgers, storage and other agents. The framework is something that is just embedded into the solution, and does not have to be maintained. The framework knows how to initiate connections, respond to requests, send messages and more. However, a framework needs to be told when to initiate a connection. It doesn’t know what response should be sent to a given request. It just sits there until it’s told what to do.

The controller is the component that, well, controls, an instance of an Aries framework’s behavior—the business rules for that particular instance of an agent. The controller is the part of a deployment that you build to create an Aries agent that handles your use case for responding to requests from other agents, and for initiating requests. For example:

In a mobile app, the controller is the user interface and how the person interacts with the user interface. As events come in, the user interface shows the person their options, and after input from the user, tells the framework how to respond to the event.
An issuer, such as Faber College’s agent, has a controller that integrates agent capabilities (requesting proofs, verifying them and issuing credentials) with enterprise systems, such as a Student Information System that tracks students and their grades. When Faber’s agent is interacting with Alice’s, and Alice’s requests an "I am a Faber Graduate" credential, it’s the controller that figures out if Alice has earned such a credential, and if so, what claims should be put into the credential. The controller also directs the agent to issue the credential.

The diagram below shows the Aries Agent architecture as exemplified by Aries Cloud Agent - Python (ACA-Py):

![Aries Agent Architecture](../Resources/Aries_Agent_Architecture__ACA-PY_.png)

The framework provides all of the core Aries functionality such as interacting with other agents and the ledger, managing secure storage, sending event notifications to, and receiving instructions from the controller. The controller executes the business logic that defines how that particular agent instance behaves—how it responds to the events it receives, and when to initiate events. The controller might be a web or native user interface for a person or it might be coded business rules driven by an enterprise system.

Between the two is a pair of notification interfaces.

- When the framework receives a message (an event) from the outside world, it sends a notification about the event to the controller so the controller can decide what to do.
- In turn, the controller sends a notification to the framework to tell the framework how to respond to the event.
- The same controller-to-framework notification interface is used when the controller wants the framework to initiate an action, such as sending a message to another agent.

What that means is that the framework is a complete dependency that must be included in the application. It is the controller that gives your agent its unique personality.

Lets take a look at what an agent looks like in the real world

![bob's agent](../Resources/bob-agent.png)

- Bob is a person who has a mobile Aries agent on his smartphone. He uses it to  message other agents, receive credentials from various agents, and uses those credentials to prove things about himself online.
- Bob’s smartphone app connects with a cloud-based Aries agent that routes messages to him. It too is Bob’s agent, but it’s one that is (most likely) run by a vendor.

This repository contains such cloud based agent.

In short a cloud based agent must be capable of:
- Starting up an instance of Aries Cloud Agent Framework (which is handled by the [Container Script](../Lib/container.py))
- Route events from the framework to the controller (which is handled by the [Webhook Server](../Lib/webhook_server.py))
- Send requests from the controller to the Aries Framework  (which is handled by the [API Hanlder](../Lib/api_handler.py))

## Requirements
In order to run an agent, a few things are required
1. Git (bash)
2. Docker
3. A working internet conneciton

## Run Demo
Running a demo is key in understanding the blockchain interaction. For this demo, two agents are setup

### Start Agent 1
1. `docker run --name Alice --rm -it  --entrypoint /bin/bash --network=bridge   -p 0.0.0.0:8030-8037:8030-8037   -v $(pwd):/home/indy/MNNU-Agent   -e LOG_LEVEL= -e RUNMODE=docker -e DOCKERHOST=192.168.65.3 -e AGENT_PORT=8020 -e TRACE_TARGET=log -e TRACE_TAG=acapy.events -e TRACE_ENABLED=   mnnu-agent:0.5`
2. `cd MNNU-Agent/Demo`
3. `python3 demo-agent.py --port 8030 --identity Alice --ledger-ip 192.168.65.3 --seed d_000000000000000000000000Test01 --wallet-name Test01.Wallet --wallet-key test123`

### Start Agent 2
1. `docker run --name Nathan --rm -it  --entrypoint /bin/bash --network=bridge   -p 0.0.0.0:8020-8027:8020-8027   -v $(pwd):/home/indy/MNNU-Agent   -e LOG_LEVEL= -e RUNMODE=docker -e DOCKERHOST=192.168.65.3 -e AGENT_PORT=8020 -e TRACE_TARGET=log -e TRACE_TAG=acapy.events -e TRACE_ENABLED=   mnnu-agent:0.5`
2. `cd MNNU-Agent/Demo`
3. `python3 demo-agent.py --port 8020 --identity Nathan --ledger-ip 192.168.65.3 --seed d_000000000000000000000000Test00 --wallet-name Test00.Wallet --wallet-key test123`



docker run --name Alice --rm -it --network=bridge -p 0.0.0.0:8030-8037:8030-8037 -v $(pwd):/root/MNNU-Agent -e LOG_LEVEL= -e RUNMODE=docker -e DOCKERHOST=192.168.65.3 -e AGENT_PORT=8020 -e TRACE_TARGET=log -e TRACE_TAG=acapy.events -e TRACE_ENABLED= mnnu-agent:0.5