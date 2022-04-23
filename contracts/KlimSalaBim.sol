// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./interfaces/IOffsetHelper.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/// @title Klim Sala Bim: A Contract to Create Carbon Neutral Events on the Polygon Network using ToucanProtocols Carbon Primitives.
/// @author danceratopz, haurog
/// @notice (Demo Version). Event participants can send MATIC to this contract in order to offset their travel to ETHAmsterdam using MATIC and ToucanProtocol's OffsetHelper.
contract KlimSalaBim is IERC721Receiver, Ownable, Pausable {

    uint256 eventId = 0;  // Can be used to identify an Event 0: ETHAmsterdam

    uint256 public totalCarbonCompensated = 0;  // Total CO2 compensated for all participants of the event.

    address OFFSETHELPER_ADDRESS = 0x1A38e74D5190bA69938979aBe69ceb7b823209d3;
    address BCT_ADDRESS = 0x2F800Db0fdb5223b3C3f354886d907A671414A7F;
    address NCT_ADDRESS = 0xD838290e877E0188a4A44700463419ED96c16107;

    // instantiate toucan's offset helper contract
    IOffsetHelper offsetHelper = IOffsetHelper(OFFSETHELPER_ADDRESS);

    enum TravelModes {
        Plane,
        Train,
        Bus,
        Bike,
        Walk
    }

    // Information about a single compensated event.
    struct SingleCompensatedTravel {
        string startingLocation;
        uint256 eventId;
        TravelModes modeOfTravel;
        uint256 distance;
        uint256 compensatedCarbon;
    }

    mapping(address => SingleCompensatedTravel[]) public compensatedTravels;

    address[] public participants;  // A list of all participants
    constructor() {}

    /// @notice Emitted when an NFT is transferred to the FractionalizeNFT contract.
    /// @param sender The address that sent the NFT.
    event NftReceived(address indexed sender);

    /// @notice Compensate the carbon used for a single leg from a particpant's journey.
    /// @param startingLocation City where the participant started their journey.
    /// @param distance in kilometers to event location.
    function compensateSingleParticipantTravel(
        string memory startingLocation,
        uint256 distance,
        uint256 carbonToCompensate,
        TravelModes modeOfTravel
    ) public payable whenNotPaused() {
        // uint256 dummyToucanID = 1; // A dummy number to fill into struct TODO: needs to be the proper ID -> No NFT to use

        if (compensatedTravels[msg.sender].length == 0) {
            participants.push(msg.sender);
        }

        compensatedTravels[msg.sender].push(SingleCompensatedTravel({
            startingLocation: startingLocation,
            eventId: eventId,
            modeOfTravel: modeOfTravel,
            distance: distance,
            compensatedCarbon: carbonToCompensate  // TODO: might want to use the a return from toucan and not the one the user filled in.
        }));

        totalCarbonCompensated += carbonToCompensate; // TODO: might want to use the a return from toucan and not the one the user filled in.

        // Call Toucan's autoOffset function to retire/compensate the carbon.
        offsetHelper.autoOffset(BCT_ADDRESS, carbonToCompensate);
    }

    /// @notice A getter function get an array of all participants back by address.
    /// @return an array (can be empty) with all owned warrant canaries.
    function getParticipants()
        public
        view
        returns(address[] memory)
    {
        return participants;
    }

    /// @notice A getter function get back an array of all compensated travels by the address.
    /// @param userAddress: Address for which the compensations are requested
    /// @return an array (can be empty) with all compensated travels
    function getTravelsCompensated(address userAddress)
        public
        view
        returns(SingleCompensatedTravel[] memory)
    {
        return compensatedTravels[userAddress];
    }

    /// @notice Pauses the contract. Contract owner only, therefore very minimal function.
    function pauseContract() public onlyOwner() {
        _pause();
    }

    /// @notice Unpauses the contract. Contract owner only, therefore very minimal function.
    function unpauseContract() public onlyOwner() {
        _unpause();
    }

    /// @dev Required to use safeTransferFrom() from OpenZeppelin's ERC721 contract (when transferring NFTs to this contract).
    function onERC721Received(
        address operator,
        address from,
        uint256 nftTokenId,
        bytes memory data
    ) public returns (bytes4) {
        emit NftReceived(msg.sender);
        return
            bytes4(
                keccak256("onERC721Received(address,address,uint256,bytes)")
            );
    }
}
