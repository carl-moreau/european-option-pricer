from .base_option import BaseOption
import logging
import numpy as np


logger = logging.getLogger(__name__)

class BinomialOption(BaseOption):
    """
    European option priced using the Cox-Ross-Rubinstein binomial tree model.

    In this implementation, we construct a recombining tree of possible asset prices
    and compute the option payoff at maturity. We then use backward induction
    under the risk-neutral measure to determine the option's present value.
    Inherits from the BaseOption class.

    Attributes:
        S (float): Spot price of the underlying asset.
        K (float): Strike price of the option.
        T (float): Time to maturity (in years).
        r (float): Risk-free interest rate.
        sigma (float): Volatility of the underlying asset.
        option_type (str): Type of the option ('call' or 'put').
    """

    def price(self, steps:int) -> float:
        """Calculate the price of a European option using the binomial tree method.

        Args:
            steps (int): Number of discrete time steps in the binomial tree.

        Returns:
            float: Option price computed through backward induction.

        Notes:
            - This implementation uses a recombining binomial tree.
            - Because of recombination (i.e., u * d = d * u), the number of final nodes is only (steps + 1),
              not 2^steps as in a generic binary tree. This significantly improves computational efficiency.
        """
        
        logger.info(f"Calculating binomial price with {steps} steps")

        dt = self.T / steps # Time increment per step
        u = np.exp(self.sigma * np.sqrt(dt)) # Upward movement factor
        d = 1 / u # Downward movement factor
        p = (np.exp(self.r * dt) - d) / (u - d) # Risk-neutral probability of upward move

        # Initialize tree of underlying asset prices
        prices = np.zeros((steps + 1, steps + 1))
        for i in range(steps + 1): 
            prices[i, steps] = self.S * (u**(steps - i)) * (d**i) # Terminal asset prices at maturity

        # Initialize option values at maturity (payoff)
        values = np.zeros_like(prices)
        for i in range(steps + 1):
            if self.option_type == "call":
                values[i, steps] = max(prices[i, steps] - self.K, 0)
            else:
                values[i, steps] = max(self.K - prices[i, steps], 0)

        # Backward induction to compute present value
        for j in range(steps - 1, -1, -1):
            for i in range(j + 1):
                values[i, j] = np.exp(-self.r * dt) * (p * values[i, j + 1] + (1 - p) * values[i + 1, j + 1])

        price = values[0, 0] # Option price at the root of the tree (t=0)

        logger.debug(f"Calculated price: {price}")
        return price