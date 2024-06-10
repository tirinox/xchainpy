class URLs:
    """
    A collection of URLs for public THORChain APIs (THORNode, RPC, Midgard).
    See https://ops.ninerealms.com/links for more links.
    """

    class THORNode:
        """
        THORNode API URLs.
        """
        PUBLIC = 'https://thornode.thorchain.info'
        NINE_REALMS = 'https://thornode.ninerealms.com'
        THORSWAP = 'https://thornode.thorswap.net'

        # Pre-hard-fork endpoints (blocks 1 through 4786559):
        ARCHIVE_V0 = 'https://thornode-v0.ninerealms.com'
        # Post-hard-fork endpoints (block 4786560 to present):
        ARCHIVE_V1 = 'https://thornode-v1.ninerealms.com'

        MAINNET = NINE_REALMS
        STAGENET = 'https://stagenet-thornode.ninerealms.com'
        TESTNET = 'https://testnet.thornode.thorchain.info'

    class RPC:
        """
        THORChain RPC URLs.
        """
        PUBLIC = 'https://rpc.thorchain.info'
        NINE_REALMS = 'https://rpc.ninerealms.com'
        THORSWAP = 'https://rpc.thorswap.net'

        ARCHIVE_V0 = 'https://rpc-v0.ninerealms.com'

        MAINNET = NINE_REALMS
        STAGENET = 'https://stagenet-rpc.ninerealms.com'
        TESTNET = 'https://testnet.rpc.thorchain.info/'

    class Midgard:
        """
        Midgard API URLs.
        """
        PUBLIC = 'https://midgard.thorchain.info'
        NINE_REALMS = 'https://midgard.ninerealms.com'
        THORSWAP = 'https://midgard.thorswap.net'

        MAINNET = NINE_REALMS
        STAGENET = 'https://stagenet-midgard.ninerealms.com'
        TESTNET = 'https://testnet.midgard.thorchain.info'
