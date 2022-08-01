
import click
from satori.lib.wallet import verify as satori_verify

@click.group()
def main():
    '''Satori CLI'''

@main.command()
def help():
    '''open this file to modify'''
    print('used to verify a signed message')

@main.command()
@click.argument('message', type=str, required=True)
@click.argument('signature', type=str, required=True)
@click.argument('pubkey', type=str, required=True)
def verify(message: str, signature:str, pubkey:str):
    '''verifies a message and signature and public key'''
    print(satori_verify(
        message=message,
        signature=signature,
        publicKey=pubkey
    ))

@main.command()
@click.argument('message', type=str, required=True)
@click.argument('signature', type=str, required=True)
@click.argument('address', type=str, required=True)
def verifyByAddress(message: str, signature:str, address:str):
    '''verifies a message and signature and address'''
    print(satori_verify(
        message=message,
        signature=signature,
        address=address
    ))