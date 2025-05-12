import { useState } from 'react';

export default function ARVisualizer() {
    const [txId, setTxId] = useState('');

    return (
        <div>
            <h2>Holographic Transaction Visualizer</h2>
            <input
                type="text"
                value={txId}
                onChange={(e) => setTxId(e.target.value)}
                placeholder="Enter Transaction ID"
            />
            <div id="ar-scene"></div>
        </div>
    );
}
