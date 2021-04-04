import os
import binascii
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc
from iroha.primitive_pb2 import can_set_my_account_detail
import sys

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required')

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '172.29.101.121')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

# user_private_key = IrohaCrypto.private_key()
# user_public_key = IrohaCrypto.derive_public_key(user_private_key)
iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))

def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """

    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result

    return tracer

@trace
def send_transaction_and_print_status(transaction):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
        print(status)

@trace
def create_asset():
    """
    Creates asset 'coolcoin#test' with precision 2
    """
    commands = [
        iroha.command('CreateAsset', asset_name='coolcoin',
                      domain_id='test', precision=2)
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

@trace
def add_coin_to_admin():
    """
    Add 1000.00 units of 'coolcoin#test' to 'admin@test'
    """
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id='coolcoin#test', amount='1000.00')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

@trace
def transfer_coin_from_admin_to_test_user():
    """
    Transfer 200.45 'coolcoin#test' from 'admin@test' to 'test@test'
    """
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id='test@test',
                      asset_id='coolcoin#test', description='Sending colcoin', amount='200.45')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


create_asset()
add_coin_to_admin()
transfer_coin_from_admin_to_test_user()
