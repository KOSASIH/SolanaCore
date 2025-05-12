# PiCore Backend API

An ultra high-tech FastAPI backend for the PiCore Intergalactic DeFi Ecosystem.

## Setup
1. Navigate: `cd api`
2. Create venv: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Configure: `cp .env.example .env`
6. Run: `python main.py`

## Endpoints
- `POST /token`: Authenticate with Solana wallet.
- `GET /health`: Check API status.
- `POST /wallet/balance`: Get SOL and Pi Coin balances.
- `POST /governance/proposal`: Fetch governance proposals.
- `POST /bridge/transfer`: Initiate cross-chain transfers.
- `POST /iaolp/optimize`: Optimize liquidity with AI.
- `POST /esate/tokenize`: Tokenize space assets.
- `POST /qecl/validate`: Validate quantum proofs.
- `WS /ws/transactions`: Real-time transaction updates.
- `POST /interplanetary/route`: Route interplanetary transactions.

## Documentation
Visit `http://localhost:8000/docs`.
