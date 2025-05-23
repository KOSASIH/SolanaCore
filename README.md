<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/KOSASIH/SolanaCore">PiCore Intergalactic DeFi Ecosystem</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://www.linkedin.com/in/kosasih-81b46b5a">KOSASIH</a> is licensed under <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Creative Commons Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""></a></p>

# PiCore Intergalactic DeFi Ecosystem

A revolutionary DeFi platform on Solana, empowering Pi Coin as a stablecoin pegged at 1 Pi = $314,159. Features include intergalactic payments, decentralized governance, cross-chain interoperability, and AI-driven analytics for terrestrial and space-based economies.

## Features
- Pi Coin Stablecoin: Pegged at $314,159 with algorithmic and collateralized stabilization.
- Intergalactic Payments: Ultra-fast transactions for terrestrial and hypothetical space use cases.
- PiCore Galactic DAO: Community-driven governance for ecosystem upgrades.
- Cross-Chain Bridge: Interoperability with Pi Network, Ethereum, and more via Wormhole.
- AI Analytics: Fraud detection and resource optimization with Cosmic Radiation Hardened AI.

## Backend API (Ultra High-Tech)
A FastAPI backend with quantum-secured authentication, AI fraud detection, WebSocket notifications, and interplanetary transaction routing.

### Features
- **Quantum JWT**: Secure access with quantum-resistant authentication.
- **WebSocket Updates**: Real-time transaction and governance notifications.
- **CRHAI Fraud Detection**: AI-powered transaction monitoring.
- **Interplanetary Routing**: Latency-aware transaction orchestration.
- **IPFS Logging**: Decentralized storage for API metadata.
- **New Program Support**: QECL, IAOLP, and ESATE integration.

See `api/README.md` for setup.

## Getting Started
1. Clone the repo: `git clone https://github.com/KOSASIH/SolanaCore`
2. Install dependencies: See `docs/user-guide.md`.
3. Deploy Solana programs: Follow `programs/README.md`.

## Contributing
See `CONTRIBUTING.md` for guidelines. Join our community on X (@Kosasihg88G) and Discord.

## License
MIT License



<br/>
<p align="center">
<a href="https://chain.link" target="_blank">
<img src="./solana_logo.png" width="225" alt="Chainlink Solana logo">
</a>
</p>
<br/>

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/smartcontractkit/solana-starter-kit)


