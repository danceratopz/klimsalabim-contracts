# Klim-Sala-Bim backend contracts

We build an intuitive way for participants of an event to offset their travel induced carbon emission by integrating with the Toucan project.

## Development Environment

### Prereqs

0. Create and activate a virtual env.
1. `pip install -r requirements.txt`

### Local Dev

1. Compile contracts, locally fork polygon in Ganache and start a Python console:
   ```
   brownie console --network polygon-main-fork
   ```
2. Deploy `KlimSalaBim.sol` to the fork (in the Python shell):
   ```
   ksb_contract = run("deploy")
   ```

#### Fork Mumbai

Prereq:
```
brownie networks add development polygon-test-fork cmd=ganache-cli host="http://127.0.0.1" port=8545
```
Fork:
```
brownie console --network polygon-test-fork
```

#### Key Management

Add private keys for deployment account by running the two commands in succession:
```
brownie accounts new ksb_deployment_polygon_main
brownie accounts new ksb_deployment_polygon_test
```
