import os, sys
# Add project root to Python path for importing sibling modules
# Required to import from 'models/' directory when running tests from 'tests/' directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(1, project_root)
from models.black_scholes import BlackScholesOption
import unittest
import numpy as np



class TestBlackScholesOption(unittest.TestCase):
    """
    Unit tests for the BlackScholesOption class.

    This test suite verifies the correctness of the European option pricing 
    implemented in the Black-Scholes model for both call and put options.

    Tests included:
    - Pricing accuracy against known reference values.
    - Deep in-the-money put option price behavior.
    - Put-call parity validation to ensure model consistency.
    """

    def setUp(self):
        """
        Set up common option parameters for call and put options used across multiple tests.
        """
        self.call_option = BlackScholesOption(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='call')
        self.put_option = BlackScholesOption(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='put')

    def test_black_scholes_call(self):
        """
        Test the call option price against a known value.

        The expected price is approximately 10.45 for the given parameters,
        verified up to 2 decimal places.
        """
        self.assertAlmostEqual(self.call_option.price(), 10.45, places=2)

    def test_black_scholes_put(self):
        """
        Test the put option price against a known value.

        The expected price is approximately 5.57 for the given parameters,
        verified up to 2 decimal places.
        """
        self.assertAlmostEqual(self.put_option.price(), 5.57, places=2)

    def test_deep_in_the_money_put(self):
        """
        Verify that a deep in-the-money put option price is close to its intrinsic value.

        For S=50 and K=100, the put is deep ITM and the price should be greater than 45.
        """
        put = BlackScholesOption(S=50, K=100, T=1, r=0.05, sigma=0.2, option_type='put')
        self.assertGreater(put.price(), 45)
 
    def test_put_call_parity(self):
        """
        Check that the put-call parity relationship holds for European options.

        The parity relationship is:
            C - P = S - K * exp(-r * T)

        This ensures internal consistency of the model.
        """
        call = BlackScholesOption(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='call')
        put = BlackScholesOption(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='put')
       
        call_price = call.price()
        put_price = put.price()
        S = 100
        K = 100
        r = 0.05
        T = 1
       
        parity = abs((call_price - put_price) - (S - K * np.exp(-r * T)))
        self.assertLess(parity, 1e-10, "Put-call parity violated beyond tolerance.")

# python3 -m unittest discover -s tests
if __name__ == '__main__':
    unittest.main()
