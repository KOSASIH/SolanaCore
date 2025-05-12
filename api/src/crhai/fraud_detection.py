import tensorflow as tf
from solana.rpc.async_api import AsyncClient
import numpy as np

class CRHAIFraudDetector:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)
        self.client = AsyncClient(os.getenv("SOLANA_RPC_URL"))

    async def detect_fraud(self, tx_id: str):
        tx = await self.client.get_transaction(tx_id)
        features = np.array([
            tx["meta"]["fee"],
            len(tx["transaction"]["message"]["accountKeys"]),
            tx["meta"]["postBalances"][0],
        ])
        prediction = self.model.predict(features.reshape(1, -1))
        return {"tx_id": tx_id, "is_fraudulent": prediction[0] > 0.5}

fraud_detector = CRHAIFraudDetector("models/crhai_fd_model.h5")  # Train and save model
