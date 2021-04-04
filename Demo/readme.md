# Local MNNU-Agent demo
This demo will help you set-up your own local MNNU-Agents that interact with a local ledger. We connect with a local ledger instead of a public one, because a local ledger will instantly update its webpage, so you can directly see what effects your commands have on a ledger. A public ledger should not behave any different, besides the instantaniousnes of the website.

## Requirements
In order to run an agent, a few things are required
1. Git (bash)
2. Docker
3. A working internet conneciton
4. A running local von Image

## Run Demo
The following steps will help you set-up and run the demo
### Setup VON-Network
TODO: readme updaten hier

### Setup Agents
1. In order to run the Demo, you must have build a Docker image with the provided [Dockerfile](../Docker/Dockerfile). The [readme](../Docker/readme.md) in the [Docker](../Docker/) directory will show you how to to that.
2. Once the image has been build, you are ready to start-up some agents. The [readme](../Docker/readme.md) for building the Docker image and running your first container showed that you can run a container with the argument: `docker run --rm -it mnnu-agent:0.5 bash`. However, for starting up an MNNU-Agent, we need to add a few more parameters.
    - Firstly, we want to add a `--name <name>` to the container. This way, it can be more easily found in the docker container explorer
    - Secondly, we want to add the `p <port(s):port(s):port(s)>` parameter to forward and expose specified docker ports to the outside world. This is needed so that the Docker container can interact with the World Wide Web.
    - Lastly, we want to add this repository, [The MNNU-Agent](../), to the docker container. The `-v <directory_to_mount:mount_point_in_image>` will help us achieve that.    

    A full fetched docker command to start a container might look something like this: `docker run --name Alice --rm -it -p 0.0.0.0:8030-8037:8030-8037   -v $(pwd):/home/indy/MNNU-Agent mnnu-agent:0.5 bash` where:
    - We have named the container Alice
    - We have exposed the portrange 8030-8037
    - We have mounted the MNNU-Agent repository to the /home/indy/MNNU-Agent directory
3. Start up a docker container for agent 1 with the following command: `docker run --name Alice --rm -it -p 0.0.0.0:8020-8027:8020-8027 -v $(pwd):/home/indy/MNNU-Agent mnnu-agent:0.5 bash`
    - Navigate to the Demo directory using the `cd MNNU-Agent/Demo` directory
    - Run the agent with the following command `python3 demo-agent.py --port 8020 --identity Alice --ledger-ip 192.168.65.3 --seed d_000000000000000000000000Test01 --wallet-name Test01.Wallet --wallet-key test123`. 
    - **Note** that the --port parameter specified matches the beginning of the exposed Docker container ports we specified during the container startup.
4. Then Start up a docker container for agent 2 with the following command: `docker run --name Nathan --rm -it -p 0.0.0.0:8030-8037:8030-8037   -v $(pwd):/home/indy/MNNU-Agent mnnu-agent:0.5 bash`
    - Navigate to the Demo directory using the `cd MNNU-Agent/Demo` directory
    - Run the agent with the following command `python3 demo-agent.py --port 8030 --identity Nathan --ledger-ip 192.168.65.3 --seed d_000000000000000000000000Test00 --wallet-name Test00.Wallet --wallet-key test123`. 
    - **Note** that the --port parameter specified matches the beginning of the exposed Docker container ports we specified during the container startup.
5. With both agents running, the command line terminal of both agents should look something like this
    - Alice agent: [output file](../Resources/Alice_Agent_startup_output.md)
    - Nathan agent: [output file](../Resources/Nathan_Agent_startup_output.md)
6. You can start-up more agents as you wish. When you do so, note a few things:
    - Specify a portrange that is not already in use. In this case port 8020...8027 and 8030..8037 are already in use, so anything above 8040 will work properly.
    - The --seed and --wallet-name must be uniqe and cannot be the same as onces already specified. Otherwise you migt get an invalid key error

### Using the Agents to interact with each other
Once both (or more) agents have been initialised, the terminals will show a prompt that looks something like:
```
1. Show Connections
2. Generate invitation
3. Receive inivtaiotn
4. Send Message
5. Get connection state
6. Exit
```
Every option will be discussed in a section below

