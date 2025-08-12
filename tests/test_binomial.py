import os, sys
# Add project root to Python path for importing sibling modules
# Required to import from 'models/' directory when running tests from 'tests/' directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(1, project_root)
from models.binomial import BinomialOption
from models.black_scholes import BlackScholesOption
import unittest


class TestBinomialOption(unittest.TestCase):
      
    def test_convergence_with_iterations(self):
        """
        Ensure binomial model converges to Black-Scholes price as steps increase.
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
    
        # Test with different numbers of steps
        n_steps_list = [10, 100, 500]
        errors = []
    
        for n_steps in n_steps_list:
            bin_option = BinomialOption(**params)
            bin_price = bin_option.price(steps=n_steps)
            errors.append(abs(bs_price - bin_price))
        
        # Check that the error decreases overall as the number of steps increases
        self.assertTrue(all(errors[i] > errors[i+1] for i in range(len(errors)-1)))

if __name__ == '__main__':
    unittest.main()