import json

from brownie import accounts, network, Contract

from scripts.abis import OFFSET_HELPERS_ABI_FILENAME, KLIMSALABIM_ABI_FILENAME
from scripts.addresses import ADDRESSES
import scripts.utils

def main(retire_tco2=False):
    """
    Example usage in brownie console:
      # Find out how much MATIC must be sent in order to offset the tco2
      run("do_offset", method_name="main", args=None, kwargs={'retire_tco2': False})
      # Actually retire the tco2
      run("do_offset", method_name="main", args=None, kwargs={'retire_tco2': True})
    """

    if (network.show_active() != "polygon-main-alchemy") and (network.show_active() != "polygon-main-fork"):
        # KlimSalaBim is not deployed on Mumbai yet
        raise Exception(f"Unexpected network: {network.show_active()}")

    offset_helpers_abi = scripts.utils.load_abi(OFFSET_HELPERS_ABI_FILENAME)
    offset_helpers_contract = Contract.from_abi("OffsetHelpers", ADDRESSES['offset_helpers'], offset_helpers_abi)

    klimsalabim_abi = scripts.utils.load_abi(KLIMSALABIM_ABI_FILENAME)
    klimsalabim_contract = Contract.from_abi("Klimsalabim_Abi_Filename", ADDRESSES['klimsalabim'], klimsalabim_abi)

    tco2_to_retire = int(5e15)  # The number we hard-code in our look-up table for the 5 cities multiplied by 1e18 and converted to int.
    matic_required = offset_helpers_contract.howMuchETHShouldISendToSwap(ADDRESSES['nct'], tco2_to_retire) # tco2_to_retire is big number

    print("\n", matic_required/1e18, " MATIC required to offset ", tco2_to_retire/1e18, " TCO2", sep="")
    if retire_tco2:
        city = "zurich"
        distance = 100
        if (network.show_active() == "polygon-main-alchemy") or (network.show_active() != "polygon-test-alchemy"):
            account = accounts.load("ksb_deployment_polygon_main")
        else:
            account = accounts[0]
        klimsalabim_contract.compensateSingleParticipantTravel(city, distance, tco2_to_retire, 0, {'from': account, 'value': matic_required});
