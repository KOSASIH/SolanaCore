from fastapi import FastAPI, HTTPException, WebSocket, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from anchorpy import Program, Provider, Wallet
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import uvicorn
import json
import httpx
import tensorflow as tf
import numpy as np
from typing import List, Dict, Optional
from websocket import WebSocketApp
from ipfshttpclient import client as IPFSClient
from src.crhai.fraud_detection import CRHAIFraudDetector
from src.solana import get_solana_client, get_anchor_program
from src.utils import load_config

# Load environment variables
load_dotenv()
config = load_config()

SOLANA_RPC_URL = config["solana_rpc_url"]
PI_COIN_PROGRAM_ID = config["pi_coin_program_id"]
GOVERNANCE_PROGRAM_ID = config["governance_program_id"]
BRIDGE_PROGRAM_ID = config["bridge_program_id"]
QECL_PROGRAM_ID = config.get("qecl_program_id")
IAOLP_PROGRAM_ID = config.get("iaolp_program_id")
ESATE_PROGRAM_ID = config.get("esate_program_id")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "quantum-secure-secret")
ALGORITHM = "HS256"  # Upgrade to quantum-resistant algorithm in production
IPFS_API = os.getenv("IPFS_API", "/ip4/127.0.0.1/tcp/5001")

app = FastAPI(
    title="PiCore Intergalactic DeFi API",
    description="Ultra high-tech backend for PiCore DeFi Ecosystem on Solana, with quantum security, AI analytics, and interplanetary capabilities.",
    version="1.0.0",
)

# OAuth2 for quantum-secured authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class WalletBalanceRequest(BaseModel):
    wallet_address: str

class ProposalRequest(BaseModel):
    proposal_id: int

class TransferRequest(BaseModel):
    wallet_address: str
    amount: int
    target_chain: int
    target_address: str

class QuantumProofRequest(BaseModel):
    proof: str
    public_inputs: str

class TokenizeAssetRequest(BaseModel):
    asset_id: str
    amount: int

class LiquidityRequest(BaseModel):
    amount: int
    market_data: Dict

class AuthRequest(BaseModel):
    wallet_address: str
    signature: str

# Initialize IPFS client
ipfs_client = IPFSClient(IPFS_API)

# Initialize CRHAI fraud detector
fraud_detector = CRHAIFraudDetector("models/crhai_fd_model.h5")

