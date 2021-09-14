ExecutionResults:

### Admin user list all users

(platform9-assignment) vivekshinde@Viveks-MacBook-Air project % python main.py 
######################################
#  Welcome to VM reservation system  #
######################################

Please Provide the userid - 0
        1. List all VMs
        2. Get VM's filtered by user
        3. Checkout VM
        4. Checkin VM
        5. Exit
Select operation to be performed : 1
  ID  NAME    HOSTNAME      OWNER
----  ------  ----------  -------
   0  vm1     localhost         3
   1  vm2     localhost
   2  vm3     localhost
   3  vm4     localhost
   4  vm5     localhost         1

### Non-admin user creates VM - quota exceeded
(platform9-assignment) vivekshinde@Viveks-MacBook-Air project % python main.py
######################################
#  Welcome to VM reservation system  #
######################################

Please Provide the userid - 1
        1. Checkout VM
        2. Checkin VM
        3. Show my VMs
        4. Exit
Select operation to be performed : 1
Quota exceeded for user 1. Below VM are already owned by user
  ID  NAME    HOSTNAME      OWNER
----  ------  ----------  -------
   4  vm5     localhost         1

### VM checked out by normal user
(platform9-assignment) vivekshinde@Viveks-MacBook-Air project % python main.py
######################################
#  Welcome to VM reservation system  #
######################################

Please Provide the userid - 2
        1. Checkout VM
        2. Checkin VM
        3. Show my VMs
        4. Exit
Select operation to be performed : 1
VM is checked out successfully under your ownership.

VM details {'name': 'vm2', 'hostname': 'localhost', 'ip': '127.0.0.1', 'id': 1, 'owner': 2}

### Validate new assignment of VM
(platform9-assignment) vivekshinde@Viveks-MacBook-Air project % python main.py
######################################
#  Welcome to VM reservation system  #
######################################

Please Provide the userid - 0       
        1. List all VMs
        2. Get VM's filtered by user
        3. Checkout VM
        4. Checkin VM
        5. Exit
Select operation to be performed : 1
  ID  NAME    HOSTNAME      OWNER
----  ------  ----------  -------
   0  vm1     localhost         3
   1  vm2     localhost         2
   2  vm3     localhost
   3  vm4     localhost
   4  vm5     localhost         1

### Show user their existing VMs
(platform9-assignment) vivekshinde@Viveks-MacBook-Air project % python main.py
######################################
#  Welcome to VM reservation system  #
######################################

Please Provide the userid - 3
        1. Checkout VM
        2. Checkin VM
        3. Show my VMs
        4. Exit
Select operation to be performed : 3
  ID  NAME    HOSTNAME      OWNER
----  ------  ----------  -------
   0  vm1     localhost         3

### VM submitted back to system by user
(platform9-assignment) vivekshinde@Viveks-MacBook-Air project % python main.py
######################################
#  Welcome to VM reservation system  #
######################################

Please Provide the userid - 3
        1. Checkout VM
        2. Checkin VM
        3. Show my VMs
        4. Exit
Select operation to be performed : 2
  ID  NAME    HOSTNAME      OWNER
----  ------  ----------  -------
   0  vm1     localhost         3
VM is checked in successfully from your ownership.
VM details {'name': 'vm1', 'hostname': 'localhost', 'ip': '127.0.0.1', 'id': 0, 'owner': None}


### Error on Invalid choice 
(platform9-assignment) vivekshinde@Viveks-MacBook-Air project % python main.py
######################################
#  Welcome to VM reservation system  #
######################################

Please Provide the userid - o

Invalid userid. Please provide your valid uid
(platform9-assignment) vivekshinde@Viveks-MacBook-Air project % python main.py
######################################
#  Welcome to VM reservation system  #
######################################

Please Provide the userid - 0
        1. List all VMs
        2. Get VM's filtered by user
        3. Checkout VM
        4. Checkin VM
        5. Exit
Select operation to be performed : 1
  ID  NAME    HOSTNAME      OWNER
----  ------  ----------  -------
   0  vm1     localhost
   1  vm2     localhost         2
   2  vm3     localhost
   3  vm4     localhost
   4  vm5     localhost         1
