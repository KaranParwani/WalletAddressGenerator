from config import web3_url, owner_address, sc_address, sc_abi, private_key
from web3 import Web3


def generate_wallet_address():
    print("Initializing connection to Infura...")
    infura_url = f"https://sepolia.infura.io/v3/{web3_url}"
    web3 = Web3(Web3.HTTPProvider(infura_url))

    # Check connection
    print("Checking connection to Ethereum node...")
    if not web3.is_connected():
        print("Error: Cannot connect to Ethereum node.")
        exit()
    print("Successfully connected to Ethereum node.")

    # Get nonce
    print(f"Fetching nonce for address {owner_address}...")
    nonce = web3.eth.get_transaction_count(owner_address)
    print(f"Nonce fetched: {nonce}")

    # Contract setup
    print(f"Setting up contract at address {sc_address}...")
    contract = web3.eth.contract(address=sc_address, abi=sc_abi)

    # Estimate gas
    print("Estimating gas for function call...")
    try:
        estimated_gas = contract.functions.generateWalletAddress().estimate_gas({
            'nonce': nonce,
            'from': owner_address
        })
        print(f"Estimated gas: {estimated_gas}")
    except Exception as e:
        print(f"Error estimating gas: {e}")
        return

    # Build transaction
    print("Building transaction...")
    try:
        transaction = contract.functions.generateWalletAddress().build_transaction({
            'nonce': nonce,
            'gasPrice': web3.eth.gas_price,
            'gas': estimated_gas,
            'from': owner_address
        })
        print(f"Transaction built: {transaction}")
    except Exception as e:
        print(f"Error building transaction: {e}")
        return

    # Sign transaction
    print("Signing transaction...")
    try:
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        print(f"Transaction signed: {signed_tx}")
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return

    # Send transaction
    print("Sending transaction...")
    try:
        txn_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Transaction hash: {txn_hash.hex()}")
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return

    # Wait for transaction receipt
    print("Waiting for transaction receipt...")
    try:
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash, timeout=240)
        print(f"Transaction receipt: {txn_receipt}")
    except Exception as e:
        print(f"Error waiting for transaction receipt: {e}")
        return

    print("Transaction completed successfully.")

    # Extract the `data` field
    event_data = txn_receipt['logs'][0]['data']

    # Convert HexBytes to a string and debug the length
    event_data_str = event_data.hex()
    print(f"Event Data (Hex): {event_data_str}")
    print(f"Length of Event Data: {len(event_data_str)}")

    # Slice to extract the address (last 40 characters, excluding padding)
    wallet_address_hex = event_data_str[-40:]  # Extract the last 40 characters for the wallet address
    print(f"Extracted Wallet Address (Hex): {wallet_address_hex}")

    # Convert to checksum address
    try:
        generated_wallet_address = Web3.to_checksum_address('0x' + wallet_address_hex)
        print(f"Generated Wallet Address: {generated_wallet_address}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    generate_wallet_address()