# JWT authentication
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        wallet_address: str = payload.get("sub")
        if wallet_address is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return wallet_address
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Token generation
@app.post("/token")
async def login(request: AuthRequest):
    # Placeholder: Verify Solana signature
    try:
        # Implement signature verification with solana.web3.js or similar
        access_token_expires = timedelta(minutes=30)
        access_token = jwt.encode(
            {"sub": request.wallet_address, "exp": datetime.utcnow() + access_token_expires},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Wallet balance with token support
@app.post("/wallet/balance")
async def get_wallet_balance(
    request: WalletBalanceRequest,
    wallet_address: str = Depends(get_current_user),
):
    try:
        client = await get_solana_client()
        wallet_pubkey = PublicKey(request.wallet_address)
        balance = await client.get_balance(wallet_pubkey)
        # Query pi-coin token account
        pi_coin_program = await get_anchor_program(
            PI_COIN_PROGRAM_ID, "../../programs/idl/pi_coin.json"
        )
        token_accounts = await client.get_token_accounts_by_owner(wallet_pubkey)
        pi_coin_balance = 0
        for account in token_accounts.value:
            account_data = await client.get_token_account_balance(account.pubkey)
            pi_coin_balance += int(account_data.value.amount) / 1_000_000_000  # Convert to Pi
        # Log to IPFS
        log_data = json.dumps({"wallet": request.wallet_address, "timestamp": str(datetime.utcnow())})
        ipfs_hash = ipfs_client.add_str(log_data)
        return {
            "wallet_address": request.wallet_address,
            "sol_balance": balance.value / 1_000_000_000,
            "pi_coin_balance": pi_coin_balance,
            "ipfs_log": ipfs_hash,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await client.close()

# Governance proposal with quantum validation
@app.post("/governance/proposal")
async def get_proposal(
    request: ProposalRequest,
    wallet_address: str = Depends(get_current_user),
):
    try:
        governance_program = await get_anchor_program(
            GOVERNANCE_PROGRAM_ID, "../../programs/idl/governance.json"
        )
        proposal_account = PublicKey.find_program_address(
            [b"proposal", request.proposal_id.to_bytes(8, "little")],
            PublicKey(GOVERNANCE_PROGRAM_ID),
        )[0]
        proposal_data = await governance_program.account["Proposal"].fetch(proposal_account)
        # Validate with QECL
        qecl_program = await get_anchor_program(
            QECL_PROGRAM_ID, "../../programs/idl/qecl.json"
        )
        quantum_valid = await qecl_program.rpc["validateQuantumProof"](
            "dummy_proof", "dummy_inputs"  # Replace with actual proof
        )
        return {
            "proposal_id": request.proposal_id,
            "description": proposal_data.description,
            "yes_votes": proposal_data.yes_votes,
            "no_votes": proposal_data.no_votes,
            "executed": proposal_data.executed,
            "quantum_validated": bool(quantum_valid),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Cross-chain transfer with AI fraud detection
@app.post("/bridge/transfer")
async def initiate_cross_chain_transfer(
    request: TransferRequest,
    wallet_address: str = Depends(get_current_user),
):
    try:
        # Check for fraud
        fraud_result = await fraud_detector.detect_fraud("pending_tx_id")  # Replace with actual tx_id
        if fraud_result["is_fraudulent"]:
            raise HTTPException(status_code=403, detail="Transaction flagged as fraudulent")
        bridge_program = await get_anchor_program(
            BRIDGE_PROGRAM_ID, "../../programs/idl/bridge.json"
        )
        tx = await bridge_program.rpc["lockAndTransfer"](
            request.amount,
            request.target_chain,
            bytes.fromhex(request.target_address),
            {"sender": PublicKey(request.wallet_address)},
        )
        # Log to IPFS
        log_data = json.dumps({"tx_id": tx, "timestamp": str(datetime.utcnow())})
        ipfs_hash = ipfs_client.add_str(log_data)
        return {
            "transaction_id": tx,
            "amount": request.amount,
            "target_chain": request.target_chain,
            "target_address": request.target_address,
            "ipfs_log": ipfs_hash,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Liquidity pool optimization
@app.post("/iaolp/optimize")
async def optimize_liquidity(
    request: LiquidityRequest,
    wallet_address: str = Depends(get_current_user),
):
    try:
        iaolp_program = await get_anchor_program(
            IAOLP_PROGRAM_ID, "../../programs/idl/iaolp.json"
        )
        # Placeholder: Call AI model
        model = tf.keras.models.load_model("models/iaolp_model.h5")
        inputs = np.array([request.market_data["price"], request.market_data["volume"]])
        prediction = model.predict(inputs.reshape(1, -1))
        tx = await iaolp_program.rpc["provideLiquidity"](
            request.amount,
            {"user": PublicKey(wallet_address)},
        )
        return {
            "transaction_id": tx,
            "recommended_liquidity": float(prediction[0]),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Tokenize space assets
@app.post("/esate/tokenize")
async def tokenize_asset(
    request: TokenizeAssetRequest,
    wallet_address: str = Depends(get_current_user),
):
    try:
        esate_program = await get_anchor_program(
            ESATE_PROGRAM_ID, "../../programs/idl/esate.json"
        )
        tx = await esate_program.rpc["tokenizeAsset"](
            request.asset_id,
            request.amount,
            {"authority": PublicKey(wallet_address)},
        )
        return {
            "transaction_id": tx,
            "asset_id": request.asset_id,
            "amount": request.amount,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Quantum proof validation
@app.post("/qecl/validate")
async def validate_quantum_proof(
    request: QuantumProofRequest,
    wallet_address: str = Depends(get_current_user),
):
    try:
        qecl_program = await get_anchor_program(
            QECL_PROGRAM_ID, "../../programs/idl/qecl.json"
        )
        tx = await qecl_program.rpc["validateQuantumProof"](
            request.proof,
            request.public_inputs,
            {"validator": PublicKey(wallet_address)},
        )
        return {"transaction_id": tx}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# WebSocket for real-time updates
@app.websocket("/ws/transactions")
async def websocket_transactions(websocket: WebSocket):
    await websocket.accept()
    client = await get_solana_client()
    try:
        subscription_id = await client.subscribe_transaction_confirmation(
            lambda tx: websocket.send_json({"tx_id": tx["transaction_id"], "status": "confirmed"})
        )
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await client.unsubscribe(subscription_id)
        await client.close()
        await websocket.close()

# Interplanetary transaction routing
@app.post("/interplanetary/route")
async def route_interplanetary_transaction(
    request: TransferRequest,
    wallet_address: str = Depends(get_current_user),
):
    try:
        # Placeholder: Latency-aware routing for interplanetary nodes
        latency = 0.1  # Simulate Mars node latency
        bridge_program = await get_anchor_program(
            BRIDGE_PROGRAM_ID, "../../programs/idl/bridge.json"
        )
        tx = await bridge_program.rpc["lockAndTransfer"](
            request.amount,
            request.target_chain,
            bytes.fromhex(request.target_address),
            {"sender": PublicKey(request.wallet_address)},
        )
        return {
            "transaction_id": tx,
            "estimated_latency": latency,
            "node": "mars-relayer-1",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)))
