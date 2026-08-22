"""
Digital Communication Laboratory — Experiment 3
Title: Sampling, Aliasing and Sinc Reconstruction

Objectives:
  1. Verify the Nyquist-Shannon Sampling Theorem.
  2. Implement ideal Whittaker-Shannon sinc interpolation.
  3. Demonstrate aliasing phenomena in time and frequency domains under undersampling.
  4. Perform theoretical vs empirical validation of aliased spectral components.

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

# Signal parameters
F1 = 100.0   # Hz
F2 = 300.0   # Hz
F_MAX = F2   # 300 Hz
F_NYQUIST = 2.0 * F_MAX  # 600 Hz


def continuous_signal(t):
    """
    Two-tone continuous signal x(t) = sin(2*pi*f1*t) + 0.5*sin(2*pi*f2*t)
    """
    return np.sin(2.0 * np.pi * F1 * t) + 0.5 * np.sin(2.0 * np.pi * F2 * t)


def sinc_reconstruction(sample_times, sample_values, t_fine, fs):
    """
    Whittaker-Shannon Sinc Interpolation Formula:
    x_hat(t) = sum_n x[n] * sinc(fs * (t - n*Ts))
    Note: np.sinc(x) computes sin(pi*x) / (pi*x)
    """
    dt_matrix = t_fine[None, :] - sample_times[:, None]
    sinc_matrix = np.sinc(fs * dt_matrix)
    x_hat = np.dot(sample_values, sinc_matrix)
    return x_hat


def calculate_spectrum(signal, fs_fine):
    """
    Compute single-sided magnitude spectrum using Real FFT.
    """
    n = len(signal)
    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs_fine)
    magnitude = (2.0 / n) * np.abs(fft_vals)
    return freqs, magnitude


def run_experiment_3():
    print("=" * 70)
    print(" DIGITAL COMMUNICATION LAB — EXPERIMENT 3 ")
    print(" Sampling, Aliasing and Sinc Reconstruction ")
    print("=" * 70)
    
    print(f"\nSignal Components: f1 = {F1} Hz, f2 = {F2} Hz")
    print(f"Maximum Frequency (f_max) = {F_MAX} Hz")
    print(f"Nyquist Rate (2 * f_max)   = {F_NYQUIST} Hz")
    
    # Time vector for continuous/reference signal
    duration = 0.05  # 50 ms (0 to 50 ms)
    fs_fine = 20000.0  # 20 kHz plotting resolution
    t_fine = np.linspace(0, duration, int(fs_fine * duration), endpoint=False)
    x_continuous = continuous_signal(t_fine)
    
    # Sampling rates to evaluate
    sampling_cases = [
        {"name": "Oversampled", "fs": 1800.0, "ratio": "3.0x Nyquist", "color": "#008A00"},
        {"name": "Critically Sampled", "fs": 600.0, "ratio": "1.0x Nyquist", "color": "#2B579A"},
        {"name": "Undersampled", "fs": 400.0, "ratio": "0.67x Nyquist", "color": "#D8000C"}
    ]
    
    results = []
    reconstructions = {}
    sampled_data = {}
    
    # -------------------------------------------------------------------------
    # TASK 7 & 8: Sampling and Sinc Reconstruction for All 3 Cases
    # -------------------------------------------------------------------------
    for case in sampling_cases:
        fs = case["fs"]
        ts = 1.0 / fs
        
        # Extend sample window slightly (-5*Ts to duration + 5*Ts) to eliminate sinc truncation edge effects
        pad_samples = 20
        n_start = -pad_samples
        n_end = int(np.ceil(duration * fs)) + pad_samples
        n_indices = np.arange(n_start, n_end)
        
        t_samples_extended = n_indices * ts
        x_samples_extended = continuous_signal(t_samples_extended)
        
        # Discrete samples within plotting range
        mask_in_range = (t_samples_extended >= 0) & (t_samples_extended <= duration)
        t_samples_range = t_samples_extended[mask_in_range]
        x_samples_range = x_samples_extended[mask_in_range]
        
        # Perform sinc interpolation using extended sample sequence
        x_reconstructed = sinc_reconstruction(t_samples_extended, x_samples_extended, t_fine, fs)
        
        # Calculate reconstruction error
        error = x_continuous - x_reconstructed
        mse = np.mean(error ** 2)
        rmse = np.sqrt(mse)
        max_error = np.max(np.abs(error))
        
        sampled_data[case["name"]] = (t_samples_range, x_samples_range)
        reconstructions[case["name"]] = (x_reconstructed, error)
        
        # Calculate manual expected aliased frequency for undersampled case
        if fs < F_NYQUIST:
            # f_alias = |f2 - k*fs|
            k = round(F2 / fs)
            f2_alias = abs(F2 - k * fs)
        else:
            f2_alias = F2
            
        results.append({
            "Sampling Case": case["name"],
            "Sampling Rate fs (Hz)": fs,
            "Ratio (fs / f_Nyquist)": case["ratio"],
            "Display Samples": len(t_samples_range),
            "MSE": mse,
            "RMSE": rmse,
            "Max Abs Error": max_error,
            "Expected f2 Alias (Hz)": f2_alias
        })
        
    df_results = pd.DataFrame(results)
    print("\n[Tasks 7 & 8] Sampling & Sinc Reconstruction Summary:")
    print(df_results.to_string(index=False))
    
    # -------------------------------------------------------------------------
    # PLOT 1: Reference vs Sampled Discrete Stems
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    fig.suptitle('Figure 1: Reference Continuous Signal vs. Sampled Discrete Stems', fontsize=14, fontweight='bold', y=0.99)
    for i, case in enumerate(sampling_cases):
        name = case["name"]
        t_samp, x_samp = sampled_data[name]
        
        axes[i].plot(t_fine * 1000, x_continuous, 'k--', alpha=0.5, label='Reference Continuous $x(t)$')
        markerline, stemlines, baseline = axes[i].stem(
            t_samp * 1000, x_samp, 
            label=f'Sampled $x[n]$ ($f_s = {case["fs"]:.0f}$ Hz)'
        )
        plt.setp(stemlines, color=case["color"], linewidth=1.5)
        plt.setp(markerline, color=case["color"], markersize=6)
        plt.setp(baseline, color='black', linewidth=0.8)
        
        axes[i].set_title(f'{name} Case: $f_s = {case["fs"]:.0f}$ Hz ({case["ratio"]})')
        axes[i].set_ylabel('Amplitude (V)')
        axes[i].grid(True)
        axes[i].legend(loc='upper right')
        
    axes[-1].set_xlabel('Time (ms)')
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    fig1_path = os.path.join(OUTPUT_DIR, 'exp3_sampled_signals.png')
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"\nSaved Plot 1: {fig1_path}")
    
    # -------------------------------------------------------------------------
    # PLOT 2: Continuous Reference vs Sinc Reconstructed Signals
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    fig.suptitle('Figure 2: Original Reference vs. Sinc Reconstructed Waveforms', fontsize=14, fontweight='bold', y=0.99)
    for i, case in enumerate(sampling_cases):
        name = case["name"]
        x_rec, _ = reconstructions[name]
        
        axes[i].plot(t_fine * 1000, x_continuous, 'k-', lw=2.2, alpha=0.7, label='Reference Original $x(t)$')
        axes[i].plot(t_fine * 1000, x_rec, color=case["color"], linestyle='--', lw=2.0, 
                     label=f'Sinc Reconstructed $\\hat{{x}}(t)$ ($f_s = {case["fs"]:.0f}$ Hz)')
        axes[i].set_title(f'{name} Reconstructed Waveform ($f_s = {case["fs"]:.0f}$ Hz)')
        axes[i].set_ylabel('Amplitude (V)')
        axes[i].grid(True)
        axes[i].legend(loc='upper right')
        
    axes[-1].set_xlabel('Time (ms)')
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    fig2_path = os.path.join(OUTPUT_DIR, 'exp3_reconstructed_waveforms.png')
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"Saved Plot 2: {fig2_path}")
    
    # -------------------------------------------------------------------------
    # PLOT 3: Magnitude Spectra (Original vs Reconstructed FFTs)
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    fig.suptitle('Figure 3: Single-Sided Magnitude Spectra (Original vs. Reconstructed FFTs)', fontsize=14, fontweight='bold', y=0.99)
    
    # Original spectrum
    freqs_ref, mag_ref = calculate_spectrum(x_continuous, fs_fine)
    axes[0].plot(freqs_ref, mag_ref, 'black', lw=2.0, label='Original Spectrum $X(f)$')
    axes[0].axvline(F1, color='blue', linestyle=':', label=f'$f_1 = {F1}$ Hz')
    axes[0].axvline(F2, color='red', linestyle=':', label=f'$f_2 = {F2}$ Hz')
    axes[0].set_title('Continuous Signal Spectrum (Reference)')
    axes[0].set_ylabel('Magnitude')
    axes[0].set_xlim(0, 800)
    axes[0].grid(True)
    axes[0].legend(loc='upper right')
    
    for i, case in enumerate(sampling_cases):
        name = case["name"]
        x_rec, _ = reconstructions[name]
        freqs_rec, mag_rec = calculate_spectrum(x_rec, fs_fine)
        
        axes[i+1].plot(freqs_rec, mag_rec, color=case["color"], lw=1.8, 
                       label=f'Reconstructed Spectrum $\\hat{{X}}(f)$ ($f_s = {case["fs"]:.0f}$ Hz)')
        axes[i+1].axvline(F1, color='blue', linestyle=':', alpha=0.6)
        axes[i+1].axvline(F2, color='red', linestyle=':', alpha=0.6)
        if case["fs"] < F_NYQUIST:
            axes[i+1].axvline(100.0, color='purple', linestyle='--', lw=2, label='Aliased Peak ($f_{2,alias} = 100$ Hz)')
        axes[i+1].set_title(f'{name} Reconstructed Spectrum ($f_s = {case["fs"]:.0f}$ Hz)')
        axes[i+1].set_ylabel('Magnitude')
        axes[i+1].grid(True)
        axes[i+1].legend(loc='upper right')
        
    axes[-1].set_xlabel('Frequency (Hz)')
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    fig3_path = os.path.join(OUTPUT_DIR, 'exp3_magnitude_spectra.png')
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"Saved Plot 3: {fig3_path}")
    
    # -------------------------------------------------------------------------
    # PLOT 4: Time-Domain Reconstruction Error Waveforms
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    fig.suptitle('Figure 4: Time-Domain Reconstruction Error Waveforms', fontsize=14, fontweight='bold', y=0.99)
    for i, case in enumerate(sampling_cases):
        name = case["name"]
        _, error = reconstructions[name]
        mse_val = df_results.loc[i, "MSE"]
        
        axes[i].plot(t_fine * 1000, error, color=case["color"], lw=1.5, 
                     label=f'Error $e(t) = x(t) - \\hat{{x}}(t)$ (MSE = {mse_val:.2e})')
        axes[i].set_title(f'{name} Reconstruction Error ($f_s = {case["fs"]:.0f}$ Hz)')
        axes[i].set_ylabel('Error (V)')
        axes[i].grid(True)
        axes[i].legend(loc='upper right')
        
    axes[-1].set_xlabel('Time (ms)')
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    fig4_path = os.path.join(OUTPUT_DIR, 'exp3_reconstruction_error.png')
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"Saved Plot 4: {fig4_path}")
    
    print("\n" + "=" * 70)
    print(" EXPERIMENT 3 EXECUTION COMPLETE. ALL ARTIFACTS GENERATED SUCCESSFULLY. ")
    print("=" * 70)


if __name__ == '__main__':
    run_experiment_3()