#### 1. Show connections
This method is used to show any type of connections of the Agent. It will show pending and active connections and who that connection is for. When starting a new agent, selecting this key will result in an empty list of connections like so:
```console
demo-agent.py:37                |  {
    "results": []
} 
demo-agent.py:38                |  Total connections: 0 
```
Once you have generated an invitation, or accepted an invitation, the connection list will show that.
```console
demo-agent.py:37                |  {
    "results": [
        {
            "accept": "auto",
            "alias": "Alice",
            "connection_id": "c9b8a28a-c919-4609-8c18-f7c0d23a18ad",
            "created_at": "2021-04-04 14:37:31.488619Z",
            "invitation_key": "C24APxgyG6JRYTUWpVLBpxMgQ5gMZmBffJPbu64QJqyi",
            "invitation_mode": "once",
            "rfc23_state": "invitation-sent",
            "routing_state": "none",
            "state": "invitation",
            "their_role": "invitee",
            "updated_at": "2021-04-04 14:37:31.488619Z"
        }
    ]
} 
demo-agent.py:38                |  Total connections: 1 
```
The rfc23_state will tell the current state of the connection. In the example above the connection is still at an "invitation-sent" stage. Once the invitation has been accepted by another agent, the `show connections` option will list it accordingly:
```console
demo-agent.py:37                |  {
    "results": [
        {
            "accept": "auto",
            "alias": "Alice",
            "connection_id": "c9b8a28a-c919-4609-8c18-f7c0d23a18ad",
            "created_at": "2021-04-04 14:37:31.488619Z",
            "invitation_key": "C24APxgyG6JRYTUWpVLBpxMgQ5gMZmBffJPbu64QJqyi",
            "invitation_mode": "once",
            "my_did": "XC9WpgQeHuC1FqzEG8BDhs",
            "rfc23_state": "completed",
            "routing_state": "none",
            "state": "active",
            "their_did": "C5FnkT1TAqHCzHj8wCkAh",
            "their_label": "Nathan.Agent",
            "their_role": "invitee",
            "updated_at": "2021-04-04 14:43:01.793435Z"
        }
    ]
} 
demo-agent.py:38                |  Total connections: 1 
```
Note that the rfc23_state is now listed as "completed", indicating that the connection is completed. Also note that, when using the `show connections` method of the agent that you have started a connection with, will list the connection as well:
```console
demo-agent.py:37                |  {
    "results": [
        {
            "accept": "auto",
            "alias": "Nathan",
            "connection_id": "bdeb8c05-af0f-40b1-a2d4-5716dd2ade62",
            "created_at": "2021-04-04 14:43:01.121897Z",
            "invitation_key": "C24APxgyG6JRYTUWpVLBpxMgQ5gMZmBffJPbu64QJqyi",
            "invitation_mode": "once",
            "my_did": "C5FnkT1TAqHCzHj8wCkAh",
            "request_id": "3c8a5d1e-71ab-4946-8279-06fc7ab8a15a",
            "rfc23_state": "completed",
            "routing_state": "none",
            "state": "active",
            "their_did": "XC9WpgQeHuC1FqzEG8BDhs",
            "their_label": "Alice.Agent",
            "their_role": "inviter",
            "updated_at": "2021-04-04 14:43:02.043511Z"
        }
    ]
} 
demo-agent.py:38                |  Total connections: 1 
```

#### 2. Generate invitations
This option is used to generate an invitation to initiate a new connection with an agent. if this option is selected, the terminal will spit out a bunch of things. First, it will show the invitation data, which looks like a large string of random charcters. Then, a QR-Code is printed out, which could be used to scan with a phone. Lastly, the webhook server will generate a callback which is logged to the console. 

Remember the architecture of an Aries Agent? Where the controller makes API calls to the framework and the framework will send events to the controller (explained in this [readme](../readme.md))? Well, in this case, the controller sends a request to the Aries Framework to generate an invitation. This can be found in the following files [agent.py](../Lib/agent.py) and [api_handler.py](../Lib/api_handler.py). The framework will do its magic and generates an invitation. 

However, in order to communicate that information back to our contoller, the framework will generate an event. This is where the webhook server comes in. The webhook server will listen for incoming events and tries to handle them accordingly. In this case, it will just print the information out to the terminal. 

The terminal output when generating an invitation should look somrthing like this (could be different when using a different seed):

