# Klim-Sala-Bim backend contracts

We build an intuitive way for participants of an event to offset their travel induced carbon emission by integrating with the Toucan project.

# KlimSalaBim

KlimSalaBim is an initiative to offset your carbon footprints and save environment.

<img src="./KlimSalaBim.png"/>

## Problem:

Many activities such as air travel cause climate-damaging CO₂ emissions. Climate change and global warming are significant challenges of the 21st century. Kyoto Protocol (1997) regards the market mechanism as a way to solve the greenhouse gas emission reduction problem and therefore carbon dioxide emission is considered a commodity- forming a transparent carbon trading system.

## Our solution

Carbon offsetting allows companies or individuals to reduce carbon emissions by purchasing carbon credits from carbon reduction projects. These projects include planting trees, avoiding deforestation, investing in renewable energy, and carbon capture.

KlimSalaBim enables users to reduce their carbon footprint by buying Carbon certificates and retiring them using Toucan smart contracts.

## How It's Made

Architecture:

- Toucan helper contracts for retiring carbon certificates
- KlimSalaBim smart contracts accumulates the total emissions 
- React-based NFT Dapp to mint Panther NFT and participate in lottery.

Technologies

- UI - Next.js, React, HTML/CSS
- Smart Contract - Solidity ERC-721, Toucan Protocol Helper classes
- Programmable Cashflows - Superfluid (Future roadmap)
- Backend - web3.js, Node.js
- Art Design - Adobe PhotoShop, Adobe Illustrator
- Testnet - Mumbai Polygon , Polygon Mainnet (Future roadmap)
- Tools - Brownie, Coinbase SDK, Metamask

## Demo Url

http://www.klimsalabim.xyz/

## Future Implementation Ideas

- Streaming functionality to compensate for the stay of the participant at the event (Retire at the end) empowered by Superfluid Protocol.
- NFT claiming functionality from Toucan Protocol and extending it with information about the event.

## Developers
- Caroline Kabat (Tweet @carolinekabat)
- Danceratopz (Tweet @danceratopz)
- Ram Vittal (Tweet @imvittal)
- Roger Häusermann (haurog@pm.me)
- Selver Senguler (selversenguler@gmail.com)

## Source code repo

- Frontend - https://github.com/Klim-Sala-Bim/klimsalabim-ui
- Smart contracts - https://github.com/Klim-Sala-Bim/backend


## Development Environment - Technical Details/ Implementations

### Prereqs

0. Create and activate a virtual env.
1. `pip install -r requirements.txt`
2. Install required Solidity libraries:
   ```
   brownie pm install OpenZeppelin/openzeppelin-contracts@4.3.2
   ```

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
