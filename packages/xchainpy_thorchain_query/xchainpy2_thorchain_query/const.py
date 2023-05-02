DEFAULT_USER_AGENT = 'XChainPy2/0.0.1/python'
DEFAULT_INTERFACE_ID = 'XChainPy2'

XCHAINPY_IDENTIFIER = 'xchainpy-client'
NINE_REALMS_CLIENT_HEADER = 'x-client-id'

TC_RESERVE_ADDR = 'thor1dheycdevq39qlkxs2a6wuuzyn4aqxhve4qxtxt'
TC_BOND_ADDR = 'thor17gw75axcnr8747pkanye45pnrwk7p9c3cqncsv'
TC_POOL_ADDR = 'thor1g98cy3n9mmjrpn0sxmn63lztelera37n8n67c0'
TC_STANDBY_RESERVE_ADDR = 'thor1lj62pg6ryxv2htekqx04nv7wd3g98qf9gfvamy'


class Mimir:
    HALTTRADING = 'HALTTRADING'
    HALTCHAINGLOBAL = 'HALTCHAINGLOBAL'
    PAUSELP = 'PAUSELP'

    @staticmethod
    def pause_lp(chain):
        return f'PAUSELP{chain.upper()}'

    @staticmethod
    def halt_trading(chain):
        return f'HALT{chain.upper()}TRADING'
