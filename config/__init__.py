import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config', 'config.ini'))

# CONTRACT CONFIG
sc_address = config.get('contract', 'sc_address')
sc_abi = config.get('contract', 'sc_abi')
owner_address = config.get('contract', 'owner_address')
private_key = config.get('contract', 'owner_private_key')
web3_url = config.get('contract', 'infura_url')
