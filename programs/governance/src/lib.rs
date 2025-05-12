use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount};
use pi_coin::PiCoin; // Import pi-coin program for token integration

declare_id!("YourGovernanceProgramId"); // Replace with actual program ID

#[program]
pub mod governance {
    use super::*;

    pub fn create_proposal(
        ctx: Context<CreateProposal>,
        proposal_id: u64,
        description: String,
        voting_period: i64,
    ) -> Result<()> {
        let proposal = &mut ctx.accounts.proposal;
        proposal.id = proposal_id;
        proposal.description = description;
        proposal.creator = ctx.accounts.creator.key();
        proposal.voting_deadline = Clock::get()?.unix_timestamp + voting_period;
        proposal.yes_votes = 0;
        proposal.no_votes = 0;
        proposal.executed = false;
        Ok(())
    }

    pub fn vote(
        ctx: Context<Vote>,
        proposal_id: u64,
        vote_yes: bool,
        amount: u64,
    ) -> Result<()> {
        let proposal = &mut ctx.accounts.proposal;
        let voter_account = &ctx.accounts.voter_account;

        require!(!proposal.executed, GovernanceError::ProposalClosed);
        require!(
            Clock::get()?.unix_timestamp <= proposal.voting_deadline,
            GovernanceError::VotingPeriodEnded
        );
        require!(
            voter_account.amount >= amount,
            GovernanceError::InsufficientTokens
        );

        // Record vote
        let vote_record = &mut ctx.accounts.vote_record;
        vote_record.voter = ctx.accounts.voter.key();
        vote_record.proposal_id = proposal_id;
        vote_record.amount = amount;
        vote_record.vote_yes = vote_yes;

        // Update proposal vote counts
        if vote_yes {
            proposal.yes_votes += amount;
        } else {
            proposal.no_votes += amount;
        }

        Ok(())
    }

    pub fn execute_proposal(ctx: Context<ExecuteProposal>, proposal_id: u64) -> Result<()> {
        let proposal = &mut ctx.accounts.proposal;

        require!(!proposal.executed, GovernanceError::AlreadyExecuted);
        require!(
            Clock::get()?.unix_timestamp > proposal.voting_deadline,
            GovernanceError::VotingPeriodActive
        );
        require!(
            proposal.yes_votes > proposal.no_votes,
            GovernanceError::ProposalFailed
        );

        // Mark proposal as executed
        proposal.executed = true;

        // Placeholder: Execute proposal logic (e.g., transfer funds, update parameters)
        emit!(ProposalExecuted {
            proposal_id,
            executor: ctx.accounts.executor.key(),
        });

        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(proposal_id: u64)]
pub struct CreateProposal<'info> {
    #[account(
        init,
        payer = creator,
        space = 8 + Proposal::LEN,
        seeds = [b"proposal", proposal_id.to_le_bytes().as_ref()],
        bump
    )]
    pub proposal: Account<'info, Proposal。此外
