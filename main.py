##########################################################################################
# Virtual Machine reservation system
# Author: Vivek Shinde
# Description : 
#    Datasource : 
#       Json files (users.json - For user data and vmdata.json to maintain VM data)
#       Data persistence is achived with file writeen to disc.
#       In real world, the data source might be cloud API's or some other source of truth
#    Usage: Just run the script and it will prompt for the user actions
#       1. Provide the user id when prompted
#       2. Based on user role, a list of menus will be prompted
#       3. Based on selected menu item, action will be performed
#    Logging: 
#       Only errors and user messages are prompted on the console
#       all other debug details are logged in log files
#    Authentication:
#       In this POC, authentication for users is ignoreed. In real system, only user authentication can be put in place
#       For the POC purpose, VM authneticaiton is done with username and password from env variables. IN real world, sensitive info like password or private key must come from secret manager like jenins creds or vault, cloud based secret manaers
############################################################################################

# External libraries import
import logging
import datetime
import json
import os
from termcolor import colored

# Import our user defined library with functions
import vmutils as vmu

# Logging configuration
tday = str(datetime.date.today())
logging.basicConfig(filename='vm-reservation-system' + tday + '.log', level=logging.DEBUG)

# Reusable print decorator for the welcome and exit scree
def header(msg):
  print('#' * (len(msg) + 6) )
  print(f'#  {msg}  #')
  print('#' * (len(msg) + 6) )
  print()

def promptMenus(menus):
  for idx,menu in enumerate(menus.keys()):
    print(f'\t{idx+1}. {menu}')

def exitFunction(*args):
  os._exit(0)

def mainDriverProgram():
  welcomeMsg = 'Welcome to VM reservation system'
  header(welcomeMsg) 
  
  # VM data - For this POC, data is used from json files. IN real world, data source might be diff
  with open('vmdata.json') as vm_jdata:
      vm_data = json.load(vm_jdata)

  # User data - For this POC, data is used from json files. IN real world, data source might be diff
  with open('users.json') as users_jdata:
      users_data = json.load(users_jdata)

  try:  
    user_id = int(input('Please Provide the userid - '))
  except Exception as err:
    logging.error('Invalid userid')
    print()
    print(colored('Invalid userid. Please provide your valid uid', 'red'))
    return

  user_details = [x for x in users_data['users'] if x['id'] == user_id]
  user_roles = user_details[0]['roles']
  
  if 'admin' in user_roles:
    logging.debug('User is admin')
    isAdmin = True
    menus = {'List all VMs': 'vmu.list_all_vms', 
      "Get VM's filtered by user": 'vmu.list_vm_by_user', 
      'Checkout VM': 'vmu.checkout_vm',
      'Checkin VM': 'vmu.checkin_vm',
      'Exit':'exitFunction'}
  else:
    logging.debug(f'User is non admin. User roles are {user_roles}')
    isAdmin = False
    menus = {'Checkout VM': 'vmu.checkout_vm',
    'Checkin VM': 'vmu.checkin_vm',
    'Show my VMs': 'vmu.filter_vm_by_user',
    'Exit': 'exitFunction'}
  
  promptMenus(menus)
  choice = int(input('Select operation to be performed : '))

  try:
    function_to_be_called = menus[list(menus.keys())[choice-1]]
  except IndexError:
    print(colored(f'Invalid choice. Please select valid choice from the list','red'))
  except Exception as e:
    logging.debug(e)
  else:
    logging.debug(f'Selected function - {function_to_be_called}')
    eval(function_to_be_called + "(vm_data, user_details[0], users_data)")

# Call to main driver code
logging.debug('Application started..') 
mainDriverProgram()