```console
http://192.168.65.3:8021/connections/create-invitation {'alias': 'Alice', 'auto_accept': 'true', 'multi_use': 'false'}
agent.py:119                    |  Use the following JSON to accept the invite from another demo agent. Or use the QR code to connect from a mobile agent. 
agent.py:120                    |  Invitation Data: "eyJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9jb25uZWN0aW9ucy8xLjAvaW52aXRhdGlvbiIsICJAaWQiOiAiMDk1NWY5ZmYtN2M1Ni00YzVlLWI5YjctMWMzZWJjMTM0YzAzIiwgInJlY2lwaWVudEtleXMiOiBbIjNBd29ZaWM2VXk4MlByOEhxZU5TbTdhaFVIUEpRdURLTG9DcFU3dWs1NXdRIl0sICJzZXJ2aWNlRW5kcG9pbnQiOiAiaHR0cDovLzE5Mi4xNjguNjUuMzo4MDIwIiwgImxhYmVsIjogIkFsaWNlLkFnZW50In0=" 
█▀▀▀▀▀▀▀█▀▀▀█▀██▀▀▀▀███▀▀▀▀▀██▀▀█▀▀████▀█▀▀▀█▀█▀██▀█▀▀█▀▀██▀███▀█▀█▀▀▀▀▀▀▀█
█ █▀▀▀█ ██▀▄▀  █▀█▀▄▀ ▄▀█▀ ▄█▀▄▄ ▀██ ▀▄███▀▀▀▀▀█  ▀▀▀█▄▀▄  ███▀▄███ █▀▀▀█ █
█ █   █ █ ▀▀ ▀▀▀███▄▄▀█ █ ▀▀ ▀ ▀█▀ ▄███ ▀▄▀▀▄▀ ▀    ▄▄▄ █ █ ▄██▄ ▀█ █   █ █
█ ▀▀▀▀▀ █ █▀▄ ▄▀█ ▄▀█ ▄ █ █▀█ █▀█▀▄▀█▀▄▀▄ ▄ █ █▀█ ▄▀▄ █▀▄▀▄ ▄ ▄ █▀█ ▀▀▀▀▀ █
█▀███▀█▀▀ ▄▀ ▄  ▀▄█▀▄▄██▀ ▀▀▀ ▀▄  ▄   ██ █▄█▀ ▀▀▀ ▀ ▄██▀▀ ▀▄▄▄▀█ ▀▀▀▀▀▀██▀█
█▄█ ▄ ▄▀▀▄█ ▀▀█ ▄▀ █▀ ▀  ▀▄█▄   █▀ █ ▄█▄ ▀▄▄ ▄█▄▀ ▄▀ ▀▀▀▀▄▀█▄▀▄ █▄▄▄▄▀█▀███
█▄▄█ █▀▀▄▀ ▄█  ▀█▀██▀▀▄  █ ▀█▀▀ ▄  ██  ▀▀█▄▄▀▄▄█▀██ █▀ ▀ ▄ ▀▄ ██▀ ▄▄ ▀█▄█ █
█ ▀▄▄ █▀▄█▄  ▄██▄ ██▀█▀▄  ███▄▄ █ ▄██▀█▄▄▀   █  █  █▀ ▀▀█▀▀███ ▀▀▀▄▄  ▄  ██
█▀▀█▄▀ ▀ ▀█▄ ▀█ ▄█ ▄▄█▄█▄ ▄▀ █ ▀█  ▄▀ █▀██▄▀ █▄   █ ▄█▄█▀ ▄█▄▄▀▀▀  ▀██▀▄▀██
█▄▄ ██▀▀█▀█ ▄▄▀▄▀▀▄▀█ ▄█▄█ ▄█▀█▄  █▀▀▀ ▄▀▄█ ██▀ ▀▀  █ ▀ ▄▄▀▄▀▄▄▀▀▄▄█▄  ▄█▄█
█▄▀██▄ ▀▀█▀▀  ▄█▀█ █▀ █  █▀█▀▀▀▄██▄▀ █ █  ▄█ ██▀▄▄ ████▀  ▀▀█ ▄▄█ ▄▄ ▀▄ ▄▄█
█▄ ▄█▀█▀▄ █▄▀█▀█▄█▄█ ▀▄ ▄▄▄▀▀▀▄▄ ▀▄▀█▀▀▄█▄ ▄██▀ █▄▄   █▀  ██   ▄█▄██▄▀▀▄▄▄█
█▄ ▄ ▀▀▀  ▄██ ▀▄▄▄▀▀▄█▄▄▀ ▀▀ ▀▀▀█ ▄▄  ▄▀ ▄▄▄█  ▀▀ ▀▄█▀▄ ▀ █▄▄▄  ▄  ▀ ▀▀ ▀ █
█▄▀▀▄ █▀█ ▄▀█▀▀▀▀▄▄▄▄  ▀█ █▀█   █  █  ▀▄▄█  ▀ █▀█ ▄   ▀▀▄██ ▀▀ ▀  █▀█ ▀  ██
█     ▀▀▀ █▀    ███▄ █▀▄█ ▀▀▀  ▀█▀ █  █  █ ▀▄ ▀▀▀ ▀██▀▄▄▀ ▄▀▄▄ █▄ ▀▀▀ ▀ ███
█▀ ▀ ▄█▀ █▄  █▄▀ █ █▄▀▀ ▄▀▄▀▀█ ▄█  ▀▀▄█▄ ▄  ▄▀█▄▀▀  ▄▀█████▄ ▀▄  █▄██ █ █▄█
█▀▀▄▀▄ ▀▄▄▄ ▄▄▀██▀█▄█▀▀█▄▄▄▄▄ ▄▀█▀▄▀ ▀▀▄▀▄█▀ ▄▄█▄▀▄▀██▀   ▄▄█ ▀██ ▀▀█   ▄██
█▀ ▄█ █▀▀  ▀▀  ▀█▄▄▀ ▄▄▄▄ ▄▀▄▀▄▄█  ▀▀█▀▄▀▀ ▄▄ ▀█ █ ▄  █ ▀▀██ █▄ ▄▀██▄▀█▀▄▄█
█▀▀▀▀▄▀▀▀▀▀█ █   ▀▀  █▄█▄▄▄ █ ▄▄  ▄  ▀▀█ ▄   █ ▄ ▀▀▄███  █▄▀▄ █▄█▄▀██ ▀ █▀█
██ ▄█▄ ▀█▄▀▀ █▄▀  ▄▄▀▀▀█ ████   ▄█ █▀▀█▄ █ ▄  █  █▄▀▄█▀  ▄▀▄▄▄▄ ▀▄█▀  ▀████
█▀▄▄  ▄▀██▀▄█ █ ▀██▄▀ ▀▀ █▄█▄▀ ██▀█▄ ▀ ▀ ▄▀▀▀███▄▄▄▀▄███▀▄▄▄█▄ ▀▀▄ ██▀▀▄███
██ ██ ▀▀▀ ▄█  ▄ █  ▄ ██ ▀▄  ▀█ ▄ ▄ ▀▄█▀▄▄  ▄▄▄█▄  ▄ ▄▀█   ▀▄█▄ ▀▀██▄██ ▀███
█ ▄██▀ ▀▀▀▀█▄▄ ▀▀▄ ▀▄▀  █ ▀▀▀▀  █ █▀ ▀▄█▀▄▀█▄▀▀▀ ▀█▄██ ▀▀  █▄▄ ▀▀ ▀▀  ▀▄███
██  ▄ █▀█  ▄▀ ▀▀▀▄▀▀ ▄▄▄  █▀█  ▄ ▄▄▀    ▄ █ █ █▀█ ▄▀▀▄▀▀  ▀▄█▄  ▄ █▀█ ▀  ██
█▄▄ ▄ ▀▀▀  ▀ █ ▀ ▄▄██▀█ ▀ ▀▀▀ ▄   ▀  ▀█ ██▀▄█ ▀▀▀ █ ██ █  ▄ █ ▄▀█ ▀▀▀ ▀▄▀▀█
█ ▄  ▄▀▀ ▀▀ ▄▄▀ █▀█▄█▄ ▀▄▀▀▀▄   ▀█ █▄█▀ ▀ █ ▄█▀█▄▀▄▀  █▀ ▀▀▄▄ ▄▀  ▀▄▀▄ ██▄█
█  ▄▄▀ ▀▀ ▄▄  ▀█▀  █ ▀▄▄██  █▄█▄█ █▀ ▀ ▄ ▄▀ ▄█ █▄  ▀██ █ ▀█▄███▄▄▀▀  ▀▀ ▀ █
█ █▄█▀ ▀▄█ ▄▀  █  ▀▀█▀▀▄▄  ▄ █ █    ▀███ ▄▀   ▀█▄ ▄▀ ▄█▀▄▄▀██▀ █▀ ▀ ▀ ▀█▄██
██▄ ▀  ▀█▄▀ █  ▀▄▄▀██▄▄ ▀▀ █▀▀ ▀ ▀█▄█▀█▀▄▄▀▄█▀██ ▀████▀▀  █████ ▀█  ███ ███
████▀ ▀▀█▄▀ ▀▀▄█  ███▄█▄█    ▄▄▄█▄ █ ▄  ▀    ▀▀▄██▄▀█▄▀ █ █ ▀▀▄ ▀ ▀▀▄ █▀▄▄█
█▀▄█  ▀▀█▀ ▀▄ ██▀█▀▄▀▄▄ ▀  █▄▄███▀ ▄ ▀▀▄ ▄▄█▀█▄▀▄ ▀██  ▄▀  █▄ ▄█▄█  ██▀▄ ▄█
█  ▄ ▄ ▀ ▄▄█▀▄█▄ █ █▀ ▀█ ██▄▄▀▄▄▀█▄▀▄█▀▄█▀█ ▄   ██ ▀ ▀▀▀█▀██  ▄  ▄█ ▀ ▀ ▄██
█▀██▄ █▀▀  █▀▀▀▄▀▀   █▄▀▄▀ ▀▀  ▀█ ▀█▀ ▄▄ █ ▀▄▀ ▀  ▀▄██▄▄ ██▄█ █▀█▀ ▀ ▀█▄█ █
█▀▀▀▀▀▀▀█    ▀ ▀▀▀▀█ █▄▀▄ █▀█   █▄ ▀  █ ▄▀▄▄▄ █▀█   ▄▀▀▀ ▄████  ▄ █▀█ ▄▀▄▄█
█ █▀▀▀█ █▀ ██▄█▀▀▀ ▀█ ▀█▄ ▀▀▀ ▄   ▀█▀▀▀▄▀█▀   ▀▀▀ █▀▄▀▀ ▀▄ █▄▄█ █ ▀▀▀ ▀▄ ▀█
█ █   █ ██▀▄▄  ▄▀▄ ▀█▄  ▀████▄▄▄▀█▄▀▄▄▀▄▄▀▄▄▄▀▄▄ █  ▄▀▀ ██▀▄▄ ▄  █▄ ▀▄▀▄▀▄█
█ ▀▀▀▀▀ █▀ ▀▀▄ ▄▄█▀█▄█ ██ ▀▀█▄ ▀  █▄  █  █▀▄▀   █ ▄███▀▄ ▄█ █  █▀█ ▀█ █▄ ▀█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
webhook_server.py:68            |  Topic connections 
webhook_server.py:80            |  Agent called controller webhook: %s%s%s%s handle_connectio
ns 
POST http://192.168.65.3:8022/webhooks/topic/connections/   with payload: 
{
    "connection_id": "a93b6c43-b38d-46f4-bf8e-22d952039de7",
    "invitation_mode": "once",
    "accept": "auto",
    "invitation_key": "3AwoYic6Uy82Pr8HqeNSm7ahUHPJQuDKLoCpU7uk55wQ",
    "rfc23_state": "invitation-sent",
    "created_at": "2021-04-04 14:43:09.172866Z",
    "updated_at": "2021-04-04 14:43:09.172866Z",
    "routing_state": "none",
    "alias": "Alice",
    "state": "invitation",
    "their_role": "invitee"
}
 
webhook_server.py:95            |  Handle connections
```

