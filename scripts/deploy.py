import json
from brownie import accounts, network, Contract, KlimSalaBim

# The path is relative to repo root (where brownie is executed)
OFFSET_HELPERS_ABI_FILENAME = "./misc/abis/OffsetHelper.json"

if 'test' in network.show_active():
    ADDRESSES = {'nct': "0x7beCBA11618Ca63Ead5605DE235f6dD3b25c530E",
                 'offset_helpers': "0x1A38e74D5190bA69938979aBe69ceb7b823209d3"}
elif 'main' in network.show_active():
    ADDRESSES = {'nct': "0xD838290e877E0188a4A44700463419ED96c16107",
                 'offset_helpers': "0x79E63048B355F4FBa192c5b28687B852a5521b31"}
else:
    raise Exception(f"Unexpected network: network.show_active():")


def load_offset_helpers_abi():
    with open(OFFSET_HELPERS_ABI_FILENAME, 'r') as f:
        abi = json.load(f)
    return abi


def deploy_fork():
    """
    Deploy locally on a Polygon Mainnet or Mumbai fork.
    """
    deploy_account = accounts[0]
    ksb_contract = KlimSalaBim.deploy({"from": deploy_account})
    print("Initialized KlimSalaBim contract:", ksb_contract)

    offset_helpers_abi = load_offset_helpers_abi()
    helpers_contract = Contract.from_abi("OffsetHelpers", ADDRESSES['offset_helpers'], offset_helpers_abi)
    print("Initalized OffsetHelpers contract:", helpers_contract)

    return ksb_contract, helpers_contract


def deploy_mumbai():
    if network.show_active() != "polygon-test-alchemy":
        print(f"ERROR: Incorrect network. Expected 'polygon-test-alchemy', got {network.show_active}")
        return
    deploy_account = accounts.load("ksb_deployment_polygon_test")
    ksb_contract = KlimSalaBim.deploy({"from": deploy_account}, publish_source=True)
    print(ksb_contract)
    return ksb_contract


def deploy_polygon():
    if network.show_active() != "polygon-main-alchemy":
        print(f"ERROR: Incorrect network. Expected 'polygon-main-alchemy', got {network.show_active}")
        return
    deploy_account = accounts.load("ksb_deployment_polygon_main")
    ksb_contract = KlimSalaBim.deploy({"from": deploy_account}, publish_source=True)
    print(ksb_contract)
    return ksb_contract


def main():

    if 'fork' in network.show_active():
        ksb_contract, helpers_contract = deploy_fork()

        # Calculate the required amount of MATIC to compenstate a specified amount of tco2
        tco2_to_retire = int(1e16)
        matic_required = helpers_contract.howMuchETHShouldISendToSwap(ADDRESSES['nct'], tco2_to_retire)
        print("\n", matic_required/1e18, "MATIC required to offset", tco2_to_retire/1e18, "TCO2")

        # Test ToucanProtocol's function in isolation:
        # helpers_contract.autoOffset(NCT_CONTRACT_ADDRESS, tco2_to_retire, {'from': accounts[0], 'value': matic_required})

        # Test the main KlimSalaBim compensation function:
        ksb_contract.compensateSingleParticipantTravel("Zurich",
                                                       100, # kilometers travelled
                                                       tco2_to_retire,
                                                       0,  # 0 ^= plane
                                                       {'from': accounts[0], 'value': matic_required});
        return ksb_contract, helpers_contract

    if network.show_active() == "polygon-test-alchemy":
        ksb_contract = deploy_mumbai()
        return ksb_contract

    if network.show_active() == "polygon-main-alchemy":
        ksb_contract = deploy_polygon()
        # If you need to instantiate the contract later on mainnet it is available in the brownie console as
        # - KlimSalaBim[0] ^= first deployment
        # - KlimSalaBim[-1] ^= last deployment
        # Then, for example (with other helpers and globals as defined above...)
        # tco2_to_retire = int(1e16)
        # helpers_contract = Contract.from_abi("OffsetHelpers", ADDRESSES['offset_helpers'], offset_helpers_abi)
        # matic_required = helpers_contract.howMuchETHShouldISendToSwap(ADDRESSES['nct'], tco2_to_retire)
        # KlimSalaBim[-1].compensateSingleParticipantTravel("Zurich", 100, tco2_to_retire, 0, {'sender': accounts[0], 'value': matic_required});
        return ksb_contract
