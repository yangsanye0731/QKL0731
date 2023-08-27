# server.py
import rpyc
import subprocess


class RemoteCommandsService(rpyc.Service):
    def on_connect(self, conn):
        print("Client connected.")

    def on_disconnect(self, conn):
        print("Client disconnected.")

    def exposed_execute_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            print(result)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output}"


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(RemoteCommandsService, port=18861)
    server.start()