When generating the invitation, the information listed after `Invitation Data: ` is the most important. This is the invitation data that you will need to provide to the other agent. In this case, the invitation data is:
```
agent.py:120                    |  Invitation Data: "eyJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9jb25uZWN0aW9ucy8xLjAvaW52aXRhdGlvbiIsICJAaWQiOiAiMDk1NWY5ZmYtN2M1Ni00YzVlLWI5YjctMWMzZWJjMTM0YzAzIiwgInJlY2lwaWVudEtleXMiOiBbIjNBd29ZaWM2VXk4MlByOEhxZU5TbTdhaFVIUEpRdURLTG9DcFU3dWs1NXdRIl0sICJzZXJ2aWNlRW5kcG9pbnQiOiAiaHR0cDovLzE5Mi4xNjguNjUuMzo4MDIwIiwgImxhYmVsIjogIkFsaWNlLkFnZW50In0=" 
```

#### 3. Receive invitation
This option will help you receive an invitation from another Agent. When selecting this option, the terminal will prompt for `Invite details`. Provide the `Invitation data` created by another agent with the `Generate invitation` method. If you dont know what the invitation data is, refer to Section 2. Generate invitation.

After you have entered the invite details, the terminal will prompt you with a question `Auto accept invitation? n/y: `. This referres to: do you want to auto-accept the invitation, or do you just want to receive the invitation. In this case, enter `y` to auto accept the connection.

