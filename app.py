import streamlit as st
from models.black_scholes import BlackScholesOption
from models.binomial import BinomialOption
from models.monte_carlo import MonteCarloOption
from plot import create_pnl_plot, plot_greeks


def main() -> None:
    """
    Streamlit dashboard for interactive option pricing analysis.

    Allows users to input parameters for European options and compare prices computed with 
    Black-Scholes, Binomial, and Monte Carlo models.
    Displays key Greeks and plots PnL and Greeks diagrams dynamically.
    """

    # Set page configuration and main title of the dashboard
    st.set_page_config(page_title="Option Pricing App", layout="centered")
    st.title("Option Pricing Dashboard")
    st.divider()

    
    # Sidebar inputs to let user specify option parameters:
    # Spot price, strike price, time to maturity, risk-free rate,
    # volatility, option type (call/put), position direction (long/short),
    # binomial steps and Monte Carlo simulations parameters,
    # plus an option to fix the random seed for reproducibility
    st.sidebar.header("Option Parameters")
    S = st.sidebar.number_input("Spot Price (S)", value=100.0, step=1.0, min_value=0.0)
    K = st.sidebar.number_input("Strike Price (K)", value=100.0, step=1.0, min_value=0.0)
    T = st.sidebar.number_input("Time to Maturity (in years)", value=1.0, step=0.1, min_value=0.0)
    r = st.sidebar.number_input("Risk-free Rate (r)", value=0.05, step=0.01, min_value=-1.0, max_value=1.0)
    sigma = st.sidebar.number_input("Volatility (σ)", value=0.2, step=0.01, min_value=0.0)
    option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
    direction = st.sidebar.selectbox("Position", ["long", "short"])
    binomial_steps = st.sidebar.number_input("Binomial - Number of steps", 1, 1000, 500, 100)
    mc_sims = st.sidebar.number_input("Monte Carlo - Number of steps", 1, 200000, 100000, 25000)
    use_fixed_seed = st.sidebar.checkbox("🔒 Fixer le seed Monte Carlo", value=True)
    if use_fixed_seed:
        seed_value = st.sidebar.number_input("Seed", value=42, min_value=0, step=1)
    
    # Initialize option pricing model instances with user inputs:
    bs_option = BlackScholesOption(S, K, T, r, sigma, option_type)
    bin_option = BinomialOption(S, K, T, r, sigma, option_type)
    if use_fixed_seed:
        mc_option = MonteCarloOption(S, K, T, r, sigma, option_type, seed=seed_value)
    else:
        mc_option = MonteCarloOption(S, K, T, r, sigma, option_type)
    greeks = bs_option.greeks()
    
    # Display option prices side-by-side for the three methods using styled HTML blocks
    col1, col2, col3 = st.columns(3)
    with col1:
            st.markdown(f"""
            <div class="metric-container">
                <h3>Black-Scholes</h3>
                <h2>{bs_option.price():.4f}€</h2>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>Binomial</h3>
            <h2>{bin_option.price(steps=binomial_steps):.4f}€</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h3>Monte Carlo</h3>
            <h2>{mc_option.price(n_simulations=mc_sims):.4f}€</h2>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
        
    col4, col5, col6, col7, col8 = st.columns(5)
    col4.metric("Delta", f"{greeks['delta']:.4f}")
    col5.metric("Gamma", f"{greeks['gamma']:.4f}")
    col6.metric("Vega", f"{greeks['vega']:.4f}")
    col7.metric("Theta", f"{greeks['theta']:.4f}")
    col8.metric("Rho", f"{greeks['rho']:.4f}")

    st.divider()
    
    # Plot and display the PnL diagram for the Black-Scholes option
    st.subheader("PnL Diagram")
    fig = create_pnl_plot(bs_option, direction=direction)
    st.pyplot(fig, use_container_width=True)

    st.divider()


    # Plot and display the Greeks diagrams for the Black-Scholes option
    st.subheader("Greeks Diagram")
    fig = plot_greeks(bs_option)
    st.pyplot(fig, use_container_width=True)

if __name__ == '__main__':
     main()