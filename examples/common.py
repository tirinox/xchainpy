import os

from xchainpy2_thorchain_query import TxDetails


def sep(title='', simple=False):
    if not simple:
        title = ' '.join(title.upper())
    title = f' {title} ' if title else ''
    print(f'{title:-^120}')


def get_phrase():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty! Usage: PHRASE='your phrase here' python3 YOUR_SCRIPT.py")
    return phrase


def get_thornode_url():
    thornode = os.environ.get('THORNODE')
    return thornode


async def thorchain_wait_tx_status(amm, tx_hash):
    sep()
    print(f"Tx has been broadcast. TX hash is {tx_hash}, {amm.wallet.explorer_url_tx(tx_hash)}")
    tracker = amm.tracker()
    async for status in tracker.poll(tx_hash):
        status: TxDetails
        print(f'Status: {status.status}; stage: {status.stage}')
    print(f"Tx has been completed. TX hash is {tx_hash}, {amm.wallet.explorer_url_tx(tx_hash)}")
    sep()
