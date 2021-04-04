# Hyperledger_Iroha_Multi_Node_Tutorial

## Prerequisites
We run this demo with Docker on Ubuntu machine.

To run the python code, you also need python3, pip3 and iroha python lirary.
Install the iroha python library with following command:
```
pip3 install iroha
```

## Network Setup
From projects root directory, run the following command to clear previous setup:
```
bash network.sh down
```
From projects root directory, run the following command to setup the network:
```
bash network.sh up
```
## Transaction & Query The Results From Different Nodes
From projects root directory, run the following command for transactions and query those results using python iroha library:

```
python3 python_sdk/tx-example.py
```
