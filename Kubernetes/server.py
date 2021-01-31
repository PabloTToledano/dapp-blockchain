import os
import json
import yaml
import subprocess
import pprint
import shlex

PATH_ENVIRONMENT_TEMPLATE = 'environment_template.yaml'
PATH_ENVIRONMENT_DEL = 'environment_del.yaml' 
PATH_BLOCKCHAININIT = './blockchainit'
PATH_BLOCKCHAINDEL = './blockchaindel' 

def load_environment():
    with open(PATH_ENVIRONMENT_TEMPLATE) as file:
        environment = yaml.load(file,Loader=yaml.FullLoader)
    return environment

def write_environment(new_environment):
    with open('environment.yaml', "w") as file:
        environment = yaml.dump(new_environment, file)   

def create_k8s_yaml():
    os.system(PATH_BLOCKCHAININIT)

def start_minikube():
    os.system("minikube start --cpus 4 --memory 4096 --kubernetes-version v1.14.2 --driver=docker")
    os.system("minikube kubectl -- get pods -A")

def stop_minikube():
    os.system('minikube delete')

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
    

def create_miner(server_yaml):
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
    

def main():
    server_conf = load_environment()
    create_miner(server_conf) 
    create_k8s_yaml()
    

def exit():
    print("Thank you for using our system. Bye!")
    #hay que poner que borre los archivos .toml
    sys.exit(0)

def stdin_write(message, caster):
    while True:
        try:
            variable = caster(input(message))
            return variable
        except ValueError:
            print("Wrong format. Try again!")

def server_menu():

    switch = {
        0 : exit,
        1 : start_minikube,
        2 : add_miner,
        3 : remove_miner,
        4 : get_pods,
        5 : forward_port,
        6 : shutdown
    }

    while True:
        print('''\nSelect an option:
        1. Start Minikube Ethereum Cluster
        2. Add Miner
        3. Remove Miner
        4. Get pods
        5. Forward port
        6. Shutdown Minikube
        0. Exit poll menu  
        ''')
    
        option = stdin_write("Choose an option: ", int)
        function = switch.get(option, None)
        if function == None:
            print("Invalid option. Try again!")
            continue
        else:
            function()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Thank you for using our system. Bye!")
    except Exception as e:
        print(e) 
        print("System error. Closing!")

