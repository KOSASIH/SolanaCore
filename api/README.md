# PiCore Backend API

A FastAPI backend for the PiCore Intergalactic DeFi Ecosystem.

## Setup
1. Navigate to `api/`: `cd api`
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env`: `cp .env.example .env` and update variables.
6. Run: `python main.py`

## Endpoints
- `GET /health`: Check API status.
- `POST /wallet/balance`: Get wallet and Pi Coin balance.
- `POST /governance/proposal`: Fetch governance proposal details.
- `POST /bridge/transfer`: Initiate cross-chain transfer.

## Documentation
Access auto-generated docs at `http://localhost:8000/docs`.
