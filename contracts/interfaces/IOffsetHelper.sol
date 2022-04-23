// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

// import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

interface IOffsetHelper {

    function autoOffset(
                        address _depositedToken,
                        address _poolToken,
                        uint256 _amountToOffset
                        ) external;

    function autoOffset(address _poolToken, uint256 _amountToOffset)
        external
        payable;

}
