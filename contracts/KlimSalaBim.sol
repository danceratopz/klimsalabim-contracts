// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

// import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

/// @title 
/// @author danceratopz, haurog
/// @notice 
//contract KlimSalaBim is IERC721Receiver {
contract KlimSalaBim {

    uint256 eventId = 0;
    
    enum TravelModes {
        Plane,
        Train,
        Bus,        
        Bike,
        Walk
    }
    
    struct SingleCompensatedTravel {
        uint256 eventId;
        TravelModes modeOfTravel;
        uint256 distance;
    }

    mapping(address => SingleCompensatedTravel) public participants;
    
    constructor() {}

    /// @notice 
    /// @param startingLocation city
    /// @param distance in kilometers to event location
    /// @dev 
    /// @return 
    function compensateSingleParticipantTravel(
                                               string memory startingLocation,
                                               uint256 distance,
                                               TravelModes modeOfTravel) public returns (uint256) {

        participants[msg.sender] = SingleCompensatedTravel({
                                                           eventId: eventId,
                                                           modeOfTravel: modeOfTravel,
                                                           distance: distance
                    });
    }

    /* /// @dev Required to use safeTransferFrom() from OpenZeppelin's ERC721 contract (when transferring NFTs to this contract). */
    /* function onERC721Received( */
    /*     address operator, */
    /*     address from, */
    /*     uint256 nftTokenId, */
    /*     bytes memory data */
    /* ) public returns (bytes4) { */
    /*     emit NftReceived(msg.sender); */
    /*     return */
    /*         bytes4( */
    /*             keccak256("onERC721Received(address,address,uint256,bytes)") */
    /*         ); */
    /* } */
    
}
