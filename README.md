# DApp-Blockchain

On this project we deploy an ethereum network in which the nodes are built on Kubernetes containers. This network can be used with any kind of DApp that can be ran on a private blockchain.
We have implemented a Poll DApp in which there are several functionalities discussed below.

Any user(node) of the blockchain will be able to create a Poll given the name of the poll.
Only the owner (creator) of a poll will be able to add candidates and advance the state of the poll.

Polls will have different states such as open for registration, closed registration, voting stage and vote counting stage.

During voting stage any user will be able to submit their vote.
A user may only vote once in a poll, exclusively to an existent candidate.

Our Kubernetes + Geth network is based on the works at: 
[ethereum-poa-clique-kubernetes-template]

In order to deploy the Kubernetes + Ethereum Network :
```sh
$ ./server.py
```
or
```sh
$ python3 server.py
```

Poll DApp may be ran through:

```sh
$ python3 -m src.user_interface
```

## Requirements
To execute the DApp the following software must be installed:
* [Docker]
* [Kubernetes] v1.15.1
* [Kubectl]
* [Solidity] v0.5.16

Other requirements are specified in [Poll-dapp/requirements.txt]

### Default accounts:
 - 0xC11Ba4c7C24f70e7A581C7DAA92EAc108099aCEC
 - 0x4C92786B90D848eAA3f4EF46918af724A309Ae79
 
## Authors

 - Javier Plata
 - Eduardo Eiroa
 - Elena Hervás
 - Pablo Toledano
 - Enrique Cepeda
 - Elena Ruiz
 
[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   
   [ethereum-poa-clique-kubernetes-template]: <https://github.com/blockchain-it-hr/ethererum-poa-clique-kubernetes-template>
   [Poll-dapp/requirements.txt]: <https://github.com/PabloTToledano/dapp-blockchain/blob/main/Poll_dapp-main/requirements.txtt>
   [Docker]: <https://www.docker.com/>
   [Kubernetes]: <https://kubernetes.io/es/>
   [kubectl]: <https://kubernetes.io/es/docs/tasks/tools/install-kubectl/>
   [solidity]: <https://solidity-es.readthedocs.io/es/latest/>
   ''
