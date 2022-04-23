from brownie import accounts, network, KlimSalaBim

def main():
    deploy_account = accounts[0]
    ksb_contract = KlimSalaBim.deploy({"from": deploy_account})
    print(ksb_contract)
    return ksb_contract
