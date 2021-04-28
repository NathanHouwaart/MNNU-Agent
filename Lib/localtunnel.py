import asyncio

class LocalTunnel():
    def __init__(self, port: str, subdomain: str=None):
        self.port = port
        self.subdomain = subdomain
        self.process_done = asyncio.Future()
        self.tunnel_url = None

    async def start_local_tunnel(self):
            agent_args = ['lt', '--port', str(self.port)]
            agent_args.extend([] if self.subdomain is None else  ['--subdomain', self.subdomain])
            print(agent_args)
            self.server_tunnel_ps = await asyncio.create_subprocess_exec(  # TODO: Catch invalid key/ arguments error.
                *agent_args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=None
            )

            await self.__wait_localtunnel_started(self.server_tunnel_ps)

    async def __wait_localtunnel_started(self, process):
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            try:
                line = line.decode("ascii")
                # print(line, end="")
                if "your url is:" in line:
                    print("tunnel started")
                    # user_object = await self.database.get_user(user)
                    self.tunnel_url = line.replace(" ", "").replace("\n","").split(":", 1)[1]
                    self.process_done.set_result(None)
                    break
            except Exception as e:
                continue


async def run_server():
    tunnel = LocalTunnel(port, subdomain)
    await tunnel.start_local_tunnel()
    print(tunnel.tunnel_url)


if __name__ == '__main__':
    port      = 8000
    subdomain = None #"test_local_port_1234"

    loop = asyncio.get_event_loop()
    loop.create_task(run_server())
    loop.run_forever()
