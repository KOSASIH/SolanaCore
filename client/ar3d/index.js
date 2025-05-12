import * as solanaWeb3 from '@solana/web3.js';
import * as AR from 'ar.js';

const connection = new solanaWeb3.Connection('https://api.devnet.solana.com', 'confirmed');

async function visualizeTransaction(txId) {
    const tx = await connection.getTransaction(txId);
    const scene = new AR.Scene();
    const geometry = new AR.SphereGeometry(0.5, 32, 32);
    const material = new AR.MeshBasicMaterial({ color: 0x00ff00 });
    const sphere = new AR.Mesh(geometry, material);
    sphere.position.set(tx.meta.fee / 1_000_000_000, 0, 0); // Scale by fee
    scene.add(sphere);
    return scene;
}

// Render AR scene in browser
document.addEventListener('DOMContentLoaded', () => {
    const arToolkit = new AR.Toolkit({
        source: new AR.ToolkitSource({ sourceType: 'webcam' }),
        context: new AR.ToolkitContext({ cameraParametersUrl: 'data/camera_para.dat' }),
    });
    arToolkit.init(() => {
        visualizeTransaction('sampleTxId').then(scene => {
            arToolkit.context.update();
            document.body.appendChild(scene.domElement);
        });
    });
});
