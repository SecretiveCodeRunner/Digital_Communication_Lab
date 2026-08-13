"""
Digital Communication Laboratory — Experiment 2
Title: Random Variables and Additive White Gaussian Noise (AWGN)

Objectives:
  1. Estimate PDF, CDF, mean, and variance of Uniform and Gaussian random variables.
  2. Relate signal power, noise power, and measured SNR in an AWGN channel.
  3. Analyze sample-size convergence (Law of Large Numbers) and noise autocorrelation.

Author: Ciel (for Apurba Maity)
Date: 2026-08-13
"""

import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

# Set publication style for matplotlib plots
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'grid.color': '#E0E0E0',
    'grid.linestyle': '--',
    'grid.linewidth': 0.7,
})

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'plots')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_random_variables(n_samples=100000, seed=42):
    """
    Generate Uniform and Gaussian random variables.
    
    Parameters:
        n_samples (int): Number of samples to generate.
        seed (int): Seed for reproducibility.
        
    Returns:
        tuple: (unif_samples, gauss_samples)
    """
    rng = np.random.default_rng(seed)
    
    # Uniform RV U[-1, 1]
    a, b = -1.0, 1.0
    unif_samples = rng.uniform(a, b, n_samples)
    
    # Gaussian RV N(0, 1)
    mu, sigma = 0.0, 1.0
    gauss_samples = rng.normal(mu, sigma, n_samples)
    
    return unif_samples, gauss_samples


def compute_empirical_cdf(samples):
    """
    Compute the empirical CDF (ECDF) of a sample vector.
    
    Parameters:
        samples (ndarray): Input sample vector.
        
    Returns:
        tuple: (sorted_samples, ecdf_values)
    """
    sorted_samples = np.sort(samples)
    ecdf_values = np.arange(1, len(samples) + 1) / len(samples)
    return sorted_samples, ecdf_values


def add_awgn(signal, target_snr_db, seed=42):
    """
    Add Additive White Gaussian Noise (AWGN) to a deterministic signal at specified SNR.
    
    Parameters:
        signal (ndarray): Input clean signal.
        target_snr_db (float): Target Signal-to-Noise Ratio in dB.
        seed (int): Random seed for reproducibility.
        
    Returns:
        tuple: (noisy_signal, noise, measured_snr_db, sig_power, noise_power)
    """
    rng = np.random.default_rng(seed)
    sig_power = np.mean(signal ** 2)
    
    # Convert SNR from dB to linear scale
    snr_linear = 10.0 ** (target_snr_db / 10.0)
    
    # Calculate required noise power (variance)
    noise_power_target = sig_power / snr_linear
    noise_std = np.sqrt(noise_power_target)
    
    # Generate Gaussian noise
    noise = rng.normal(0.0, noise_std, size=len(signal))
    noisy_signal = signal + noise
    
    # Empirical measurements
    noise_power_measured = np.mean((noisy_signal - signal) ** 2)
    measured_snr_db = 10.0 * np.log10(sig_power / noise_power_measured)
    
    return noisy_signal, noise, measured_snr_db, sig_power, noise_power_measured


def compute_autocorrelation(x, max_lags=100):
    """
    Compute normalized autocorrelation of a 1D sequence x up to max_lags.
    
    Parameters:
        x (ndarray): 1D input array.
        max_lags (int): Maximum lag count.
        
    Returns:
        tuple: (lags, r_xx)
    """
    x_zero_mean = x - np.mean(x)
    n = len(x)
    autocorr = np.correlate(x_zero_mean, x_zero_mean, mode='full')
    center = len(autocorr) // 2
    lags = np.arange(-max_lags, max_lags + 1)
    r_xx = autocorr[center - max_lags : center + max_lags + 1] / np.var(x) / n
    return lags, r_xx


