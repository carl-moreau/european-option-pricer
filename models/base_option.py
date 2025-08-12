from abc import ABC, abstractmethod
from typing import Literal

class BaseOption(ABC):
    """Abstract base class for European-style options.

    This class provides a common interface for all pricing models related to European options.
    It enforces the implementation of a `price()` method in any subclass.

    Args:
        S (float): Spot price of the underlying asset.
        K (float): Strike price of the option.
        T (float): Time to maturity (in years).
        r (float): Risk-free interest rate.
        sigma (float): Volatility of the underlying asset.
        option_type (str): Option type, either 'call' or 'put'.

    Note:
        This base class is designed for European options only, which can be exercised
        only at expiration. Subclasses must implement the pricing logic specific to
        their respective models.
    """

    def __init__(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: Literal['call','put'] = 'call'
    ):
        self.validate_inputs(S, K, T, sigma)
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()
    
    @abstractmethod  # All pricing models (Black-Scholes, Binomial, Monte Carlo) must implement this method.
    def price(self) -> float:
        """Abstract method to compute the theoretical price of a European option.

        This method must be implemented by any subclass using a specific pricing model.

        Returns:
            float: The theoretical price of the option.
        """
    
        pass
    
    @staticmethod
    def validate_inputs(S: float, K: float, T: float, sigma: float) -> None:
        """Validate input parameters for option initialization.

        Ensures all relevant numerical values are strictly positive. Negative or zero
        values would lead to invalid computations or undefined financial behavior.

        Args:
            S (float): Spot price.
            K (float): Strike price.
            T (float): Time to maturity.
            sigma (float): Volatility.

        Raises:
            ValueError: If any of the inputs is not strictly positive.
        """

        if any ( x < 0 for x in [S,K,T,sigma]):
            raise ValueError("S, K, T and sigma must be positive")