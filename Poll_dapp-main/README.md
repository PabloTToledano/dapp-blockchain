# Poll DApp

We have implemented a Poll DApp in which there are several functionalities discussed below.

Any user(node) of the blockchain will be able to create a Poll given the name of the poll.
Only the owner (creator) of a poll will be able to add candidates and advance the state of the poll.

Polls will have different states such as open for registration, closed registration, voting stage and vote counting stage.

During voting stage any user will be able to submit their vote.
A user may only vote once in a poll, exclusively to an existent candidate.

## Requirements
To execute the DApp isolated the following software must be installed:
* [Solidity v0.5.16](https://github.com/ethereum/solidity/releases/tag/v0.5.16)
* [Python 3.8.1](https://www.python.org/downloads/release/python-381/)
* [Ganache-cli](https://github.com/trufflesuite/ganache-cli)
* [Truffle](https://github.com/trufflesuite/truffle)
* [Vagrant](https://www.vagrantup.com/)


Poll DApp may be ran through:

```sh
$ python3 -m src.user_interface
```

Tests have been written on Solidity (using truffle) and Python (using web3) to assure the Dapp correct behaviour. Those test may be ran through:

```sh
$ python3 -m unittest discover tests
```

```sh
$ truffle test
```

The python requirements are specified on _requirements.txt_ and may be installed through:

```sh
$ pip3 install -r requirements.txt
```

## Authors

 - Javier Plata
 - Eduardo Eiroa
 - Elena Hervás
 - Pablo Toledano
 - Enrique Cepeda
 - Elena Ruiz
 