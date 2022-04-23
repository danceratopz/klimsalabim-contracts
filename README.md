# Klim-Sala-Bim backend contracts

We build an intuitive way for participants of an event to offset their travel induced carbon emission by integrating with the Toucan project.

## Development Environment

### Prereqs

0. Create and activate a virtual env.
1. `pip install -r requirements.txt`

### Local Dev

1. Compile contracts, locally fork polygon in Ganache and start a Python console:
   ```
   brownie console --network development
   ```
2. Deploy `KlimSalaBim.sol` to the fork (in the Python shell):
   ```
   ksb_contract = run("deploy")
   ```
