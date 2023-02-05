# CS765 Assignment 1

# Simulation of a Cryptocurrency P2P Network

## About project
The project is divided into 9 files, details as follows:  
**block.py:** Contains `Block` and `GenesisBlock` class  
**blockchain.py:** Contains the `Blockchain` class  
**constants.py:** Contains the project-wide constants  
**exceptions.py:** Contains custom exceptions  
**main.py:** Main driver program  
**network.py:** Contains utility functions to create a network of nodes  
**node.py:** Contains the `Node` class  
**txn.py:** Contains the `Transaction` and `CoinbaseTransaction` classes  
**visualize.py:** Used to visualize blockchain tree  

## Setup

1. Unzip project files into a folder.
2. Inside that folder, create a python3 virtual environment using:
    ```
    $ python3 venv .venv
    ```
3. Activate the virtual environment
    ```
    $ source .venv/bin/activate
    ```
4. Install requirements using:
    ```
    (.venv)$ pip install -r requirements.txt
    ```
5. Install `graphviz` using:
    ```
    $ sudo apt-get install graphviz
    ```

## Execution
The main file can be executed as:
```
(.venv)$ python main.py <n> <z0> <z1> <txn_time> <mining_time> <simulation_until>
```

The folder path where blockchain trees of all nodes will be stored after the simulation is available in `constants.py` file in constant `TREE_OUTPUT_DIR`.  
The nodes of the tree are stored in the format:
```
<block_id>::<block_timestamp>
```

To visualize the above tree files, run the script `visualize.py` as:
```
(.venv)$ python visualize.py
```
This script automatically picks up all tree files from the `TREE_OUTPUT_DIR` folder and creates a `png` file out of them, saving them into the same folder with the same file name and png extension.  