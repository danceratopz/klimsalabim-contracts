import json
from brownie import accounts, network, Contract, KlimSalaBim

from scripts.abis import OFFSET_HELPERS_ABI_FILENAME, KLIMSALABIM_ABI_FILENAME
from scripts.addresses import ADDRESSES
import scripts.utils

def deploy_fork():
    """
    Deploy locally on a Polygon Mainnet or Mumbai fork.
    """
    deploy_account = accounts[0]
    ksb_contract = KlimSalaBim.deploy({"from": deploy_account})
    print("Initialized KlimSalaBim contract:", ksb_contract)

    offset_helpers_abi = scripts.utils.load_abi(OFFSET_HELPERS_ABI_FILENAME)
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
