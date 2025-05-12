import { useWallet } from "@solana/wallet-adapter-react";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";
import Head from "next/head";

export default function Home() {
  const { publicKey } = useWallet();

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Head>
        <title>PiCore Intergalactic DeFi</title>
      </Head>
      <header className="p-4 flex justify-between">
        <h1 className="text-2xl">PiCore</h1>
        <WalletMultiButton />
      </header>
      <main className="p-4">
        <h2 className="text-xl">Welcome to PiCore</h2>
        {publicKey ? (
          <p>Connected: {publicKey.toBase58()}</p>
        ) : (
          <p>Connect your wallet to start.</p>
        )}
      </main>
    </div>
  );
}
