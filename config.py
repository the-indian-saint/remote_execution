#This script can execute commands on any number of servers asychronously and can be used to delete same or different
# files on remote servers.
# add more server configuration in following format in the server list

'''
{
    "ip" : str,            - Host Ip as a string
    "username" : str,      - Host Username   
    "password" : str,      - Host Password 
    "filename" : str       - File to be removed and replaced
}

'''

servers = [{'ip':'10.20.12.08', 'username':'admin', 'password':'Admin@123', 'filename':'reaper'},
           {'ip':'10.20.12.12', 'username':'admin', 'password':'Admin@123', 'filename':'reaper'},
           {'ip':'10.20.12.21', 'username':'admin', 'password':'Admin@123', 'filename':'reaper'},
           {'ip':'10.20.12.22', 'username':'admin', 'password':'Admin@123', 'filename':'reaper'},
           ]
