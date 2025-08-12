import numpy as np
from models.black_scholes import BlackScholesOption
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st


def setup_plot_style() -> None:
    """
    Set up a modern style for matplotlib plots to enhance readability.
    """
    plt.rcParams.update({
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
    })

#@st.cache_data
def create_pnl_plot(option : BlackScholesOption, direction='long'):
    """
    Generate a payoff (PnL) plot of the option over a range of underlying prices.
    
    Args:
        option (BlackScholesOption): The option instance to analyze.
        direction (str): Position direction, either 'long' or 'short'.
    
    Returns:
        matplotlib.figure.Figure: The generated PnL figure.
    """

    setup_plot_style()
    
    # Define the range of underlying prices around the strike price
    spot_range = np.linspace(0.5 * option.K, 1.5 * option.K, 200)

    # Calculate the PnL values across this price range
    pnl = option.pnl_array(spot_range, direction=direction)
    
    # Plot the PnL curve and color regions of profit (green) and loss (red)
    fig, ax = plt.subplots(1,1)
    ax.plot(spot_range, pnl, label=f'PnL {direction} {option.option_type}')
    ax.axhline(0, color='black', linestyle='-', alpha=0.4, linewidth=1)
    ax.fill_between(spot_range, pnl, alpha=0.2, where=(pnl < 0), color='red')
    ax.fill_between(spot_range, pnl, alpha=0.2, where=(pnl >= 0), color='green')

    # Add axis labels, title, legend, and grid for clarity
    ax.set_xlabel('Underlying Price (S)')
    ax.set_ylabel('PnL')
    ax.set_title('Option PnL')
    ax.legend()
    ax.grid(True)
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('white')
    
    return fig

#@st.cache_data
def plot_greeks(option: BlackScholesOption):
    """
    Plot the main option Greeks (Delta, Gamma, Vega, Theta, Rho) across a range of spot prices.
    
    Args:
        option (BlackScholesOption): The option instance to analyze.
    
    Returns:
        matplotlib.figure.Figure: The figure containing subplots of each Greek.
    """

    setup_plot_style()
    
    spot_range = np.linspace(0.5 * option.K, 1.5 * option.K, 100)
    deltas, gammas, vegas, thetas, rhos = [], [], [], [], []
    
    # Loop over spot prices to instantiate option objects and compute Greeks
    for S in spot_range:
        temp_option = BlackScholesOption(S=S, K=option.K, T=option.T, 
                                       sigma=option.sigma, r=option.r, 
                                       option_type=option.option_type)
        deltas.append(temp_option.delta())
        gammas.append(temp_option.gamma())
        vegas.append(temp_option.vega())
        thetas.append(temp_option.theta())
        rhos.append(temp_option.rho())
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Option Sensitivities (Greeks)', fontsize=18, fontweight='bold')
    
    greeks_data = {
        'Delta (Δ)': (deltas, 'Price Sensitivity', colors[0]),
        'Gamma (Γ)': (gammas, 'Delta Sensitivity', colors[1]),
        'Vega (ν)': (vegas, 'Volatility Sensitivity', colors[2]),
        'Theta (Θ)': (thetas, 'Time Decay', colors[3]),
        'Rho (ρ)': (rhos, 'Interest Rate Sensitivity', colors[4])
    }
    
    positions = [(0,0), (0,1), (0,2), (1,0), (1,1)]
    
    for i, (greek, (values, description, color)) in enumerate(greeks_data.items()):
        row, col = positions[i]
        ax = axs[row, col]
        ax.plot(spot_range, values, linewidth=3, color=color, alpha=0.8)
        ax.fill_between(spot_range, values, alpha=0.2, color=color)

        # Highlight the strike price (red dashed line) and current spot price (blue dashed line)
        ax.axvline(option.K, color='red', linestyle='--', alpha=0.6, linewidth=1)
        ax.axvline(option.S, color='blue', linestyle='--', alpha=0.6, linewidth=1)
        ax.axhline(0, color='black', linestyle='-', alpha=0.4, linewidth=1)
        
        # Mark the current Greek value with a prominent dot and annotate it
        current_value = values[np.argmin(np.abs(spot_range - option.S))]
        ax.scatter([option.S], [current_value], color=color, s=100, zorder=5,
                  edgecolors='white', linewidth=2)
        
        ax.set_title(f'{greek}\n{description}', fontweight='bold', pad=10)
        ax.set_xlabel('Spot Price (€)')
        ax.set_ylabel(greek.split('(')[0].strip())
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#FAFAFA')
        
        # Mark the current Greek value with a prominent dot and annotate it
        ax.text(0.02, 0.98, f'Current: {current_value:.4f}', 
               transform=ax.transAxes, fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
               verticalalignment='top')
    
    # Hide the unused subplot
    axs[1, 2].axis('off')
    
    # Display a legend explaining plot symbols
    ax_legend = axs[1, 2]
    ax_legend.text(0.1, 0.9, 'Legend:', fontsize=14, fontweight='bold', transform=ax_legend.transAxes)

    # Strike Price
    ax_legend.plot([0.1, 0.3], [0.75, 0.75], color='red', linestyle='--', alpha=0.6, linewidth=2, transform=ax_legend.transAxes)
    ax_legend.text(0.35, 0.75, 'Strike Price', fontsize=12, transform=ax_legend.transAxes, verticalalignment='center')

    # Current Spot
    ax_legend.plot([0.1, 0.3], [0.6, 0.6], color='blue', linestyle='--', alpha=0.6, linewidth=2, transform=ax_legend.transAxes)
    ax_legend.text(0.35, 0.6, 'Current Spot Price', fontsize=12, transform=ax_legend.transAxes, verticalalignment='center')

    # Current Greek value
    ax_legend.scatter([0.2], [0.45], color='black', s=100, zorder=5, edgecolors='white', linewidth=2, transform=ax_legend.transAxes)
    ax_legend.text(0.35, 0.45, 'Current Greek value', fontsize=12, transform=ax_legend.transAxes, verticalalignment='center')

    
    plt.tight_layout()
    return fig
