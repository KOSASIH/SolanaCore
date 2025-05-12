import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "solana_rpc_url": os.getenv("SOLANA_RPC_URL"),
        "pi_coin_program_id": os.getenv("PI_COIN_PROGRAM_ID"),
        "governance_program_id": os.getenv("GOVERNANCE_PROGRAM_ID"),
        "bridge_program_id": os.getenv("BRIDGE_PROGRAM_ID"),
    }
