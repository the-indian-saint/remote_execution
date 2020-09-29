Prerequisites - 

1) Make sure sshd service is running on the remote servers.
2) User being used has sudo permissions.
3) Make sure 'PubkeyAuthentication' is set to 'no' in '/etc/ssh/sshd_config'
4) Make sure user is not prompted for password while executing sudo commands by editing the visudo file.
5) Make sure a home directory exists for the user 
6) See commands.txt to know all the commands.
7) Make sure your local machine has netwrok/firewall level permissions to ssh into remote servers.

---------------------------------------------------------------------------------------------------------------

Operation -

1) Install Python 3.8 and PIP
2) Navigate in the directory and run pip install -r requirements.txt
3) Update config.py files with all server info.
4) Run 'main.py' by executing python main.py
5) Check all modules for specific task.
6) Logs can be found in servers.log

---------------------------------------------------------------------------------------------------------------