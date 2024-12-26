from web3 import Web3

# Connect to the blockchain node
node_url = "http://94.237.54.116:35587"
web3 = Web3(Web3.HTTPProvider(node_url))

if not web3.is_connected():
    print("Failed to connect to blockchain")
    exit()

print("Connected to blockchain")

# CryoPod contract address and ABI
cryopod_address = "0xa821D7DdE75C118BF5EE48468a621b39244e80c3"
cryopod_abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "user", "type": "address"},
            {"indexed": False, "name": "data", "type": "string"}
        ],
        "name": "PodStored",
        "type": "event"
    }
]

# Create contract instance
cryopod_contract = web3.eth.contract(address=cryopod_address, abi=cryopod_abi)

# Fetch PodStored events
print("Fetching PodStored events...")
try:
    events = cryopod_contract.events.PodStored.create_filter(fromBlock="earliest").get_all_entries()
    for event in events:
        user = event.args.user
        raw_data = event.args.data
        print(f"Event - User: {user}, Raw Data: {raw_data}")
        # Attempt to decode the data
        try:
            decoded_data = bytes.fromhex(raw_data[2:]).decode('utf-8')
            print(f"Decoded Data: {decoded_data}")
        except Exception as e:
            print(f"Failed to decode as UTF-8. Error: {e}")
except Exception as e:
    print(f"Error fetching events: {e}")
