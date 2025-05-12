import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Bridge } from "../target/types/bridge";
import { PublicKey, Keypair } from "@solana/web3.js";
import { TOKEN_PROGRAM_ID, createMint, createAccount, mintTo } from "@solana/spl-token";

describe("bridge", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.Bridge as Program<Bridge>;
  let mint: PublicKey;
  let tokenAccount: PublicKey;
  let vault: PublicKey;
  let bridgeState: Keypair;

  before(async () => {
    // Set up mint and token accounts
    const mintKeypair = Keypair.generate();
    mint = await createMint(
      provider.connection,
      provider.wallet.payer,
      provider.wallet.publicKey,
      null,
      9
    );
    tokenAccount = await createAccount(
      provider.connection,
      provider.wallet.payer,
      mint,
      provider.wallet.publicKey
    );
    vault = await createAccount(
      provider.connection,
      provider.wallet.payer,
      mint,
      provider.wallet.publicKey
    );
    await mintTo(
      provider.connection,
      provider.wallet.payer,
      mint,
      tokenAccount,
      provider.wallet.publicKey,
      1000000
    );

    // Initialize bridge state
    bridgeState = Keypair.generate();
    const space = 8 + 8 + 8; // Discriminator + total_locked + total_minted
    await program.methods
      .initialize()
      .accounts({
        bridgeState: bridgeState.publicKey,
        payer: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([bridgeState])
      .rpc();
  });

  it("Locks and transfers tokens", async () => {
    const amount = 1000;
    const targetChain = 2; // Ethereum
    const targetAddress = new Array(32).fill(0); // Dummy address

    const tx = await program.methods
      .lockAndTransfer(new anchor.BN(amount), targetChain, targetAddress)
      .accounts({
        sender: provider.wallet.publicKey,
        tokenAccount,
        vault,
        bridgeState: bridgeState.publicKey,
        tokenProgram: TOKEN_PROGRAM_ID,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .rpc();

    console.log("Tokens locked:", tx);
  });

  it("Receives and mints tokens", async () => {
    const amount = 500;
    const sourceChain = 2;
    const sourceAddress = new Array(32).fill(0);
    const vaaHash = new Array(32).fill(0); // Dummy VAA hash

    const tx = await program.methods
      .receiveAndMint(vaaHash, new anchor.BN(amount), sourceChain, sourceAddress)
      .accounts({
        mint,
        recipientAccount: tokenAccount,
        mintAuthority: provider.wallet.publicKey,
        bridgeState: bridgeState.publicKey,
        tokenProgram: TOKEN_PROGRAM_ID,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .rpc();

    console.log("Tokens minted:", tx);
  });
});
