import paramiko as pm
import os
import time
import logging

#this module creates a class for remote servers and persists information of each server as an object. 
#if username and password is not provided, the script will look for 'username' and 'password' environment variables
#filename can be different for each server 

#to reduce log size set level=logging.INFO in below config

logging.basicConfig(filename='servers.log', level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
                    )


class remote_server():

    def __init__(self, ip, username=None, password=None, filename=None):
        self.ip = ip
        if not username:
            self.username = os.environ['username']
        else:
            self.username = username
        if not password:
            self.password = os.environ['password']
        else:
            self.password = password
        self.filename = filename
        
    
    def create_connection(self):
        client = pm.SSHClient()
        client.set_missing_host_key_policy(pm.AutoAddPolicy())
        try:
            client.connect(hostname=self.ip, username=self.username, password=self.password)
            self.connection = client
            logging.info(f"Connection created to the host '{self.ip}'")
        except Exception as e:
            print(f"Unable to connect to host {self.ip}")
            print(e)
            self.connection = None
            logging.info(f"Connection colud not be created to the host '{self.ip}'")
            logging.debug(e)
        
    
    def remote_exec(self, cmd, waite=False): # function will waite for remote output
        if self.connection != None:
            start = time.perf_counter()
            try:
                client = self.connection
                print(f"executing '{cmd}' on '{self.ip}'")
                logging.info(f"Command = {cmd}")
                _ , stdout, stderr = client.exec_command(cmd)
                output = stdout.readlines()
                if waite == True:
                    exit_status = stdout.channel.recv_exit_status()
                    if exit_status == 0:
                        logging.debug(f"Output = {stderr.readlines()}")
                        logging.info(f"Error = {stdout.readlines()}")
                        return {'status_code': 0, "output":stdout.readlines()}
                if len(stderr.readlines()) > 0:
                    logging.debug(f"Error = {stderr.readlines()}")
                    end = time.perf_counter()
                    total_time = round(end - start, 2)
                    logging.info(f"Command took {total_time} second(s)")
                    logging.info("-------------------------------------------------------------------")
                    return {'status_code': 1, "output":stderr.readlines()}
                logging.info(f"Output = {stdout.readlines()}")
                #print(stdout.readlines())
                #print(stderr.readlines())
                end = time.perf_counter()
                total_time = round(end - start, 2)
                logging.info(f"Command took {total_time} second(s)")
                logging.info("-------------------------------------------------------------------")
                return {'status_code': 0, "output": output}
            except Exception as e:
                print(e)

    
    def deleteAndreplace(self):

        find_file = f'sudo updatedb && locate -e -r /{self.filename}$'
        path = self.remote_exec(find_file, waite=False)
        if path['status_code'] == 1:
            logging.warning(f"error {path['status_code']} for {find_file}")
            logging.debug(f"error = {path['output']}")
        elif len(path['output']) == 0:
            print(f"file '{self.filename}' does not exist on '{self.ip}'")
            logging.info(f"file '{self.filename}' does not exist on '{self.ip}'")
        else:
            print(f"file '{self.filename}' found at '{path['output'][0]}' on '{self.ip}'")
            logging.info(f"file '{self.filename}' found at '{path['output']}' on '{self.ip}'")
        
        #change the owner of the directory

        dir = path['output'][0].split('/')
        dir.pop()
        dirname = '/'.join([str(elem) for elem in dir])

        change_owner = f"chown {self.username} {dirname}"
        self.remote_exec(change_owner, waite=False)

        delete_file = f"rm -rf {path['output'][0]}"
        self.remote_exec(delete_file, waite=False)

        replace = f"echo deleted > {path['output'][0]}"
        self.remote_exec(replace, waite=False)

        print(f'File Replaced on {self.ip} :)')
        self.connection.close()
