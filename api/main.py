from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from anchorpy import Program, Provider, Wallet
from dotenv import load_dotenv
import os
import uvicorn
import json
import httpx

# Load environment variables
load_dotenv()

SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")
PI_COIN_PROGRAM_ID = os.getenv("PI_COIN_PROGRAM_ID")
GOVERNANCE_PROGRAM_ID = os.getenv("GOVERNANCE_PROGRAM_ID")
BRIDGE_PROGRAM_ID = os.getenv("BRIDGE_PROGRAM_ID")

app = FastAPI(
    title="PiCore Intergalactic DeFi API",
    description="Backend API for PiCore DeFi Ecosystem on Solana",
    version="0.1.0",
)

# Pydantic models for request/response validation
class WalletBalanceRequest(BaseModel):
    wallet_address: str

class ProposalRequest(BaseModel):
    proposal_id: int

class TransferRequest(BaseModel):
    wallet_address: str
    amount: int
    target_chain: int
    target_address: str

# Initialize Solana client
async def get_solana_client():
    return AsyncClient(SOLANA_RPC_URL)

# Placeholder: Load Anchor program (requires IDL file)
async def get_program(program_id: str, idl_path: str):
    client = await get_solana_client()
    provider = Provider(client, Wallet.dummy())
    with open(idl_path, "r") as f:
        idl = json.load(f)
    return Program(idl, PublicKey(program_id), provider)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/wallet/balance")
async def get_wallet_balance(request: WalletBalanceRequest):
    try:
        client = await get_solana_client()
        wallet_pubkey = PublicKey(request.wallet_address)
        # Placeholder: Query pi-coin token account balance
        balance = await client.get_balance(wallet_pubkey)
        return {
            "wallet_address": request.wallet_address,
            "balance": balance.value / 1_000_000_000,  # Convert lamports to SOL
            "pi_coin_balance": 0,  # Replace with actual token balance query
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await client.close()

@app.post("/governance/proposal")
async def get_proposal(request: ProposalRequest):
    try:
        # Placeholder: Fetch proposal from governance program
        governance_program = await get_program(
            GOVERNANCE_PROGRAM_ID, "../programs/governance/target/idl/governance.json"
        )
        # Example: Fetch proposal account
        proposal_account = PublicKey.find_program_address(
            [b"proposal", request.proposal_id.to_bytes(8, "little")],
            PublicKey(GOVERNANCE_PROGRAM_ID)
        )[0]
        proposal_data = await governance_program.account["Proposal"].fetch(proposal_account)
        return {
            "proposal_id": request.proposal_id,
            "description": proposal_data.description,
            "yes_votes": proposal_data.yes_votes,
            "no_votes": proposal_data.no_votes,
            "executed": proposal_data.executed,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/bridge/transfer")
async def initiate_cross_chain_transfer(request: TransferRequest):
    try:
        # Placeholder: Initiate cross-chain transfer via bridge program
        bridge_program = await get_program(
            BRIDGE_PROGRAM_ID, "../programs/bridge/target/idl/bridge.json"
        )
        # Example: Call lock_and_transfer instruction
        tx = await bridge_program.rpc["lockAndTransfer"](
            request.amount,
            request.target_chain,
            bytes.fromhex(request.target_address),
            {
                "sender": PublicKey(request.wallet_address),
                # Add other accounts as needed
            }
        )
        return {
            "transaction_id": tx,
            "amount": request.amount,
            "target_chain": request.target_chain,
            "target_address": request.target_address,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)))
