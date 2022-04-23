from brownie import accounts, network, KlimSalaBim

def deploy_dev():
    deploy_account = accounts[0]
    ksb_contract = KlimSalaBim.deploy({"from": deploy_account})
    print(ksb_contract)
    return ksb_contract

def deploy_mumbai():
    if network.show_active() != "polygon-test-alchemy":
        print(f"ERROR: Incorrect network. Expected 'polygon-test', got {network.show_active}")
        return
    deploy_account = accounts.load("ksb_deployment_polygon_test")
    ksb_contract = KlimSalaBim.deploy({"from": deploy_account}, publish_source=True)
    print(ksb_contract)
    return ksb_contract

def main():
    if network.show_active() == "polygon-test-fork":
        ksb_contract = deploy_dev()
        return ksb_contract

    if network.show_active() == "polygon-test-alchemy":
        ksb_contract = deploy_mumbai()
        return ksb_contract
