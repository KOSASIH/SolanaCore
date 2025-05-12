use anchor_lang::prelude::*;
use anchor_spl::token::{Mint, Token, TokenAccount};

declare_id!("YourESATEProgramId");

#[program]
pub mod esate {
    use super::*;

    pub fn tokenize_asset(
        ctx: Context<TokenizeAsset>,
        asset_id: String,
        amount: u64,
    ) -> Result<()> {
        let asset = &mut ctx.accounts.asset;
        asset.asset_id = asset_id;
        asset.amount = amount;
        token::mint_to(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                token::MintTo {
                    mint: ctx.accounts.mint.to_account_info(),
                    to: ctx.accounts.token_account.to_account_info(),
                    authority: ctx.accounts.authority.to_account_info(),
                },
            ),
            amount,
        )?;
        emit!(AssetTokenized { asset_id, amount });
        Ok(())
    }
}

#[derive(Accounts)]
pub struct TokenizeAsset<'info> {
    #[account(init, payer = payer, space = 8 + 64)]
    pub asset: Account<'info, Asset>,
    #[account(mut)]
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub token_account: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct Asset {
    pub asset_id: String,
    pub amount: u64,
}

#[event]
pub struct AssetTokenized {
    pub asset_id: String,
    pub amount: u64,
}
