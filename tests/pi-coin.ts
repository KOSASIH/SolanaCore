import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { PiCoin } from "../target/types/pi_coin";

describe("pi-coin", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.PiCoin as Program<PiCoin>;

  it("Initializes mint", async () => {
    const mint = anchor.web3.Keypair.generate();
    const tx = await program.methods
      .initializeMint(provider.wallet.publicKey)
      .accounts({
        mint: mint.publicKey,
        authority: provider.wallet.publicKey,
        payer: provider.wallet.publicKey,
        rent: anchor.web3.SYSVAR_RENT_PUBKEY,
        tokenProgram: anchor.utils.token.TOKEN_PROGRAM_ID,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([mint])
      .rpc();
    console.log("Mint initialized:", tx);
  });
});
