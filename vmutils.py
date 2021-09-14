###########################################################
# Description : Utilities to suport main reservation system
# Author : Vivek Shinde
###########################################################
import inspect
import logging
import sys
import os
import paramiko
from tabulate import tabulate
import json
from termcolor import colored

def list_all_vms(vm_data, user_details, users_data):
    """
    Utility function for users with admin role to list all the VM's  of all users.
    """    
    logging.debug(f'Inside function - ({sys.modules[__name__]}) {inspect.stack()[0][3]}')
    vm_data_list = [[vm["id"], vm["name"], vm["hostname"], vm["owner"]] for vm in vm_data["virtualMachines"]]
    print (tabulate(vm_data_list, headers=["ID", "NAME", "HOSTNAME", "OWNER"]))

def list_vm_by_user(vm_data, user_details, users_data):
    """
    Utility function for users with admin role to list all the VM's of any user.
    """
    logging.debug(f'Inside function - ({sys.modules[__name__]}) {inspect.stack()[0][3]}')
    while True:
        uid_to_search = int(input('Provide UID to search VMs under ownership : '))
        if uid_to_search not in [ x["id"] for x in users_data["users"]]:
            logging.debug(f'userid {uid_to_search} does not exist in users database')
            print(f'userid {uid_to_search} does not exist in users database')
        else:
            break
    vm_data_list = [[vm["id"], vm["name"], vm["hostname"], vm["owner"]] for vm in vm_data["virtualMachines"] if vm["owner"] == uid_to_search]
    print (tabulate(vm_data_list, headers=["ID", "NAME", "HOSTNAME", "OWNER"]))    

def writejsonData(jdata, jfile):
    """
    Helper function to update the data back in the database. In our case, data is in json, in real world, it might be required to be done using Cloud API.
    """
    logging.debug(f'Writing data to file {jfile}')
    with open(jfile, 'w') as jdatafile:
        json.dump(jdata, jdatafile)

def checkout_vm(vm_data, user_details, users_data):
    """
    This function is used to perform the reservation of the available VMs
    - Checks if the user have free quota available 
    - Checks if there are any free VMs in the system
    """
    logging.debug(f'Inside function - ({sys.modules[__name__]}) {inspect.stack()[0][3]}')
    current_usage = [[vm["id"], vm["name"], vm["hostname"], vm["owner"]] for vm in vm_data["virtualMachines"] if vm["owner"] == user_details["id"]]
    
    if len(current_usage) >= user_details["quota"]:
        print(f'Quota exceeded for user {user_details["id"]}. Below VM are already owned by user')
        logging.warn(f'Quota exceeded for user {user_details["id"]}. Below VM are already owned by user')
        print (tabulate(current_usage, headers=["ID", "NAME", "HOSTNAME", "OWNER"]))
        print()
        return  
    
    allocated = False

    for vm in vm_data["virtualMachines"]:
        if vm["owner"] == None:
            vm["owner"] = user_details["id"]
            allocated = True
            print(f'VM is checked out successfully under your ownership.')
            logging.info(f'VM is checked out successfully under your ownership.')
            print()
            print(f'VM details {vm}')
            break
    if allocated == True:
        writejsonData(vm_data, 'vmdata.json')
        

def checkin_vm(vm_data, user_details, users_data):
    """
    This function performs the task of returning the VM back to the system
    - Checks how many VMs are owned by user
       - If =0, do nothing and show msg to user
       - If =1, perform the required cleanup and return the VM to system 
       - If >1, show the list of owned VMs and ask user to select the VM to be returned to system (Performs cleanup on selected VM and then returns)
    """
    logging.debug(f'Inside function - ({sys.modules[__name__]}) {inspect.stack()[0][3]}')
    current_usage = [[vm["id"], vm["name"], vm["hostname"], vm["owner"]] for vm in vm_data["virtualMachines"] if vm["owner"] == user_details["id"]]
    print (tabulate(current_usage, headers=["ID", "NAME", "HOSTNAME", "OWNER"]))
    if len(current_usage) == 1:
        vm_id = current_usage[0][0]
    elif len(current_usage) >1:
        vm_id = int(input('Provide VM ID to be checked in :')) 
    else:
        print('No VM under your ownership')
        return
    
    deallocated = False
    for vm in vm_data["virtualMachines"]:
        if vm["id"] == vm_id:
            vm["owner"] = None
            deallocated = True
            vm_cleanup(vm["hostname"])
            print(f'VM is checked in successfully from your ownership.')
            print(f'VM details {vm}')
            break

    if deallocated == True:
        writejsonData(vm_data, 'vmdata.json')


def filter_vm_by_user(vm_data, user_details, users_data):
    """
    This function is used to show VM's under user ownership
    """
    logging.debug(f'Inside function - ({sys.modules[__name__]}) {inspect.stack()[0][3]}')
    current_usage = [[vm["id"], vm["name"], vm["hostname"], vm["owner"]] for vm in vm_data["virtualMachines"] if vm["owner"] == user_details["id"]]
    print (tabulate(current_usage, headers=["ID", "NAME", "HOSTNAME", "OWNER"]))    

def vm_cleanup(server_hostname):
    """
    This function is used to perform cleanup of the VM before being returned to the reservation system
    """
    logging.debug(f'Inside function - ({sys.modules[__name__]}) {inspect.stack()[0][3]}')
    # NOTE : This code picks the credentials from environment variable for project purpose, 
    # Ideally, in production grade systems, it should come from some secret manager like 
    # jenkins credentials or vault or some secret manager.
    try:
        sshclient = paramiko.SSHClient()
        cmd_to_execute = 'rm -rf /Users/vivekshinde/Learning/Python/platform9-assignment/tmp/*'
        sshclient.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        sshclient.connect(server_hostname, username=os.environ.get("username"), password=os.environ.get("password"))
        ssh_stdin, ssh_stdout, ssh_stderr = sshclient.exec_command(cmd_to_execute)
    except Exception as e: 
        logging.debug(f'An error occured')
        logging.debug(e)

if __name__ == "__main__":
  pass