from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from anchorpy import Program, Provider, Wallet
import json

async def get_solana_client(rpc_url: str):
    return AsyncClient(rpc_url)

async def get_anchor_program(program_id: str, idl_path: str, rpc_url: str):
    client = await get_solana_client(rpc_url)
    provider = Provider(client, Wallet.dummy())
    with open(idl_path, "r") as f:
        idl = json.load(f)
    return Program(idl, PublicKey(program_id), provider)
