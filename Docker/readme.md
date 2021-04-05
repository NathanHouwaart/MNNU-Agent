# Docker Agent setup
This readme will give an instruction on how to build a docker agent image by using the [Dockerfile](Dockerfile) provided.

## Requirements
1. Docker is installed
2. Docker is running
3. 1gb of free (hard)disk space

## Build
In order to build the agent image, navigate to the [Docker](../Docker) directory and run the following command:
`docker build -f Dockerfile -t mnnu-agent:0.5 .`

- Where the -f flag specifies the file we want to use for the build process of a docker container
- Where the -t flag is used to give a tag to the container

The build process should not take longer than 5 minutes to complete (based on internet speed and such).

## Verify
In order to verify if the build went right, we are going to start a container with the freshly build image. To do so, use the following command:  
`docker run --rm -it mnnu-agent:0.5 bash`. This should start up a container. 

Then run the command `aca-py` in the bash terminal. If everything is installed correctly, the terminal should return the output as shown below.

```bash
root@ee2ac43de9fd:~# aca-py
usage: aca-py [-h] [-v] {provision,start} ...

positional arguments:
  {provision,start}
    provision        Provision an agent
    start            Start a new agent process

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      print application version and exit
```

If this succeeds, you can exit the container by entering `exit` in the bash command line.