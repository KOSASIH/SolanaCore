from fastapi import HTTPException
import tensorflow as tf
import numpy as np

class IAOLPModel:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)

    async def optimize_yield(self, market_data: dict):
        inputs = np.array([market_data["price"], market_data["volume"]])
        prediction = self.model.predict(inputs.reshape(1, -1))
        return {"recommended_liquidity": float(prediction[0])}

iaolp_model = IAOLPModel("models/iaolp_model.h5")  # Train and save model separately
