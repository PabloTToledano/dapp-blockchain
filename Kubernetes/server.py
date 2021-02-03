#!/usr/bin/python3
import os
import sys
import json
import yaml
import copy
import subprocess
import webbrowser
import pprint
import shlex

PATH_ENVIRONMENT_TEMPLATE = 'environments/environment_template.yaml'
PATH_ENVIRONMENT = 'environments/environment.yaml'
PATH_ENVIRONMENT_DEL = 'environments/environment_del.yaml' 
PATH_BLOCKCHAININIT = './blockchainit'
PATH_BLOCKCHAINDEL = './blockchaindel' 
PORT_FORWARD = None
minikube = False

def load_environment(environment_path):
    with open(environment_path) as file:
        environment = yaml.load(file,Loader=yaml.FullLoader)
    return environment

def write_environment(new_environment):
    with open(PATH_ENVIRONMENT, "w") as file:
        environment = yaml.dump(new_environment, file)   

def write_environment_del(new_environment):
    with open(PATH_ENVIRONMENT_DEL, "w") as file:
        environment = yaml.dump(new_environment, file) 

def create_k8s_yaml():
    os.system(PATH_BLOCKCHAININIT)

def create_k8s_yaml_del():
    os.system(PATH_BLOCKCHAINDEL)

def start_minikube(server_yaml):
    global minikube
    if minikube:
        print("🤦‍♀️ Minikube is already running 🤦‍♂️")
    else:
        if not os.path.exists('yaml'):
            os.makedirs('yaml')
        os.system("minikube start --cpus 4 --memory 4096 --kubernetes-version v1.14.2 --driver=docker")
        os.system("minikube kubectl -- get pods -A")
        write_environment(server_yaml)
        create_k8s_yaml()
        apply_yamls()
        minikube = True
        
        
def stop_minikube():
    global minikube
    os.system('minikube delete')
    minikube = False

def get_pods():
    if minikube:
        os.system('kubectl get pods')
    else:
        print("🙎🏻‍♀️ Start Minikube first 🙎🏻‍♂️")

def forward_ports():
    global minikube
    if minikube:
        PORT_FORWARD = [subprocess.Popen(["kubectl", "port-forward", "monitor-0", "3001:3001"],stdout=subprocess.DEVNULL),
        subprocess.Popen(["kubectl", "port-forward", "geth-miner01-0", "8545:8545"],stdout=subprocess.DEVNULL)]
        print("🤭 Forwarding Done")
    else:
        print("🙎🏻‍♀️ Start Minikube first 🙎🏻‍♂️")

def apply_yamls():
    os.system("kubectl apply -f yaml/")

def apply_del_yamls():
    os.system("kubectl delete -f yamlDel/")

def open_ethstats():
    webbrowser.open('127.0.0.1:3001')

def clean_up():
    for root,d_names,f_names in os.walk('./'):
        for f in f_names:
            file_path = os.path.join(root, f)
            #erase .toml files
            if '.toml' in file_path and not '.erb' in file_path:
                os.remove(file_path) 
            #erase old .yaml
            if '/yaml/' in file_path or '/yamlDel/' in file_path:
                os.remove(file_path)
            if 'UTC--2021' in file_path:
                os.remove(file_path)
    if os.path.exists(PATH_ENVIRONMENT_DEL):
        os.remove(PATH_ENVIRONMENT_DEL)

def indent_keystore(keystore_path):
    file = open(keystore_path)
    old_keystone = json.load(file)
    file.close()
    file = open(keystore_path,'w')
    json.dump(old_keystone,file, indent=2)
    file.write('\n')
    file.close()
    

def create_eth_account():
    cmd = shlex.split(f'geth account new --keystore=./keystore --password password')
    output = subprocess.check_output(cmd)
    output = output.decode().split('\n')
    etherbase_miner = output[3].split(' ')[-1]
    path_keystore = output[4].split(' ')[-1].split('/')[-1]
    indent_keystore(f'./keystore/{path_keystore}')
    return etherbase_miner, path_keystore
    
