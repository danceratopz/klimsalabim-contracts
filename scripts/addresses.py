from brownie import network

if 'test' in network.show_active():  # mumbai
    ADDRESSES = {'nct': "0x7beCBA11618Ca63Ead5605DE235f6dD3b25c530E",
                 'offset_helpers': "0x1A38e74D5190bA69938979aBe69ceb7b823209d3"}
elif 'main' in network.show_active():  # polygon mainnet
    ADDRESSES = {'nct': "0xD838290e877E0188a4A44700463419ED96c16107",
                 'offset_helpers': "0x79E63048B355F4FBa192c5b28687B852a5521b31",
                 'klimsalabim' : "0x246716856349a0931eefAA42be86e58C3B385a90" }
else:
    raise Exception(f"Unexpected network: network.show_active():")
