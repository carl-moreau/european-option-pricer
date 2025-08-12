from .base_option import BaseOption
import logging
from typing import Optional
import numpy as np
from scipy.stats import norm

logger = logging.getLogger(__name__)

class MonteCarloOption(BaseOption):
    """European option pricer using Monte Carlo simulation.

    This class implements pricing of European call and put options using
    simulated terminal prices of the underlying asset under the risk-neutral measure.
    Inherits from the BaseOption class.

    Args:
        S (float): Spot price of the underlying asset.
        K (float): Strike price of the option.
        T (float): Time to maturity (in years).
        r (float): Risk-free interest rate.
        sigma (float): Volatility of the underlying asset.
        option_type (str, optional): Type of the option, either 'call' or 'put'. Defaults to 'call'.
        seed (int, optional): Random seed for reproducibility of simulations.
    """

    def __init__(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: str = 'call',
        seed: Optional[int] = None  # Set a random seed for reproducibility, if provided
    ):
        super().__init__(S, K, T, r, sigma, option_type)
        if seed is not None:
            np.random.seed(seed)
    

    def price(self, n_simulations):
        """Estimate the price of a European option using Monte Carlo simulation.

        Simulates terminal prices of the underlying asset using a geometric Brownian motion (GBM)
        and calculates the expected discounted payoff under the risk-neutral measure.

        Args:
            n_simulations (int): Number of Monte Carlo paths to simulate.

        Returns:
            float: The estimated option price.
        """

        logger.info(f"Calculating MC price with {n_simulations} simulations")

        Z = np.random.standard_normal(n_simulations)
        
        # Simulate terminal asset prices under the risk-neutral measure (Q)
        ST = self.S * np.exp((self.r - 0.5 * self.sigma**2) * self.T + self.sigma * np.sqrt(self.T) * Z)

        if self.option_type == "call":
            payoff = np.maximum(ST - self.K, 0)
        else:
            payoff = np.maximum(self.K - ST, 0)

        price = np.exp(-self.r * self.T) * np.mean(payoff)

        logger.info(f"Calculated price: {price}")
        return price