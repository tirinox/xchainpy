import asyncio
import json
import logging
import os
import pickle
import subprocess
import tempfile

import aiofiles

from xchainpy2_thorchain_query import TransactionTracker


class TxStatusRecorder:
    def __init__(self, tx_hash, tracker: TransactionTracker):
        self.tx_hash = tx_hash
        self.db = {}
        self.tick = 0
        self.ignore_keys = []
        self.tracker = tracker

    @property
    def filename(self):
        return f'../../temp/tx_status_db/{self.tx_hash}.pkl'

    async def query_status_from_server(self, block_no):
        try:
            details = await self.tracker.tc_get_tx_details(self.tx_hash, block_no)
            status = await self.tracker.tc_get_tx_status(self.tx_hash, block_no)

            data = {
                'details': details.to_dict() if details else None,
                'status': status.to_dict() if status else None,
            }

            print(f'Got status for block #{block_no}: {data}')

            return data
        except Exception as e:
            logging.exception(f'Error querying status for block #{block_no}: {e}')
            pass

    async def get_tx_status(self, block_no, log_prefix=''):
        block_no = str(block_no)
        if block_no in self.db:
            return self.db[block_no]
        else:
            status = None
            for _ in range(5):
                status = await self.query_status_from_server(block_no)
                if status:
                    break
                else:
                    await asyncio.sleep(3.0)

            if status:
                self.db[block_no] = status
                await self.save_db_sometimes(lpg_prefix=log_prefix)
                return status

    async def save_db(self, log_prefix=''):
        print(f'{log_prefix}Saving DB: {len(self.db)} entries')
        with open(self.filename, 'wb') as f:
            pickle.dump(self.db, f)

        print(f'{log_prefix}Saved file size is {get_size_mb(self.filename)} MB')

    async def save_db_sometimes(self, lpg_prefix=''):
        self.tick += 1
        if self.tick % 10 == 0:
            await self.save_db(lpg_prefix)

    async def load_db(self):
        try:
            with open(self.filename, 'rb') as f:
                print(f'Loading Db. Filesize is {get_size_mb(self.filename)} MB')
                self.db = pickle.load(f)
                if not isinstance(self.db, dict):
                    self.db = {}
                print(f'DB loaded: {len(self.db)} items')
        except Exception:
            print(f'Error! DB is not loaded!')
            return {}

    def clear_db(self):
        self.db = {}

    @staticmethod
    def are_identical(state1, state2):
        return str(state1) == str(state2)

    async def batch_load(self, *blocks):
        for b in blocks:
            await self.get_tx_status(b)

    async def scan(self, start_block, end_block):
        if end_block < start_block:
            raise ValueError('End block should be greater than start block')

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        return await self._scan(start_block, end_block)

    def clear_identical_states(self):
        keys = list(self.db.keys())
        for i in range(len(keys) - 1):
            if self.are_identical(self.db[keys[i]], self.db[keys[i + 1]]):
                del self.db[keys[i]]

    async def _scan(self, left_block, right_block, depth=0):
        prefix = ' ' * (depth * 2)

        if left_block >= right_block:
            print(f'{prefix}Stop branch at #{left_block}.')
            return

        print(f'{prefix}Scan start {left_block} and {right_block}; '
              f'they are {right_block - left_block} block apart.')

        left_nodes = await self.get_tx_status(left_block, prefix)
        right_nodes = await self.get_tx_status(right_block, prefix)

        if not left_nodes or not right_nodes:
            print(f"{prefix}ERROR Scanning this interval! Skip this!")
            return

        if not self.are_identical(left_nodes, right_nodes):
            print(f'{prefix}There is difference between blocks {left_block}...{right_block}; '
                  f'they are {right_block - left_block} block apart.')
            middle = (left_block + right_block) // 2
            await self._scan(left_block, middle, depth=depth + 1)
            await self._scan(middle + 1, right_block, depth=depth + 1)
        else:
            print(f'{prefix}There are no changes in range {left_block}..{right_block} '
                  f'({right_block - left_block} blocks)')

    async def naive_diff(self, block1, block2):
        if block1 == block2:
            print('Same block')
            return

        with await self.save_temp(block1) as fn1, await self.save_temp(block2) as fn2:
            result = subprocess.run(['diff', fn1.name, fn2.name], capture_output=True, text=True)
            return result

    async def save_temp(self, block):
        nodes = await self.get_tx_status(block)
        temp_file = tempfile.NamedTemporaryFile(delete=True, mode='wb', suffix='.pkl')
        pickle.dump(nodes, temp_file)
        temp_file.flush()  # Ensure data is written before using it in the diff command
        return temp_file

    def print_db_map(self):
        print('------ DB MAP ------')
        keys = list(self.db.keys())
        if not keys:
            print('DB is empty!')
            return
        min_block = min(int(b) for b in keys)
        max_block = max(int(b) for b in keys)

        print(f'Full range: {min_block}..{max_block} ({max_block - min_block + 1} blocks)')
        fill_factor = len(keys) / (max_block - min_block + 1) * 100.0
        print(f'Loaded {len(keys)} items, fill factor is {fill_factor:.2f} %')

        r = ''
        for i in range(min_block, max_block + 1):
            r += ('o' if str(i) in self.db else '.')

        print(r)

    @property
    def block_list(self):
        return sorted(list(self.db.keys()))

    def __getitem__(self, item):
        return self.db[item]


def get_size_mb(file_path):
    file_size = os.path.getsize(file_path)
    size = file_size / 1024 ** 2
    return round(size, 3)
