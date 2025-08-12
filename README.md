# Option Pricing Models

This project implements three classical option pricing models in Python, along with an interactive dashboard built using Streamlit, and a suite of unit tests to ensure correctness and numerical stability.

The implemented models are:

- **Black-Scholes**  
- **Binomial Tree (CRR)**  
- **Monte Carlo Simulation**

[Open the Streamlit App](https://carl-moreau-european-option-pricer-app.streamlit.app)

---

## Black-Scholes Model

The Black-Scholes model provides a closed-form solution for pricing European options under a set of simplifying assumptions. It models the asset price as following a geometric Brownian motion.

### Pricing Formulas

The price of a European call option is given by:

$$
C = S_0 \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)
$$

The price of a European put option is given by:

$$
P = K \cdot e^{-rT} \cdot N(-d_2) - S_0 \cdot N(-d_1)
$$

where:

$$
d_1 = \frac{\ln(S_0 / K) + \left(r + \frac{1}{2} \sigma^2\right) T}{\sigma \sqrt{T}}, \quad
d_2 = d_1 - \sigma \sqrt{T}
$$
$$ 
$$

- $K$: strike price  
- $r$: risk-free rate  
- $\sigma$ : volatility
- $T$: time to maturity  
- $N(\cdot)$: standard normal cumulative distribution function

### Model Assumptions
 
- Asset prices follow a lognormal distribution (i.e., log-returns are normally distributed and i.i.d.).
- The volatility of the asset is constant over time.
- The risk-free rate is known and constant. 
- Originally, no dividends are paid (though the model can be adapted to include them).  
- No transaction costs.  
- Underlying assets are divisible, allowing fractional trading.  
- Short selling is allowed.

### Option Greeks

The Greeks represent the sensitivities of the option's price with respect to underlying parameters. 


- Delta ($\delta$): Measures the sensitivity of the option price to changes in the price of the underlying asset. It indicates how much the option price is expected to move for a small change in the underlying.
- Gamma ($\gamma$): Measures the rate of change of Delta with respect to the underlying asset price. It shows how Delta will change as the underlying price changes, indicating the curvature of the option’s value.
- Vega (ν): Measures the sensitivity of the option price to changes in the volatility of the underlying asset. It reflects how the option value responds when the market expects more or less volatility.
- Theta ($\theta$): Represents the time decay of the option, showing how the option price decreases as time passes, assuming all other factors remain constant.
- Rho ($\rho$): Measures the sensitivity of the option price to changes in the risk-free interest rate. It shows how the option’s value reacts to shifts in interest rates.

---

## Binomial Tree Model (Cox-Ross-Rubinstein)

The Cox–Ross–Rubinstein (CRR) binomial tree is a discrete-time model for option pricing that simulates all possible paths the underlying asset price can take over the option’s lifetime.

The asset price evolution is modeled using a recombining binomial tree, where each node branches into two possible moves: up and down. Probabilities are assigned under the risk-neutral measure, allowing the model to price derivatives by backward induction.

As the number of time steps increases, the binomial model converges to the continuous-time Black–Scholes model.

### Parameters in the CRR Model

In the Cox–Ross–Rubinstein model, the parameters are set as:

$$
u = e^{\sigma \sqrt{\Delta t}}, \quad d = e^{-\sigma \sqrt{\Delta t}}, \quad p = \frac{e^{r \Delta t} - d}{u - d}
$$

where:
- $u$ = up factor per step
- $d$ = down factor per step
- $p$ = risk-neutral probability of an up move
- $\sigma$ = annualized volatility of the underlying
- $\Delta t$ = $\frac{T}{N}$ = time step length ($T$ = maturity, $N$ = number of steps)

---

## Monte Carlo Simulation

The Monte Carlo model simulates a large number of possible price paths for the underlying asset to compute an expected discounted payoff under the risk-neutral measure.

### Model Assumptions

The asset follows the same geometric Brownian motion as in Black-Scholes:

$$
dS_t = r S_t dt + \sigma S_t dW_t
$$

The simulation assumes:  
  - Constant interest rate $(r)$  
  - Constant volatility $(\sigma)$  
  - Frictionless markets and no arbitrage

### Pricing Logic

1. Simulate $N$ price paths at maturity using:

$$
S_T^{(i)} = S_0 \cdot e^{\left(r - \frac{1}{2} \sigma^2\right) T + \sigma \sqrt{T} Z^{(i)}}, \quad Z^{(i)} \sim \mathcal{N}(0, 1)
$$

2. Compute the payoff:
- $\max(S_T^{(i)} - K, 0)$ for calls
- $\max(K - S_T^{(i)}, 0)$ for puts


3. Discount and average the payoffs:

$$
V = e^{-rT} \cdot \frac{1}{N} \sum_{i=1}^{N} \text{payoff}^{(i)}
$$


---

## Streamlit Dashboard Features

The web-based dashboard allows users to explore and compare the models interactively:

- **Input parameters**:  
  - Spot price, strike, maturity, volatility, risk-free rate  
  - Choice of call or put  
- Model selection: Black-Scholes, Binomial (with adjustable steps), Monte Carlo (with custom simulation count and seed)  
- Real-time option pricing  
- Display of Greeks and PnL diagrams 
- Lightweight interface deployable to Streamlit Cloud

---

## Unit Tests Summary

The project includes a suite of unit tests (using `unittest`) to validate the correctness of the implementations and their convergence behavior.

### Black-Scholes

- `test_black_scholes_call` — Verifies the European call price.  
- `test_black_scholes_put` — Verifies the European put price.  
- `test_put_call_parity` — Ensures that put-call parity holds:

$$
C - P = S - K e^{-rT}
$$

- `test_deep_in_the_money_put` — Validates pricing in edge-case scenarios.

### Binomial Tree

- `test_convergence_with_iterations` — Checks that the binomial price converges to Black-Scholes as the number of steps increases.

### Monte Carlo

- `test_convergence_with_iterations` — Checks that Monte Carlo prices converge toward Black-Scholes with increased simulations.

Each test isolates and verifies a specific aspect of the pricing logic, promoting confidence in both theoretical consistency and numerical robustness.

---