def run_experiment_2():
    print("=" * 70)
    print(" DIGITAL COMMUNICATION LAB — EXPERIMENT 2 ")
    print(" Random Variables and Additive White Gaussian Noise (AWGN) ")
    print("=" * 70)
    
    N_LARGE = 100000
    unif, gauss = generate_random_variables(n_samples=N_LARGE, seed=42)
    
    # -------------------------------------------------------------------------
    # TASK 1 & 2: Statistical Moments and Normalized Histograms
    # -------------------------------------------------------------------------
    print("\n[Task 1 & 2] Statistical Moments Estimation (N = 100,000):")
    stats_data = [
        {
            "Distribution": "Uniform U[-1, 1]",
            "Theoretical Mean": 0.0,
            "Sample Mean": np.mean(unif),
            "Theoretical Var": (1 - (-1))**2 / 12,  # 0.3333...
            "Sample Var": np.var(unif, ddof=1),
            "Skewness": stats.skew(unif),
            "Kurtosis": stats.kurtosis(unif) # Excess kurtosis
        },
        {
            "Distribution": "Gaussian N(0, 1)",
            "Theoretical Mean": 0.0,
            "Sample Mean": np.mean(gauss),
            "Theoretical Var": 1.0,
            "Sample Var": np.var(gauss, ddof=1),
            "Skewness": stats.skew(gauss),
            "Kurtosis": stats.kurtosis(gauss)
        }
    ]
    df_moments = pd.DataFrame(stats_data)
    print(df_moments.to_string(index=False))
    
    # Plot 1: Histograms vs Theoretical PDFs
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # Uniform Histogram & PDF
    count_u, bins_u, _ = axes[0].hist(unif, bins=60, density=True, alpha=0.6, color='#2B579A', edgecolor='black', label='Empirical Histogram')
    x_u = np.linspace(-1.5, 1.5, 500)
    pdf_u = np.where((x_u >= -1.0) & (x_u <= 1.0), 0.5, 0.0)
    axes[0].plot(x_u, pdf_u, 'r-', lw=2.5, label='Theoretical PDF ($U[-1, 1]$)')
    axes[0].set_title('Uniform Distribution $U[-1, 1]$')
    axes[0].set_xlabel('Value ($x$)')
    axes[0].set_ylabel('Probability Density $f_X(x)$')
    axes[0].grid(True)
    axes[0].legend()
    
    # Gaussian Histogram & PDF
    count_g, bins_g, _ = axes[1].hist(gauss, bins=60, density=True, alpha=0.6, color='#008A00', edgecolor='black', label='Empirical Histogram')
    x_g = np.linspace(-4.0, 4.0, 500)
    pdf_g = stats.norm.pdf(x_g, loc=0.0, scale=1.0)
    axes[1].plot(x_g, pdf_g, 'r-', lw=2.5, label='Theoretical PDF ($\\mathcal{N}(0, 1)$)')
    axes[1].set_title('Gaussian Distribution $\\mathcal{N}(0, 1)$')
    axes[1].set_xlabel('Value ($x$)')
    axes[1].set_ylabel('Probability Density $f_X(x)$')
    axes[1].grid(True)
    axes[1].legend()
    
    plt.tight_layout()
    fig1_path = os.path.join(OUTPUT_DIR, 'exp2_pdf_histograms.png')
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"Saved Plot 1: {fig1_path}")
    
    # -------------------------------------------------------------------------
    # TASK 3: Empirical CDF vs Theoretical CDF
    # -------------------------------------------------------------------------
    print("\n[Task 3] Plotting Empirical and Theoretical CDFs...")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # Uniform ECDF vs CDF
    s_u, ecdf_u = compute_empirical_cdf(unif)
    cdf_u_theory = np.clip((s_u - (-1.0)) / (1.0 - (-1.0)), 0.0, 1.0)
    axes[0].plot(s_u, ecdf_u, color='#2B579A', lw=2, label='Empirical CDF')
    axes[0].plot(s_u, cdf_u_theory, 'r--', lw=2, label='Theoretical CDF')
    axes[0].set_title('Uniform Empirical & Theoretical CDF')
    axes[0].set_xlabel('Value ($x$)')
    axes[0].set_ylabel('Cumulative Probability $F_X(x)$')
    axes[0].grid(True)
    axes[0].legend()
    
    # Gaussian ECDF vs CDF
    s_g, ecdf_g = compute_empirical_cdf(gauss)
    cdf_g_theory = stats.norm.cdf(s_g, loc=0.0, scale=1.0)
    axes[1].plot(s_g, ecdf_g, color='#008A00', lw=2, label='Empirical CDF')
    axes[1].plot(s_g, cdf_g_theory, 'r--', lw=2, label='Theoretical CDF')
    axes[1].set_title('Gaussian Empirical & Theoretical CDF')
    axes[1].set_xlabel('Value ($x$)')
    axes[1].set_ylabel('Cumulative Probability $F_X(x)$')
    axes[1].grid(True)
    axes[1].legend()
    
    plt.tight_layout()
    fig2_path = os.path.join(OUTPUT_DIR, 'exp2_ecdf.png')
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"Saved Plot 2: {fig2_path}")
    
    # -------------------------------------------------------------------------
    # TASK 4: Add AWGN to Sinusoid & Measure SNR
    # -------------------------------------------------------------------------
    print("\n[Task 4] AWGN Channel Simulation on Sinusoidal Signal:")
    fs = 1000  # Sampling frequency 1 kHz
    duration = 1.0  # 1 second
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    f0 = 5.0  # 5 Hz sinusoid
    amplitude = 2.0  # Power = A^2 / 2 = 2.0
    clean_signal = amplitude * np.sin(2 * np.pi * f0 * t)
    
    target_snrs = [-5.0, 0.0, 5.0, 10.0, 20.0]
    snr_results = []
    
    fig, axes = plt.subplots(len(target_snrs), 1, figsize=(12, 10), sharex=True)
    
    for i, snr_target in enumerate(target_snrs):
        noisy_sig, noise, measured_snr, sig_pwr, noise_pwr = add_awgn(clean_signal, snr_target, seed=42+i)
        snr_results.append({
            "Target SNR (dB)": snr_target,
            "Measured SNR (dB)": measured_snr,
            "SNR Error (dB)": measured_snr - snr_target,
            "Signal Power (W)": sig_pwr,
            "Noise Power (W)": noise_pwr
        })
        
        axes[i].plot(t, clean_signal, 'k--', alpha=0.7, lw=1.5, label='Clean Signal ($A=2V$)' if i == 0 else "")
        axes[i].plot(t, noisy_sig, color='#D8000C' if snr_target < 5 else '#005A9E', lw=1.2, label=f'Noisy Signal (SNR={snr_target} dB)')
        axes[i].set_ylabel('Amp (V)')
        axes[i].set_title(f'Target SNR = {snr_target} dB | Measured SNR = {measured_snr:.2f} dB', fontsize=11)
        axes[i].grid(True)
        axes[i].legend(loc='upper right')
        
    axes[-1].set_xlabel('Time (seconds)')
    plt.tight_layout()
    fig3_path = os.path.join(OUTPUT_DIR, 'exp2_clean_vs_noisy_waveforms.png')
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"Saved Plot 3: {fig3_path}")
    
    df_snr = pd.DataFrame(snr_results)
    print(df_snr.to_string(index=False))
    
    # -------------------------------------------------------------------------
    # TASK 5: Mandatory Validation — Sample Size Convergence Sweep
    # -------------------------------------------------------------------------
    print("\n[Task 5 — Mandatory Validation] Sample-Size Convergence Sweep (10^2 to 10^6):")
    sample_sizes = [100, 1000, 10000, 100000, 1000000]
    convergence_data = []
    
    rng = np.random.default_rng(123)
    for N_val in sample_sizes:
        u_samples = rng.uniform(-1.0, 1.0, N_val)
        g_samples = rng.normal(0.0, 1.0, N_val)
        
        u_mean, u_var = np.mean(u_samples), np.var(u_samples, ddof=1)
        g_mean, g_var = np.mean(g_samples), np.var(g_samples, ddof=1)
        
        convergence_data.append({
            "Sample Count (N)": N_val,
            "Gauss Mean": g_mean,
            "Gauss Mean Err": abs(g_mean - 0.0),
            "Gauss Var": g_var,
            "Gauss Var Err": abs(g_var - 1.0),
            "Unif Mean": u_mean,
            "Unif Mean Err": abs(u_mean - 0.0),
            "Unif Var": u_var,
            "Unif Var Err": abs(u_var - (1/3))
        })
        
    df_conv = pd.DataFrame(convergence_data)
    print(df_conv.to_string(index=False))
    
    # -------------------------------------------------------------------------
    # TASK 6: Noise Autocorrelation Function
    # -------------------------------------------------------------------------
    print("\n[Task 6] Estimating Noise Autocorrelation Function...")
    _, noise_sample, _, _, _ = add_awgn(clean_signal, target_snr_db=10.0, seed=99)
    lags, r_nn = compute_autocorrelation(noise_sample, max_lags=50)
    
    plt.figure(figsize=(9, 4.5))
    plt.stem(lags, r_nn, linefmt='b-', markerfmt='bo', basefmt='r-')
    plt.title('Normalized Autocorrelation $R_{nn}[\\tau]$ of AWGN (Target SNR = 10 dB)')
    plt.xlabel('Lag (samples $\\tau$)')
    plt.ylabel('Normalized Autocorrelation')
    plt.grid(True)
    plt.ylim(-0.2, 1.1)
    
    plt.tight_layout()
    fig4_path = os.path.join(OUTPUT_DIR, 'exp2_autocorrelation.png')
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"Saved Plot 4: {fig4_path}")
    
    print("\n" + "=" * 70)
    print(" EXPERIMENT 2 EXECUTION COMPLETE. ALL ARTIFACTS GENERATED SUCCESSFULLY. ")
    print("=" * 70)


if __name__ == '__main__':
    run_experiment_2()
