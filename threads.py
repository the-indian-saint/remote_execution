
#this module handels the concurrency of the functions to execute commands on remote servers asynchonously

from remote_servers import remote_server
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


def get_hosts(servers):
    hosts = []
    for server_data in servers:
        #host = f"host-{str(server_data.index() + 1)}"
        host = remote_server(server_data['ip'], server_data['username'], server_data['password'], server_data['filename'])
        host.create_connection()
        hosts.append(host)
    return hosts

def exec_commands(hosts):
    print('Executing commands on remote servers...')

    with ThreadPoolExecutor() as executor:
        results = [executor.submit(host.deleteAndreplace) for host in hosts]
        for f in concurrent.futures.as_completed(results):
            print(f.result())

            


