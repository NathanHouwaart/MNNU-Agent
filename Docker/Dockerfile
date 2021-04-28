FROM bcgovimages/von-image:py36-1.16-0 AS BUILD_IMAGE

ENV ENABLE_PTVSD 0
ENV ENABLE_PYDEVD_PYCHARM 0
# ENV PYDEVD_PYCHARM_HOST "host.docker.internal"

USER root
RUN apt-get update
RUN cd ~/ && rm -r * 

RUN curl -L -o /bin/jq \
	https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 && \
	chmod ug+x /bin/jq

RUN cd ~ && \
    git clone --depth 1 --branch 0.6.0 https://github.com/hyperledger/aries-cloudagent-python && \
    cd aries-cloudagent-python && \
    python3 -m pip install --no-cache-dir -r requirements.txt -r requirements.dev.txt

RUN cd ~/aries-cloudagent-python && python3 -m pip install --no-cache-dir -r demo/requirements.txt
    
RUN cd ~/aries-cloudagent-python && \
    cp -a ./bin/. /bin/

RUN cd ~/aries-cloudagent-python && python3 setup.py install

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash && apt install nodejs -y && npm install -g localtunnel && npm prune --production

ADD . /home/indy/MNNU-Agent
WORKDIR /home/indy/MNNU-Agent/Demo


ENTRYPOINT ["bash", "-c", "--"]