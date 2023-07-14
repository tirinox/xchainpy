from typing import NamedTuple


class ExplorerProvider(NamedTuple):
    explorer_url: str
    explorer_address_url: str
    explorer_tx_url: str

    def get_address_url(self, address: str) -> str:
        return self.explorer_address_url.format(address=address)

    def get_tx_url(self, tx_id: str) -> str:
        return self.explorer_tx_url.format(tx_id=tx_id)