def remove_miner(server_yaml):
    global minikube
    #Recoger nodo y keystore del ultimo miner
    n_miner=server_yaml["nodes"][-1]
    info_miner = n_miner[list(n_miner.keys())[0]]
    eth_etherbase= info_miner['geth']['Eth_Etherbase']

    #Eliminación de nodes 
    cpy_server_yaml = copy.deepcopy(server_yaml)
    cpy_server_yaml.pop("nodes")

    #Añadimos solo el node del miner a eliminar
    cpy_server_yaml['nodes'] =[ n_miner]
    print(server_yaml['keystore'])
    #Eliminamos todas las keystore que no pertenezcan al miner a eliminar
    for key_store in server_yaml['keystore']['items']:
        if key_store!=eth_etherbase:
            cpy_server_yaml['keystore']['items'].pop(key_store)

    #Eliminamos el miner y su keystore del environment
    del server_yaml['nodes'][-1]    
    del server_yaml['keystore']['items'][eth_etherbase]
   
    write_environment_del(cpy_server_yaml)
    write_environment(server_yaml)
    if minikube:  
        create_k8s_yaml() 
        create_k8s_yaml_del()
        apply_del_yamls()
    print("👋💀 Node removed 💀👋")


def create_miner(server_yaml):
    global minikube
    etherbase_miner, path_keystore = create_eth_account()
    
    n_miner = int(list(server_yaml["nodes"][-1].keys())[0][5:]) + 1 
    
    miner_node_dict = {
        f'miner0{n_miner}' :{
            'k8s': {
                'replicas':1
            },
            'geth':{
                'storage_size': 20,
                'Eth_Etherbase': etherbase_miner,
                'Eth_Password': '0987654321',
                'Node_UserIdent': f'miner0{n_miner}',
                'Node_DataDir' : f'/etc/testnet/miner0{n_miner}',
                'Node_HTTPPort': 8545,
                'Node_WSPort' : 8546,     
                'NodeP2P_DiscoveryAddr': 30303,
                'Dashboard_Port' : 8080,
                'Dashboard_Refresh' : 3000000000       
            }        
        }
    }
    keystore_items_dict = {
        etherbase_miner: path_keystore
    }
    #concatenarlo en el yaml y hacer un dump
    server_yaml["nodes"].append(miner_node_dict)
    server_yaml["keystore"]["items"].update(keystore_items_dict)
    write_environment(server_yaml)
    if minikube:
        create_k8s_yaml()
        apply_yamls()
    print("👌 Node added 👌")    

def exit():
    stop_minikube()
    print("Thank you for using our system 🙋")
    clean_up()
    sys.exit(0)

def stdin_write(message, caster):
    while True:
        try:
            variable = caster(input(message))
            return variable
        except ValueError:
            print("Wrong format. Try again!")

def exit_menu():
    if minikube:
        while True:
            print('''\nExiting.. Do you also want to close Minikube?
            1.  ░█──░█ ░█▀▀▀ ░█▀▀▀█ 
                ░█▄▄▄█ ░█▀▀▀ ─▀▀▀▄▄ 
                ──░█── ░█▄▄▄ ░█▄▄▄█
            2. ⁿᵒ 
            ''')
            
            option = stdin_write("Choose an option: ", int)

            if option==1:
                exit()
            elif option==2:
                sys.exit(0)
            else:
                print("Invalid option. Try again!🤬")
    sys.exit(0)    

def config_menu():
    #ponga si cargar el template o el ultimo environment
       
    while True:
        print('''\nSelect the configuration:
        1. Default environment
        2. Last environment 
        ''')
        
        option = stdin_write("Choose an option: ", int)

        if option==1:
            return load_environment(PATH_ENVIRONMENT_TEMPLATE)   
        elif option==2:
            return load_environment(PATH_ENVIRONMENT)
        else:
            print("Invalid option. Try again!🤬")

def prueba():
    server_yaml = config_menu()
    remove_miner(server_yaml)

def server_menu():
    server_yaml = config_menu()
    switch = {
        0 : exit_menu,
        1 : start_minikube,
        2 : create_miner,
        3 : remove_miner,
        4 : get_pods, 
        5 : forward_ports,
        6 : open_ethstats,
    }

    while True:
        print('''\n🧑‍💻 Awesome simple menu 🧑‍💻 
        Select an option:
        1. Start Minikube Ethereum Cluster
        2. Add Miner
        3. Remove Miner
        4. Get pods
        5. Enable port forwarding
        6. Open EthStats
        0. Exit
        ''')
    
        option = stdin_write("Choose an option: ", int)
        function = switch.get(option, None)
        if function == None:
            print("Invalid option. Try again!🤬")
            continue
        elif option in range(1,4):
            function(server_yaml)
        else:
            function()

if __name__ == "__main__":
    try:
        server_menu()
        #prueba()
        minikube = False
        
    except KeyboardInterrupt:
        print("Thank you for using our system. Bye!")
        exit()
    except Exception as e:
        print(e) 
        print("System error. Closing!")

