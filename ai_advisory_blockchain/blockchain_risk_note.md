# Blockchain & Crypto Risk Appendix — Paytm Money

## 1. "Paytm Crypto Insights" Watchlist Feature: Stablecoin & DeFi/DAO Governance Risk

If Paytm Money were to responsibly surface crypto information to retail users via a
"Paytm Crypto Insights" watchlist, the single most important distinction to get right
upfront is **stablecoin type**. Stablecoins are cryptocurrencies designed to hold a
steady value, typically pegged to a fiat currency, but they achieve this in very
different ways with very different risk profiles. **Fiat-collateralized stablecoins**
(e.g., USDC, USDT) are backed roughly 1:1 by cash and short-term securities held by
the issuer; their primary risk is counterparty and reserve-transparency risk — users
must trust that the issuer actually holds what it claims, and that those reserves are
regularly audited. **Algorithmic stablecoins**, by contrast, maintain their peg
through automated on-chain incentive mechanisms rather than real-world collateral.
These carry materially higher risk: the 2022 collapse of TerraUSD demonstrated that
algorithmic pegs can break suddenly and irreversibly once market confidence erodes,
wiping out holders' value within days. A watchlist feature must clearly label which
type each listed stablecoin is, since conflating the two gives retail users a false
sense of uniform safety.

The second risk area is **DeFi/DAO governance risk**. Many crypto assets and
protocols are governed not by a company with legal accountability, but by a
Decentralized Autonomous Organization (DAO), where holders of a governance token vote
on protocol changes. This introduces risks unfamiliar to traditional retail
investors: governance power can concentrate in a small number of large token holders
("whales"), protocol rules and fee structures can change with little notice following
a vote, and there is often no legal entity investors can pursue if a governance
decision harms them or if the protocol is exploited. For a regulated fintech platform
like Paytm, any watchlist feature should flag whether an asset's underlying protocol
is DAO-governed, and should avoid implying the same regulatory protections that apply
to listed securities or bank deposits.



## 2. Crypto as an Asset Class: A Portfolio Recommendation

Applying CAPM-style portfolio theory (the same framework used in this project's
advisory agent), an asset does not need to be individually safe to be worth including
in a diversified portfolio — it needs sufficiently low or negative correlation with
the investor's other holdings so that it reduces the portfolio's overall volatility.
Cryptocurrency's price movements are not perfectly correlated with equities, which is
the theoretical case in its favor. However, several features of crypto returns
complicate a naive application of this theory: crypto exhibits heavy-tailed
distributions (large, sudden crashes and spikes far more frequent than a normal
distribution would predict), the historical dataset suffers from survivorship bias
(thousands of tokens have simply failed and vanished from the record, inflating the
apparent historical performance of "crypto" as a category), and transaction costs
(spreads, gas fees, exchange withdrawal fees) are meaningfully higher than for listed
equities, eroding any diversification benefit through friction.

Given these factors, this note's recommendation for a retail advisory product is a
**maximum allocation of 3% of a portfolio's investable assets to cryptocurrency**,
and only for investors already classified as Moderate or Aggressive risk tolerance in
this project's framework. This figure is justified as follows: at 3%, even a
near-total loss of the crypto position would reduce total portfolio value by no more
than 3%, which is recoverable within a normal rebalancing cycle, while still allowing
the (theoretical) diversification benefit to register if crypto and equities decouple
during a market event. A Conservative-tolerance investor should receive a **justified
zero allocation**, since the asset class's heavy-tailed downside risk is
incompatible with capital preservation, which is the defining objective of a
Conservative risk profile in this project's investor model.



## 3. T.A.N.G. Fraud Framework: Social-Engineering Risk for a UPI/Wallet + Lending + Wealth App

The T.A.N.G. framework (Temptation, Authority, Need, Greed) categorizes the
psychological lever a social-engineering attacker exploits. For a combined
UPI/wallet, BNPL lending, and wealth-advisory platform like Paytm, the two most
relevant vectors are:

**Authority.** Because the app already handles payments, credit, and investments in
one place, users are conditioned to trust in-app prompts and messages that claim to
be from "Paytm Support," "RBI," or a partner bank — a common scam pattern is a fake
call or SMS instructing the user to approve a UPI collect request or share an OTP to
"verify" their account or "reverse a wrongful debit." **One-sided real-time defense:**
the app should never allow a UPI collect (pull) request above a low threshold to be
silently pre-filled or one-tap-approved when it originates from a payee the user has
never paid before; instead, first-time high-value collect requests should trigger a
mandatory cooling-off screen naming the payee's verified registration details
in large text, independent of whatever the accompanying SMS or call claims.

**Greed.** The wealth-advisory side of the app makes it a natural target for "double
your investment," fake trading-tip, or fraudulent high-return scheme messages that
direct users to move money outside the platform via UPI. **One-sided real-time
defense:** the platform can maintain a real-time graph-based anomaly model that flags
outbound UPI transfers to newly created or previously-flagged payee accounts that are
immediately followed by rapid onward transfers ("mule" account patterns), and
automatically hold such transfers for step-up verification — this defense works
independent of user awareness, since it detects the fraud pattern on the money-movement
side rather than relying on the user recognizing the scam themselves.