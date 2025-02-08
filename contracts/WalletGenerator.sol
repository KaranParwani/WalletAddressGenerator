// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WalletManager{
    event WalletAddressGenerator(address WalletAddres);

    function generateWalletAddress() public returns (address) {
        Wallet newWallet = new Wallet(msg.sender);
        emit WalletAddressGenerator(address(newWallet));

        return address(newWallet);

    }
}

contract Wallet {
    address public owner;

    constructor(address _owner) {
        owner = _owner;
    }
}