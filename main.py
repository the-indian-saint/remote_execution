from threads import get_hosts, exec_commands 
from config import servers


def main(servers):
    hosts = get_hosts(servers)
    exec_commands(hosts)



main(servers)