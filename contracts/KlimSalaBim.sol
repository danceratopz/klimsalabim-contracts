// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

// import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

/// @title
/// @author danceratopz, haurog
/// @notice
//contract KlimSalaBim is IERC721Receiver {
contract KlimSalaBim {
    uint256 eventId = 0;

    uint256 public totalCarbonCompensated = 0;  // Total CO2 compensated for all participants of the event.

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
        uint256 toucanBadgeID;
    }

    mapping(address => SingleCompensatedTravel[]) public participants;

    constructor() {}

    /// @notice
    /// @param startingLocation city
    /// @param distance in kilometers to event location
    /// @dev
    /// @return
    function compensateSingleParticipantTravel(
        string memory startingLocation,
        uint256 distance,
        uint256 carbonToCompensate,
        TravelModes modeOfTravel
    ) public payable {
        // TODO: Connect to toucan retire function
        // Send Matic to toucan protocol

        uint256 dummyToucanID = 1; // A dummy number to fill into struct TODO: needs to be the proper ID

        participants[msg.sender].push(SingleCompensatedTravel({
            startingLocation: startingLocation,
            eventId: eventId,
            modeOfTravel: modeOfTravel,
            distance: distance,
            compensatedCarbon: carbonToCompensate,  // TODO: might want to use the a return from toucan and not the one the user filled in.
            toucanBadgeID: dummyToucanID
        }));

        totalCarbonCompensated += carbonToCompensate; // TODO: might want to use the a return from toucan and not the one the user filled in.
    }

    /// @notice A getter function get back an array of all compensated travels by the address.
    /// @param userAddress: Address for which the compensations are requested
    /// @return an array (can be empty) with all compensated travels
    function getTravelsCompensated(address userAddress)
        public
        view
        returns(SingleCompensatedTravel[] memory)
    {
        return participants[userAddress];
    }
}
