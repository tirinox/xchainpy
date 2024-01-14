import sys
from os.path import dirname


sys.path.append(dirname(__file__))

try:
    from .mayachain.v1.common.common_pb2 import Coin as THORCoin, Asset as THORAsset
    from .mayachain.v1.x.mayachain.types.msg_deposit_pb2 import MsgDeposit
    from .mayachain.v1.x.mayachain.types.msg_send_pb2 import MsgSend
except TypeError:
    """
    At the time of writing the code, the structure of these classes is identical in both TC and Maya.
    Therefore, the classes are interchangeable.
    If the classes split up, this approach will no longer work.
    """
    from xchainpy2_thorchain.proto.thorchain.v1.common.common_pb2 import Coin as THORCoin, Asset as THORAsset
    from xchainpy2_thorchain.proto.thorchain.v1.x.thorchain.types.msg_deposit_pb2 import MsgDeposit
    from xchainpy2_thorchain.proto.thorchain.v1.x.thorchain.types.msg_send_pb2 import MsgSend
