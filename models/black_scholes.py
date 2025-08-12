from .base_option import BaseOption
import logging
import numpy as np
from scipy.stats import norm


logger = logging.getLogger(__name__)

class BlackScholesOption(BaseOption):
    """Implements the Black-Scholes option pricing model for European options.

    This class provides methods to compute the price of a European call or put option,
    as well as the option's Greeks (Delta, Gamma, Vega, Theta, and Rho).
    Inherits from the BaseOption class.

    Attributes:
        S (float): Spot price of the underlying asset.
        K (float): Strike price of the option.
        T (float): Time to maturity (in years).
        r (float): Risk-free interest rate.
        sigma (float): Volatility of the underlying asset.
        option_type (str): Type of the option ('call' or 'put').
    """

    def d1(self) -> float:
        """Calculates the d1 term used in the Black-Scholes formula.

        Returns:
            float: The computed d1 value.
        """

        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
    
    def d2(self) -> float:
        """Calculates the d2 term used in the Black-Scholes formula.

        Returns:
            float: The computed d2 value.
        """
        
        return self.d1() - self.sigma * np.sqrt(self.T)

    def price(self) -> float:
        """Calculates the theoretical Black-Scholes price of the option.

        Returns:
            float: The option price.
        """

        logger.info(f"Calculating BS price for {self.option_type} option")
        
        d1 = self.d1()

        d2 = self.d2()

        if self.option_type == "call":
            price = self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        else:
            price = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
        
        logger.info(f"Calculated price: {price}")
        return price
    
    def delta(self) -> float:
        """Computes the Delta of the option, which measures sensitivity to the underlying asset price.

        Returns:
            float: The Delta of the option.
        """

        d1 = self.d1()
        if self.option_type == "call":
            return norm.cdf(d1)
        else:
            return norm.cdf(d1) - 1

    def gamma(self) -> float:
        """Computes the Gamma of the option, which measures the rate of change of Delta.

        Returns:
            float: The Gamma of the option.
        """

        d1 = self.d1()
        return norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self) -> float:
        """Computes the Vega of the option, which measures sensitivity to volatility.

        Returns:
            float: The Vega of the option, scaled per 1% change in volatility.
        """

        d1 = self.d1()
        return self.S * norm.pdf(d1) * np.sqrt(self.T) / 100

    def theta(self) -> float:
        """Computes the Theta of the option, which measures sensitivity to time decay.

        Returns:
            float: The Theta of the option, expressed per day.
        """

        d1 = self.d1()
        d2 = self.d2()
        if self.option_type == "call":
            term1 = -(self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
            term2 = -self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
            return (term1 + term2) / 365  # par jour
        else:
            term1 = -(self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
            return (term1 + term2) / 365  # par jour

    def rho(self) -> float:
        """Computes the Rho of the option, which measures sensitivity to the interest rate.

        Returns:
            float: The Rho of the option, scaled per 1% change in interest rate.
        """

        d2 = self.d2()
        if self.option_type == "call":
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2) / 100
        else:
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2) / 100

    def greeks(self) -> dict:
        """Returns a dictionary containing all major Greeks for the option.

        Returns:
            dict: A dictionary with keys 'delta', 'gamma', 'vega', 'theta', and 'rho'.
        """

        return {
            "delta": self.delta(),
            "gamma": self.gamma(),
            "vega": self.vega(),
            "theta": self.theta(),
            "rho": self.rho(),
        }

    def payoff_array(self, spot_range: np.ndarray) -> np.ndarray:
        """Compute the payoff of the option at maturity for a given range of spot prices.
        
        Args:
            spot_range (np.ndarray): Array of spot prices at maturity.

        Returns:
            np.ndarray: Payoff values (without accounting for the option premium).
        """

        if self.option_type == 'call':
            return np.maximum(spot_range - self.K, 0)
        elif self.option_type == 'put':
            return np.maximum(self.K - spot_range, 0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    def pnl_array(self, spot_range: np.ndarray, direction: str = 'long', price: float = None) -> np.ndarray:
        """Compute the PnL profile of the option (payoff net of the option premium).
        
        Args:
            spot_range (np.ndarray): Array of spot prices at maturity.
            direction (str): 'long' or 'short' position.
            price (float, optional): Price of the option. If None, it will be computed.

        Returns:
            np.ndarray: Profit and loss values for each spot price in the range.
        """

        payoff = self.payoff_array(spot_range)
        if price is None:
            price = self.price()

        if direction == 'long':
            return payoff - price
        elif direction == 'short':
            return -(payoff - price)
        else:
            raise ValueError("direction must be 'long' or 'short'")