from web3 import Web3

from xchainpy2_client import TokenTransfer
from xchainpy2_ethereum import EVM_NULL_ADDRESS
from xchainpy2_utils import Asset, Amount


class EventDescription:
    def __init__(self, abi):
        self.abi = abi
        self.signature = Web3.keccak(text=abi['name'] + '(' + ','.join([i['type'] for i in abi['inputs']]) + ')').hex()
        self.types = [i['type'] for i in abi['inputs'] if not i['indexed']]

    def match(self, log):
        return log['topics'][0].hex() == self.signature


TRANSFER_OUT = EventDescription({
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "vault", "type": "address"},
        {"indexed": True, "name": "to", "type": "address"},
        {"indexed": False, "name": "asset", "type": "address"},
        {"indexed": False, "name": "amount", "type": "uint256"},
        {"indexed": False, "name": "memo", "type": "string"}
    ],
    "name": "TransferOut",
    "type": "event"
})

TRANSFER = EventDescription({
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "from", "type": "address"},
        {"indexed": True, "name": "to", "type": "address"},
        {"indexed": False, "name": "value", "type": "uint256"}
    ],
    "name": "Transfer",
    "type": "event"
})

DEPOSIT = EventDescription({
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "to", "type": "address"},
        {"indexed": True, "name": "asset", "type": "address"},
        {"indexed": False, "name": "amount", "type": "uint256"},
        {"indexed": False, "name": "memo", "type": "string"}
    ],
    "name": "Deposit",
    "type": "event"
})


class Web3LogDecoder:
    def __init__(self, web3: Web3, native_asset: Asset):
        self.web3 = web3
        self.native_asset = native_asset

    def get_asset_from_address(self, address):
        if address == EVM_NULL_ADDRESS:
            return self.native_asset
        else:
            return Asset(self.native_asset.chain, "", address.upper())

    def decode_transfer_event(self, log, tx_receipt):
        # decode ERC20 transfer
        data = self.web3.codec.decode(TRANSFER.types, log['data'])
        value = data[0]
        amount = self._get_amount(value)

        from_address = '0x' + log['topics'][1].hex()[26:]  # Remove 0x prefix and address padding
        to_address = '0x' + log['topics'][2].hex()[26:]

        asset = self.get_asset_from_address(log['address'])
        return TokenTransfer(from_address, to_address, amount, asset, tx_hash=self._tx_hash(tx_receipt))

    def decode_deposit_event(self, log, tx_receipt):
        data = self.web3.codec.decode(DEPOSIT.types, log['data'])

        to_address = '0x' + log['topics'][1].hex()[26:]  # Remove 0x prefix and address padding
        asset = '0x' + log['topics'][2].hex()[26:]
        asset = self.get_asset_from_address(asset)
        amount = self._get_amount(data[0])
        # memo = data[1].decode('utf-8') if isinstance(data[1], bytes) else data[1]
        return TokenTransfer(to_address, "", amount, asset, tx_hash=self._tx_hash(tx_receipt))

    def decode_transfer_out_events(self, log, tx_receipt):
        from_address = '0x' + log['topics'][1].hex()[26:]  # Remove 0x prefix and address padding
        to_address = '0x' + log['topics'][2].hex()[26:]

        # log_data = log['data'][2:]
        data = self.web3.codec.decode(TRANSFER_OUT.types, log['data'])
        asset = data[0]
        amount = data[1]
        # memo = data[2].decode('utf-8') if isinstance(data[2], bytes) else data[2]
        return TokenTransfer(
            from_address=from_address,
            to_address=to_address,
            amount=self._get_amount(amount),
            asset=asset,
            tx_hash=self._tx_hash(tx_receipt),
            outbound=True
        )

    def decode_events(self, tx_receipt):
        results = []
        for log in tx_receipt['logs']:
            if TRANSFER.match(log):
                results.append(self.decode_transfer_event(log, tx_receipt))
            elif DEPOSIT.match(log):
                results.append(self.decode_deposit_event(log, tx_receipt))
            elif TRANSFER_OUT.match(log):
                results.append(self.decode_transfer_out_events(log, tx_receipt))
        return results

    @staticmethod
    def _tx_hash(tx_receipt):
        return tx_receipt.transactionHash.hex()

    @staticmethod
    def _get_amount(amount):
        return Amount.from_base(amount)
