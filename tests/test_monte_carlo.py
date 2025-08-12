import os, sys
# Add project root to Python path for importing sibling modules
# Required to import from 'models/' directory when running tests from 'tests/' directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(1, project_root)
from models.monte_carlo import MonteCarloOption
from models.black_scholes import BlackScholesOption
import unittest


class TestMonteCarloOption(unittest.TestCase):

    def test_convergence_with_iterations(self):
        """
        Test convergence of Monte Carlo price with increasing number of simulations.
        """
        params = {
            'S': 100,
            'K': 100,
            'T': 1,
            'r': 0.05,
            'sigma': 0.2,
            'option_type': 'call'
        }
       
        bs_option = BlackScholesOption(**params)
        bs_price = bs_option.price()
       
        # Test with different numbers of simulations
        n_sims_list = [1000, 10000, 100000]
        errors = []
       
        for n_sims in n_sims_list:
            mc_option = MonteCarloOption(**params, seed=42)
            mc_price = mc_option.price(n_simulations=n_sims)
            errors.append(abs(bs_price - mc_price))
       
        # Check that the error decreases overall as the number of simulations increases
        self.assertLess(errors[-1], errors[0], "Error should decrease as number of simulations increases.")

        # Check that the error with a large number of simulations is acceptable
        self.assertLess(errors[-1], 0.1, "Error with 100000 simulations should be less than 0.1.")


if __name__ == '__main__':
    unittest.main()