Now both agents will output data in their terminals indicating that they are making a connection. When no errors present themselves, the connection between two agents is established. To confirm this, you can use the `Show Connections` method to list all connections of the agent, including completed (active) onces.

**Fun fact:** As an agent, you can receive and accept your own invitation to make a connection with yourself!

#### 4. Send Message
With this option, you are able to send a message to any active connections. When selecting this option, you will be promted to input a connection id. This conenction id can be read in the terminal after receiving and accepting an invitation:
```console
POST http://192.168.65.3:8032/webhooks/topic/connections/   with payload: 
{
    "invitation_mode": "once",
    "invitation_key": "C24APxgyG6JRYTUWpVLBpxMgQ5gMZmBffJPbu64QJqyi",
    "created_at": "2021-04-04 14:43:01.121897Z",
    "updated_at": "2021-04-04 14:43:02.043511Z",
    "rfc23_state": "completed",
    "state": "active",
    "their_role": "inviter",
    "routing_state": "none",
    "connection_id": "bdeb8c05-af0f-40b1-a2d4-5716dd2ade62",
    "their_did": "XC9WpgQeHuC1FqzEG8BDhs",
    "alias": "Nathan",
    "request_id": "3c8a5d1e-71ab-4946-8279-06fc7ab8a15a",
    "my_did": "C5FnkT1TAqHCzHj8wCkAh",
    "accept": "auto",
    "their_label": "Alice.Agent"
}
 
webhook_server.py:95            |  Handle connections 
```
In this case, the connection id is `bdeb8c05-af0f-40b1-a2d4-5716dd2ade62`. 