# Chainlink Solana Starter Kit
The Chainlink Solana Starter Kit is an [Anchor](https://project-serum.github.io/anchor/getting-started/introduction.html) based program and client that shows developers how to use and interact with [Chainlink Price Feeds on Solana](https://docs.chain.link/solana/). The demo is configured to run on the [Devnet cluster](https://docs.solana.com/clusters#devnet), and is comprised of an on-chain program written in Rust, and an off-chain client written in JavaScript. The program takes parameters and account information from the off-chain client, retrieves the latest price data from the specified Chainlink Price Feed on Devnet, then writes the data out to the specified account, which can then be read by the off-chain client.

## Running the example on Devnet

### Requirements
- [NodeJS 12](https://nodejs.org/en/download/) or higher
- [Rust](https://www.rust-lang.org/tools/install)
- [Solana CLI](https://docs.solanalabs.com/cli/install)
- [Anchor](https://book.anchor-lang.com/getting_started/installation.html)
- A C compiler such as the one included in [GCC](https://gcc.gnu.org/install/).

### Building and Deploying the Consumer Program

First, ensure that you're in the `solana-starter-kit` directory in this repository

```
cd ./solana-starter-kit
```

Next step is to install all of the required dependencies:

```
npm install
```

**Note for [Apple M1](https://en.wikipedia.org/wiki/Apple_M1) chipsets**: You will need to perform an extra step to get the Anchor framework installed manually from source, as the NPM package only support x86_64 chipsets currently, please run the following command to install it manually:

```
cargo install --git https://github.com/coral-xyz/anchor --tag v0.30.1 anchor-cli --locked
```


Next, generate a new wallet:

```
solana-keygen new -o id.json
```

You should see the public key in the terminal output. Alternatively, you can find the public key  with the following CLI command:

```
solana-keygen pubkey id.json
```

Next, airdrop 5 SOL tokens into your new account. Be sure to replace both instances of <RECIPIENT_ACCOUNT_ADDRESS> with your wallet's public key from the previous step:

```
solana airdrop 5 $(solana-keygen pubkey ./id.json) --url https://api.devnet.solana.com
```

Next, build the program:

```
anchor build
```

The build process generates the keypair for your program's account. Before you deploy your program, you must update this public key in this line `lib.rs` file.
```
declare_id!("GEgDWT7Cc8H5S1o2YnTp3umiciazQj5fKbftPXkc2TsL");
``` 
To do this, you need to run the command below:
```
anchor keys sync
```

After this command, check the file `lib.rs` again. The line will be updated as below (you may find diffretn value within the `declare_id!()`)

```
declare_id!("JC16qi56dgcLoaTVe4BvnCoDL6FhH5NtahA7jmWZFdqm");
```

Finally, because you updated the source code with the generated program ID, you need to rebuild the program to regenerate the associated files for deployment, and then it can be deployed to devnet

```
anchor build
anchor deploy --provider.cluster devnet
```

Once you have successfully deployed the program, the terminal output will specify the program ID of the program, it should match the value you inserted into the `lib.rs` file and the `Anchor.toml` file. Once again, take note of this Program ID, as it will be required when executing the client:

```
Deploying workspace: https://api.devnet.solana.com
Upgrade authority: ./id.json
Deploying program "chainlink_solana_demo"...
Program path: ./target/deploy/chainlink_solana_demo.so...
Program Id: JC16qi56dgcLoaTVe4BvnCoDL6FhH5NtahA7jmWZFdqm
```

### Running the Client

The first step is to set the Anchor [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). These are required by the Anchor framework to determine which provider to use and which wallet to use for interacting with the deployed program:

```
export ANCHOR_PROVIDER_URL='https://api.devnet.solana.com'
export ANCHOR_WALLET='./id.json'
```

Now you are ready to run the JavaScript client. Be sure to pass Chainlink data feed address that you want to query. This can be taken from the [Chainlink Solana Data Feeds page](https://docs.chain.link/docs/solana/data-feeds-solana/), and the value will be defaulted to the Devnet SOL/USD feed address if you don’t specify a value. In this example, we specified the ETH/USD feed:

```
node client.js --feed	669U43LNHx7LsVj95uYksnhXUfWKDsdzVqev3V4Jpw3P
```

The client will generate a new account and pass it to the deployed program, which will then populate the account with the current price from the specified price feed. The client will then read the price from the account, and output the value to the console.

```
Running client...
priceFeedAccount public key: DNQBqwGijKix2EmKhMMaftZgSywcbfnQZSzfDyEMEfLf
user public key: GWKzUMdSF8Y4xQ3JANTChkaJDFE4UdkvAkHCknmJtJUX
Fetching transaction logs...
[
  'Program BrEqc6zHVR77jrP6U6WZLUV24AZ9UnHrWfDQTDV7VoDY invoke [1]',
  'Program log: Instruction: Execute',
  'Program 11111111111111111111111111111111 invoke [2]',
  'Program 11111111111111111111111111111111 success',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny invoke [2]',
  'Program log: Instruction: Query',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny consumed 2551 of 1360424 compute units',
  'Program return: HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny RZ0GABn5swcAAAAA3ltiYgAVg8dFAAAAAAAAAAAAAAA=',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny success',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny invoke [2]',
  'Program log: Instruction: Query',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny consumed 2245 of 1328033 compute units',
  'Program return: HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny CQAAAEVUSCAvIFVTRA==',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny success',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny invoke [2]',
  'Program log: Instruction: Query',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny consumed 1826 of 1295650 compute units',
  'Program return: HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny CA==',
  'Program HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny success',
  'Program log: ETH / USD price is 2997.00000000',
  'Program BrEqc6zHVR77jrP6U6WZLUV24AZ9UnHrWfDQTDV7VoDY consumed 109699 of 1400000 compute units',
  'Program return: BrEqc6zHVR77jrP6U6WZLUV24AZ9UnHrWfDQTDV7VoDY CA==',
  'Program BrEqc6zHVR77jrP6U6WZLUV24AZ9UnHrWfDQTDV7VoDY success'
]
Price Is: 2997
Success
```

### Running the Read Only Clients

To facilitate the scenario of purely requiring Chainlink Price Feed data off-chain, we have also included a second `read-data` client that queries a specified price feed and returns the latest price data. This version of the client does not generate a transaction, and therefore requires no accounts created or transaction fees. To run the read-data client, first you should ensure you have set the required Anchor environment variables. You can skip this step if you already did it earlier before running the normal client:

```
export ANCHOR_PROVIDER_URL='https://api.devnet.solana.com'
export ANCHOR_WALLET='./id.json'
```

Next, you can set the value of the `CHAINLINK_FEED_ADDRESS` static variable to the value of the [Price Feed account address](https://docs.chain.link/docs/solana/data-feeds-solana/) that you wish to query. This example queries the ETH/USD feed on Devnet:


```
const CHAINLINK_FEED_ADDRESS="669U43LNHx7LsVj95uYksnhXUfWKDsdzVqev3V4Jpw3P"
```

Once you save your file, you can then execute the client. There is a [Typescript](https://github.com/smartcontractkit/solana-starter-kit/blob/main/read-data.ts) and a [JavaScript](https://github.com/smartcontractkit/solana-starter-kit/blob/main/read-data.js) version:

Typescript:

```
npm run read-data
```

JavaScript:
```
node read-data.js
```

The client will query the specified price feed using the published [Chainlink Solana NPM package](https://www.npmjs.com/package/@chainlink/solana-sdk), and will then continuously just print the latest price to the console.

```
pappas99@Pappas solana-starter-kit % npm run read-data
> @ read-data /Users/pappas99/GitHub/22-hackathon/solana-starter-kit
> ts-node ./read-data.ts

301296000000
301250000000
301215000000
301205000000
301331000000
```


### Testing

You can execute the [integration test](./tests/chainlink-solana-demo-int-test.ts) with the following command

```bash
anchor test
```

The integration test checks that the value of the specified price feed account (defaulted to SOL/USD) on Devnet is greater than 0.

```bash
 solana-starter-kit

Price Is: 105.52
    ✔ Query SOL/USD Price Feed! (4521ms)


  1 passing (5s)

✨  Done in 10.49s.
```