**Note that when two agents are connected with each other, their connection id is not the same. One agent might have a connection id of `bdeb8c05-af0f-40b1-a2d4-5716dd2ade62`, whilst the other agent has a connection id of `c9b8a28a-c919-4609-8c18-f7c0d23a18ad`. They refer to the same connection, but are different for both agents.**

After entering the connection id, the terminal will prompt you to enter a message. Type anything you like and press return. An example might be:
```
Send message to <connection id> :bdeb8c05-af0f-40b1-a2d4-5716dd2ade62                       
Message <message>:Hello Alice
```

The agent you send the message to will now receive the message:
```
webhook_server.py:68            |  Topic basicmessages 
webhook_server.py:80            |  Agent called controller webhook: %s%s%s%s handle_basicmess
ages 
POST http://192.168.65.3:8022/webhooks/topic/basicmessages/   with payload: 
{
    "connection_id": "c9b8a28a-c919-4609-8c18-f7c0d23a18ad",
    "message_id": "d0801551-4132-459f-a8a6-6a6846922d55",
    "content": "Hello Alice",
    "state": "received"
}
 
webhook_server.py:92            |  Received message: Hello Alice
```
And the agent that has send the message will receive a confirmation that the message was received:

```
webhook_server.py:68            |  Topic basicmessages 
webhook_server.py:80            |  Agent called controller webhook: %s%s%s%s handle_basicmes
sages 
POST http://192.168.65.3:8032/webhooks/topic/basicmessages/   with payload: 
{
    "connection_id": "bdeb8c05-af0f-40b1-a2d4-5716dd2ade62",
    "message_id": "c591f066-731c-4fe5-996c-9d4e5d812a49",
    "content": "Alice.Agent received your message",
    "state": "received"
}
 
webhook_server.py:92            |  Received message: Alice.Agent received your message 
```

#### 5. Get connection state



#### 6. Exit
This option will terminate the agent and container. It shuts down the webhook server, the docker container and the client session. If everything went correctly, the terminal should look like:
```                                                                                         
agent.py:169                    |  Shutting down Alice 
webhook_server.py:98            |  Shutting down web hooks site 
container.py:94                 |  Shutting down agent 

Shutting down
container.py:101                |  Docker Container exited with return code 0 
```





