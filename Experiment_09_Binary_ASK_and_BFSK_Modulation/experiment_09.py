#!/usr/bin/env python3
"""
Experiment 09: Binary Amplitude Shift Keying (BASK) & Binary Frequency Shift Keying (BFSK)
Software-Based Digital Communication Laboratory (EC592 / EC593)
Department of Electronics & Communication Engineering, Cooch Behar Government Engineering College
Student Name: Apurba Maity | Roll No: 34900324001
"""

import os
import sys
import numpy as np
from scipy import signal, special
import matplotlib.pyplot as plt

# Output directory for publication plots
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(SCRIPT_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# Set global Matplotlib styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#1e293b'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['grid.color'] = '#cbd5e1'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.65
plt.rcParams['figure.dpi'] = 300

# Color Palette
CLR_PRIMARY = '#0f2b48'    # Deep Navy
CLR_SEC = '#0e7490'        # Dark Cyan
CLR_ACCENT = '#b91c1c'     # Crimson Red
CLR_GREEN = '#15803d'      # Forest Green
CLR_AMBER = '#b45309'      # Amber
CLR_PURPLE = '#6b21a8'     # Deep Violet
CLR_SLATE = '#334155'      # Slate 700

# Simulation Parameters
RB = 1000.0             # Bit rate: 1000 bps
TB = 1.0 / RB           # Bit duration: 1.0 ms
FS = 100000.0           # Sampling rate: 100 kHz (100 samples per bit)
DT = 1.0 / FS
SAMPLES_PER_BIT = int(FS * TB)

# Carrier Frequencies
FC_BASK = 4000.0        # BASK carrier: 4 kHz (4 cycles per bit)
F1_BFSK = 3000.0        # BFSK Space '0': 3 kHz (3 cycles per bit)
F2_BFSK = 5000.0        # BFSK Mark '1': 5 kHz (5 cycles per bit)
# Delta f = 2000 Hz = 2 * Rb (Orthogonal for both coherent and non-coherent detection)

print("=" * 75)
print("EXPERIMENT 09: BINARY ASK & BFSK MODULATION AND DEMODULATION")
print("Comprehensive Physical Layer Simulation Suite | Apurba Maity (34900324001)")
print("=" * 75)

# ---------------------------------------------------------------------------
# FIGURE 1: TIME-DOMAIN WAVEFORMS (BASK & BFSK)
# ---------------------------------------------------------------------------
def generate_fig1_waveforms():
    print("[1/7] Generating Figure 1: Time-Domain Waveforms (BASK vs BFSK)...")
    bits = np.array([1, 0, 1, 1, 0, 0, 1, 0])
    n_bits = len(bits)
    t = np.linspace(0, n_bits * TB, n_bits * SAMPLES_PER_BIT, endpoint=False)
    
    # Baseband bit waveform (NRZ unipolar)
    baseband = np.repeat(bits, SAMPLES_PER_BIT)
    
    # Carrier signals
    carrier_bask = np.cos(2 * np.pi * FC_BASK * t)
    carrier_f1 = np.cos(2 * np.pi * F1_BFSK * t)
    carrier_f2 = np.cos(2 * np.pi * F2_BFSK * t)
    
    # BASK (OOK): s_BASK(t) = m(t) * Ac * cos(2 pi fc t)
    Ac = np.sqrt(2.0 / TB)  # Normalization for unit average energy
    bask_sig = baseband * Ac * carrier_bask
    
    # BFSK (Orthogonal, continuous phase): s_BFSK(t) = cos(2 pi f_i t)
    bfsk_sig = np.zeros_like(t)
    for i, b in enumerate(bits):
        idx = slice(i * SAMPLES_PER_BIT, (i + 1) * SAMPLES_PER_BIT)
        t_sub = t[idx]
        freq = F2_BFSK if b == 1 else F1_BFSK
        bfsk_sig[idx] = Ac * np.cos(2 * np.pi * freq * t_sub)
        
    fig, axes = plt.subplots(4, 1, figsize=(12, 9), sharex=True)
    t_ms = t * 1000.0
    
    # (a) Bitstream
    axes[0].step(t_ms, baseband, where='post', color=CLR_PRIMARY, lw=2.2, label='Binary Message m(t)')
    axes[0].set_ylabel('Data m(t)\n[V]', fontweight='bold', color=CLR_PRIMARY)
    axes[0].set_ylim(-0.2, 1.3)
    axes[0].grid(True)
    for i, b in enumerate(bits):
        axes[0].text((i + 0.5) * TB * 1000, 0.5, f"b={b}", ha='center', va='center',
                     fontsize=11, fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', facecolor='#e0f2fe', edgecolor=CLR_SEC))
    axes[0].set_title('(a) Transmitted Binary Bitstream m(t) [Bit Rate Rb = 1 kbps, Tb = 1.0 ms]', fontsize=11, fontweight='bold', loc='left')
    
    # (b) Carriers
    axes[1].plot(t_ms, carrier_f2, color=CLR_SEC, lw=1.2, alpha=0.8, label=f'f2 (Mark "1") = {int(F2_BFSK/1000)} kHz')
    axes[1].plot(t_ms, carrier_f1, color=CLR_AMBER, lw=1.2, alpha=0.8, ls='--', label=f'f1 (Space "0") = {int(F1_BFSK/1000)} kHz')
    axes[1].set_ylabel('Carriers\n[V]', fontweight='bold')
    axes[1].legend(loc='upper right', framealpha=0.9)
    axes[1].grid(True)
    axes[1].set_title('(b) Orthogonal Carrier Frequencies (f1 = 3 kHz, f2 = 5 kHz, Δf = 2 kHz = 2 Rb)', fontsize=11, fontweight='bold', loc='left')
    
    # (c) BASK Modulated Waveform
    axes[2].plot(t_ms, bask_sig, color=CLR_ACCENT, lw=1.6, label='BASK (On-Off Keying)')
    axes[2].set_ylabel('BASK s(t)\n[V]', fontweight='bold', color=CLR_ACCENT)
    axes[2].grid(True)
    axes[2].legend(loc='upper right', framealpha=0.9)
    axes[2].set_title('(c) Binary Amplitude Shift Keying (BASK / OOK): Envelope = Ac for "1", Envelope = 0 for "0"', fontsize=11, fontweight='bold', loc='left')
    
    # (d) BFSK Modulated Waveform
    axes[3].plot(t_ms, bfsk_sig, color=CLR_GREEN, lw=1.6, label='BFSK Waveform')
    axes[3].set_ylabel('BFSK s(t)\n[V]', fontweight='bold', color=CLR_GREEN)
    axes[3].set_xlabel('Time t [milliseconds]', fontweight='bold', fontsize=11)
    axes[3].grid(True)
    axes[3].legend(loc='upper right', framealpha=0.9)
    axes[3].set_title('(d) Binary Frequency Shift Keying (BFSK): Instantaneous Frequency f2=5 kHz for "1", f1=3 kHz for "0"', fontsize=11, fontweight='bold', loc='left')
    
    # Vertical gridlines per bit boundary
    for ax in axes:
        for i in range(n_bits + 1):
            ax.axvline(i * TB * 1000, color='#94a3b8', linestyle=':', lw=1.0)
            
    fig.suptitle('Figure 1: Time-Domain Signaling Waveforms for Binary ASK and BFSK Transceivers',
                 fontsize=14, fontweight='bold', color=CLR_PRIMARY, y=0.99)
    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, "fig1_bask_bfsk_time_domain_waveforms.png")
    plt.savefig(out_path)
    plt.close()
    print(f"  -> Saved: {out_path}")

# ---------------------------------------------------------------------------
# FIGURE 2: SIGNAL SPACE AND CONSTELLATION GEOMETRY
# ---------------------------------------------------------------------------
def generate_fig2_constellations():
    print("[2/7] Generating Figure 2: Signal Space & Constellation Geometry...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.8))
    
    # (a) BASK 1D Signal Space
    Eb = 1.0
    s0_bask = 0.0
    s1_bask = np.sqrt(2 * Eb)  # For OOK with average Eb, peak energy Ep = 2 Eb
    gamma_opt = s1_bask / 2.0  # Optimal decision boundary
    
    ax1.axhline(0, color='#64748b', lw=1.5)
    ax1.axvline(gamma_opt, color=CLR_ACCENT, lw=2.0, ls='--', label=r'Optimum Threshold $\gamma = \sqrt{E_b/2}$')
    
    # Plot Conditional Gaussian Distributions at SNR = 8 dB
    sigma = np.sqrt(0.12)
    r_axis = np.linspace(-0.8, 2.2, 500)
    pdf0 = (1.0 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * ((r_axis - s0_bask) / sigma)**2)
    pdf1 = (1.0 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * ((r_axis - s1_bask) / sigma)**2)
    
    ax1.plot(r_axis, pdf0 * 0.4, color=CLR_SEC, lw=1.8, label=r'$p(r|s_0)$ (Bit 0)')
    ax1.plot(r_axis, pdf1 * 0.4, color=CLR_GREEN, lw=1.8, label=r'$p(r|s_1)$ (Bit 1)')
    
    # Shaded error regions
    ax1.fill_between(r_axis[r_axis >= gamma_opt], 0, pdf0[r_axis >= gamma_opt] * 0.4, color=CLR_SEC, alpha=0.3, label='False Alarm $P(e|0)$')
    ax1.fill_between(r_axis[r_axis < gamma_opt], 0, pdf1[r_axis < gamma_opt] * 0.4, color=CLR_GREEN, alpha=0.3, label='Missed Detection $P(e|1)$')
    
    # Points
    ax1.scatter([s0_bask], [0], color=CLR_SEC, s=160, zorder=5, edgecolors='k', lw=1.5)
    ax1.scatter([s1_bask], [0], color=CLR_GREEN, s=160, zorder=5, edgecolors='k', lw=1.5)
    ax1.text(s0_bask, -0.15, r'$s_0 = 0$', ha='center', fontsize=12, fontweight='bold', color=CLR_SEC)
    ax1.text(s1_bask, -0.15, r'$s_1 = \sqrt{2E_b}$', ha='center', fontsize=12, fontweight='bold', color=CLR_GREEN)
    
    ax1.set_xlabel(r'Basis Function $\phi_1(t) = \sqrt{\frac{2}{T_b}}\cos(2\pi f_c t)$', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Probability Density & Constellation Plane', fontweight='bold', fontsize=11)
    ax1.set_title(r'(a) BASK 1-Dimensional Signal Space ($N = 1$)', fontsize=12, fontweight='bold', loc='left')
    ax1.set_xlim(-0.8, 2.2)
    ax1.set_ylim(-0.25, 0.9)
    ax1.legend(loc='upper right', fontsize=9.5)
    ax1.grid(True)
    
    # (b) BFSK 2D Orthogonal Signal Space
    s0_bfsk = np.array([np.sqrt(Eb), 0.0])
    s1_bfsk = np.array([0.0, np.sqrt(Eb)])
    
    ax2.axhline(0, color='#64748b', lw=1.2)
    ax2.axvline(0, color='#64748b', lw=1.2)
    
    # Decision boundary line r2 = r1
    x_bnd = np.linspace(-0.5, 1.8, 100)
    ax2.plot(x_bnd, x_bnd, color=CLR_ACCENT, lw=2.0, ls='--', label=r'Decision Boundary: $r_2 = r_1$ ($y_2 - y_1 = 0$)')
    
    # Shaded Decision Regions
    ax2.fill_between(x_bnd, x_bnd, 2.0, color='#f0fdf4', alpha=0.5, label='Region $Z_1$ (Decide Bit 1)')
    ax2.fill_between(x_bnd, -0.5, x_bnd, color='#eff6ff', alpha=0.5, label='Region $Z_0$ (Decide Bit 0)')
    
    # Constellation points
    ax2.scatter([s0_bfsk[0]], [s0_bfsk[1]], color=CLR_AMBER, s=180, zorder=5, edgecolors='k', lw=1.5)
    ax2.scatter([s1_bfsk[0]], [s1_bfsk[1]], color=CLR_GREEN, s=180, zorder=5, edgecolors='k', lw=1.5)
    
    # Euclidean distance line
    ax2.plot([s0_bfsk[0], s1_bfsk[0]], [s0_bfsk[1], s1_bfsk[1]], color=CLR_PURPLE, lw=2.2, ls=':')
    ax2.text(0.55 * np.sqrt(Eb), 0.55 * np.sqrt(Eb), r'$d = \sqrt{2E_b}$', color=CLR_PURPLE, fontsize=12, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=CLR_PURPLE))
    
    # Noise hypersphere circles around points
    circle0 = plt.Circle((s0_bfsk[0], s0_bfsk[1]), 0.35, color=CLR_AMBER, fill=False, lw=1.5, ls='--')
    circle1 = plt.Circle((s1_bfsk[0], s1_bfsk[1]), 0.35, color=CLR_GREEN, fill=False, lw=1.5, ls='--')
    ax2.add_patch(circle0)
    ax2.add_patch(circle1)
    
    ax2.text(s0_bfsk[0] + 0.08, s0_bfsk[1] - 0.15, r'$\mathbf{s}_0 = [\sqrt{E_b}, 0]^T$', fontsize=11, fontweight='bold', color=CLR_AMBER)
    ax2.text(s1_bfsk[0] - 0.45, s1_bfsk[1] + 0.08, r'$\mathbf{s}_1 = [0, \sqrt{E_b}]^T$', fontsize=11, fontweight='bold', color=CLR_GREEN)
    
    ax2.set_xlabel(r'Basis $\phi_1(t) = \sqrt{\frac{2}{T_b}}\cos(2\pi f_1 t)$ (Space Channel)', fontweight='bold', fontsize=11)
    ax2.set_ylabel(r'Basis $\phi_2(t) = \sqrt{\frac{2}{T_b}}\cos(2\pi f_2 t)$ (Mark Channel)', fontweight='bold', fontsize=11)
    ax2.set_title(r'(b) BFSK 2-Dimensional Orthogonal Signal Space ($N = 2$)', fontsize=12, fontweight='bold', loc='left')
    ax2.set_xlim(-0.5, 1.6)
    ax2.set_ylim(-0.5, 1.6)
    ax2.legend(loc='lower left', fontsize=9.5)
    ax2.grid(True)
    
    fig.suptitle('Figure 2: Geometric Signal Space Representations & Optimum Decision Boundaries',
                 fontsize=14, fontweight='bold', color=CLR_PRIMARY)
    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, "fig2_signal_space_and_constellation.png")
    plt.savefig(out_path)
    plt.close()
    print(f"  -> Saved: {out_path}")

# ---------------------------------------------------------------------------
# FIGURE 3: COHERENT VS NON-COHERENT DEMODULATION PIPELINE
# ---------------------------------------------------------------------------
def generate_fig3_demod_pipeline():
    print("[3/7] Generating Figure 3: Demodulation Processing Pipelines...")
    bits = np.array([1, 0, 1, 0])
    n_bits = len(bits)
    t = np.linspace(0, n_bits * TB, n_bits * SAMPLES_PER_BIT, endpoint=False)
    t_ms = t * 1000.0
    
    # Generate waveforms with moderate noise (SNR = 10 dB)
    np.random.seed(42)
    Ac = np.sqrt(2.0 / TB)
    baseband = np.repeat(bits, SAMPLES_PER_BIT)
    
    # 1. BASK received signal
    bask_clean = baseband * Ac * np.cos(2 * np.pi * FC_BASK * t)
    noise_sigma = 0.25 * Ac
    r_bask = bask_clean + np.random.normal(0, noise_sigma, len(t))
    
    # Coherent BASK: Multiply by local carrier and integrate over each bit
    bask_product = r_bask * np.cos(2 * np.pi * FC_BASK * t)
    bask_correlator = np.zeros_like(t)
    for i in range(n_bits):
        idx = slice(i * SAMPLES_PER_BIT, (i + 1) * SAMPLES_PER_BIT)
        bask_correlator[idx] = np.cumsum(bask_product[idx]) * (DT / TB)
        
    # Non-coherent BASK: Envelope detector (Full-wave rectify + Butterworth LPF)
    rectified_bask = np.abs(r_bask)
    b_lpf, a_lpf = signal.butter(4, 2 * 1.5 * RB / FS, btype='low')
    envelope_bask = signal.filtfilt(b_lpf, a_lpf, rectified_bask)
    
    # 2. BFSK received signal
    bfsk_clean = np.zeros_like(t)
    for i, b in enumerate(bits):
        idx = slice(i * SAMPLES_PER_BIT, (i + 1) * SAMPLES_PER_BIT)
        f_active = F2_BFSK if b == 1 else F1_BFSK
        bfsk_clean[idx] = Ac * np.cos(2 * np.pi * f_active * t[idx])
    r_bfsk = bfsk_clean + np.random.normal(0, noise_sigma, len(t))
    
    # Coherent BFSK: Dual correlators
    bfsk_prod1 = r_bfsk * np.cos(2 * np.pi * F1_BFSK * t)  # Space branch
    bfsk_prod2 = r_bfsk * np.cos(2 * np.pi * F2_BFSK * t)  # Mark branch
    bfsk_corr1 = np.zeros_like(t)
    bfsk_corr2 = np.zeros_like(t)
    for i in range(n_bits):
        idx = slice(i * SAMPLES_PER_BIT, (i + 1) * SAMPLES_PER_BIT)
        bfsk_corr1[idx] = np.cumsum(bfsk_prod1[idx]) * (DT / TB)
        bfsk_corr2[idx] = np.cumsum(bfsk_prod2[idx]) * (DT / TB)
        
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    
    # Panel (a): Coherent BASK Correlator Trajectory
    axes[0].plot(t_ms, bask_product, color='#94a3b8', lw=0.8, alpha=0.6, label='Product: r(t) * cos(2π fc t)')
    axes[0].plot(t_ms, bask_correlator, color=CLR_PRIMARY, lw=2.0, label='Integrator State y(t)')
    axes[0].axhline(0.25 * Ac, color=CLR_ACCENT, ls='--', lw=1.5, label='Optimum Threshold γ')
    # Mark sampling instants
    for i in range(n_bits):
        samp_t = (i + 1) * TB * 1000 - 0.01
        samp_val = bask_correlator[(i + 1) * SAMPLES_PER_BIT - 1]
        axes[0].plot(samp_t, samp_val, 'ro', markersize=8)
        axes[0].text(samp_t - 0.3, samp_val + 0.15 * Ac, f'Sample: {samp_val:.2f}V\nDecide {1 if samp_val > 0.25*Ac else 0}',
                     fontsize=8.5, fontweight='bold', color=CLR_PRIMARY)
    axes[0].set_ylabel('Amplitude [V]', fontweight='bold')
    axes[0].set_title('(a) Coherent BASK Correlator Receiver: Product Demodulator & Integrate-and-Dump Sampler', fontsize=11, fontweight='bold', loc='left')
    axes[0].legend(loc='upper right', fontsize=8.5)
    axes[0].grid(True)
    
    # Panel (b): Non-Coherent BASK Envelope Detector
    axes[1].plot(t_ms, r_bask, color='#cbd5e1', lw=0.7, label='Received Noisy Signal r(t)')
    axes[1].plot(t_ms, envelope_bask, color=CLR_ACCENT, lw=2.2, label='Lowpass Envelope Trajectory R(t)')
    axes[1].axhline(0.35 * Ac, color=CLR_AMBER, ls='--', lw=1.5, label='Envelope Threshold γ_env')
    axes[1].set_ylabel('Amplitude [V]', fontweight='bold')
    axes[1].set_title('(b) Non-Coherent BASK Envelope Receiver: Rectification, Lowpass Filtering & Slicing (No Carrier Sync Needed)', fontsize=11, fontweight='bold', loc='left')
    axes[1].legend(loc='upper right', fontsize=8.5)
    axes[1].grid(True)
    
    # Panel (c): Coherent BFSK Dual-Correlator Output
    axes[2].plot(t_ms, bfsk_corr2, color=CLR_GREEN, lw=2.0, label='Mark Correlator y2(t) (5 kHz)')
    axes[2].plot(t_ms, bfsk_corr1, color=CLR_AMBER, lw=2.0, label='Space Correlator y1(t) (3 kHz)')
    axes[2].set_ylabel('Correlator [V]', fontweight='bold')
    axes[2].set_title('(c) Coherent BFSK Dual Matched Filter Branches: Output Difference y2(Tb) - y1(Tb) > 0 => Decide 1', fontsize=11, fontweight='bold', loc='left')
    axes[2].legend(loc='upper right', fontsize=8.5)
    axes[2].grid(True)
    
    # Panel (d): Difference Metric y2(t) - y1(t)
    diff_metric = bfsk_corr2 - bfsk_corr1
    axes[3].plot(t_ms, diff_metric, color=CLR_PURPLE, lw=2.2, label='Decision Variable: d(t) = y2(t) - y1(t)')
    axes[3].axhline(0, color='k', ls='--', lw=1.2, label='Zero Threshold')
    for i in range(n_bits):
        samp_t = (i + 1) * TB * 1000 - 0.01
        d_val = diff_metric[(i + 1) * SAMPLES_PER_BIT - 1]
        axes[3].plot(samp_t, d_val, 's', markersize=8, color=CLR_PURPLE)
        decision = 1 if d_val > 0 else 0
        axes[3].text(samp_t - 0.35, d_val + (0.15*Ac if d_val > 0 else -0.25*Ac),
                     f'd={d_val:.2f}\nBit {decision}', fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#f5f3ff', edgecolor=CLR_PURPLE))
    axes[3].set_ylabel('Metric d(t) [V]', fontweight='bold')
    axes[3].set_xlabel('Time t [milliseconds]', fontweight='bold', fontsize=11)
    axes[3].set_title('(d) BFSK Optimal Decision Statistic d(Tb): Perfect Symbol Recovery Across Alternating Frequencies', fontsize=11, fontweight='bold', loc='left')
    axes[3].legend(loc='upper right', fontsize=8.5)
    axes[3].grid(True)
    
    for ax in axes:
        for i in range(n_bits + 1):
            ax.axvline(i * TB * 1000, color='#94a3b8', linestyle=':', lw=1.0)
            
    fig.suptitle('Figure 3: Synchronous and Asynchronous Demodulation Architectures for BASK and BFSK',
                 fontsize=14, fontweight='bold', color=CLR_PRIMARY, y=0.99)
    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, "fig3_coherent_vs_noncoherent_demod_pipeline.png")
    plt.savefig(out_path)
    plt.close()
    print(f"  -> Saved: {out_path}")

# ---------------------------------------------------------------------------
# FIGURE 4: BFSK ORTHOGONALITY VS FREQUENCY SEPARATION
# ---------------------------------------------------------------------------
def generate_fig4_orthogonality():
    print("[4/7] Generating Figure 4: BFSK Orthogonality Analysis...")
    # Normalized frequency separation Δf * Tb in [0, 3]
    delta_f_norm = np.linspace(0.01, 3.0, 1000)
    
    # 1. Coherent Orthogonality (Zero phase offset):
    # rho_coh = sinc(2 * Δf * Tb) = sin(2 pi Δf Tb) / (2 pi Δf Tb)
    rho_coherent = np.sinc(2 * delta_f_norm)
    
    # 2. Non-Coherent / Arbitrary Phase Orthogonality:
    # Envelope of worst-case correlation: |rho(Δtheta)| <= |sinc(Δf Tb)|
    # Orthogonality for ANY phase requires Δf * Tb = 1, 2, 3 ...
    rho_arbitrary_phase = np.abs(np.sinc(delta_f_norm))
    
    fig, ax = plt.subplots(figsize=(11, 6))
    
    ax.plot(delta_f_norm, rho_coherent, color=CLR_PRIMARY, lw=2.5,
            label=r'Coherent Cross-Correlation $\rho_{\mathrm{coh}} = \mathrm{sinc}(2 \Delta f T_b)$')
    ax.plot(delta_f_norm, rho_arbitrary_phase, color=CLR_ACCENT, lw=2.2, ls='--',
            label=r'Non-Coherent Worst-Case Envelope $|\rho_{\max}| = |\mathrm{sinc}(\Delta f T_b)|$')
    
    ax.axhline(0, color='k', lw=1.0)
    
    # Highlight Coherent minimum orthogonal separation: Δf * Tb = 0.5 (MSK condition)
    ax.axvline(0.5, color=CLR_GREEN, ls=':', lw=1.8)
    ax.plot(0.5, 0.0, 'o', color=CLR_GREEN, markersize=10)
    ax.annotate(r'$\mathbf{\Delta f = \frac{1}{2 T_b} = \frac{R_b}{2}}$' + '\n' +
                r'Minimum Coherent Orthogonality' + '\n' + r'(MSK / Minimum Shift Keying)',
                xy=(0.5, 0.0), xytext=(0.55, 0.40),
                arrowprops=dict(facecolor=CLR_GREEN, shrink=0.08, width=1.5, headwidth=7),
                fontsize=10, fontweight='bold', color=CLR_GREEN,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0fdf4', edgecolor=CLR_GREEN))
    
    # Highlight Sunde's BFSK (Non-coherent minimum orthogonal separation): Δf * Tb = 1.0
    ax.axvline(1.0, color=CLR_SEC, ls=':', lw=1.8)
    ax.plot(1.0, 0.0, 's', color=CLR_SEC, markersize=10)
    ax.annotate(r'$\mathbf{\Delta f = \frac{1}{T_b} = R_b}$' + '\n' +
                r'Sunde\'s BFSK (Zero Phase Discontinuity)' + '\n' + r'& Non-Coherent Orthogonality',
                xy=(1.0, 0.0), xytext=(1.15, 0.25),
                arrowprops=dict(facecolor=CLR_SEC, shrink=0.08, width=1.5, headwidth=7),
                fontsize=10, fontweight='bold', color=CLR_SEC,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#e0f2fe', edgecolor=CLR_SEC))
    
    # Highlight Our Lab Configuration: Δf * Tb = 2.0
    ax.axvline(2.0, color=CLR_AMBER, ls=':', lw=1.8)
    ax.plot(2.0, 0.0, 'D', color=CLR_AMBER, markersize=10)
    ax.annotate(r'$\mathbf{\Delta f = 2 R_b = 2000\,\mathrm{Hz}}$' + '\n' +
                r'Laboratory Dual-Tone Orthogonal Spacing' + '\n' + r'($\rho = 0$ for Coherent & Non-Coherent)',
                xy=(2.0, 0.0), xytext=(1.6, -0.35),
                arrowprops=dict(facecolor=CLR_AMBER, shrink=0.08, width=1.5, headwidth=7),
                fontsize=10, fontweight='bold', color=CLR_AMBER,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef3c7', edgecolor=CLR_AMBER))
    
    ax.set_xlabel(r'Normalized Frequency Separation $\Delta f \cdot T_b = \frac{|f_2 - f_1|}{R_b}$', fontweight='bold', fontsize=12)
    ax.set_ylabel(r'Cross-Correlation Coefficient $\rho$', fontweight='bold', fontsize=12)
    ax.set_title('Figure 4: Frequency Separation vs. Cross-Correlation in BFSK (Proof of Orthogonality)',
                 fontsize=14, fontweight='bold', color=CLR_PRIMARY)
    ax.set_xlim(0, 3.0)
    ax.set_ylim(-0.45, 1.05)
    ax.grid(True)
    ax.legend(loc='upper right', fontsize=10.5)
    
    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, "fig4_bfsk_orthogonality_vs_frequency_separation.png")
    plt.savefig(out_path)
    plt.close()
    print(f"  -> Saved: {out_path}")

# ---------------------------------------------------------------------------
# FIGURE 5: POWER SPECTRAL DENSITY (PSD) COMPARISON
# ---------------------------------------------------------------------------
def generate_fig5_psd():
    print("[5/7] Generating Figure 5: Power Spectral Density (PSD)...")
    np.random.seed(101)
    n_sim_bits = 40000
    bits_sim = np.random.randint(0, 2, n_sim_bits)
    
    fs_psd = 40000.0  # 40 kHz
    tb_psd = 1.0 / RB
    sps_psd = int(fs_psd * tb_psd)
    t_sim = np.linspace(0, n_sim_bits * tb_psd, n_sim_bits * sps_psd, endpoint=False)
    
    # Generate long BASK signal
    m_unipolar = np.repeat(bits_sim, sps_psd)
    bask_long = m_unipolar * np.cos(2 * np.pi * FC_BASK * t_sim)
    
    # Generate long BFSK signal
    bfsk_long = np.zeros_like(t_sim)
    phase = 0.0
    for i, b in enumerate(bits_sim):
        idx = slice(i * sps_psd, (i + 1) * sps_psd)
        f_act = F2_BFSK if b == 1 else F1_BFSK
        # Continuous phase FSK (CPFSK)
        t_local = t_sim[idx] - t_sim[idx.start]
        bfsk_long[idx] = np.cos(2 * np.pi * f_act * t_local + phase)
        phase += 2 * np.pi * f_act * tb_psd
        phase = phase % (2 * np.pi)
        
    # Welch estimate of PSD
    nperseg = 4096
    f_bask, psd_bask = signal.welch(bask_long, fs_psd, nperseg=nperseg, scaling='density')
    f_bfsk, psd_bfsk = signal.welch(bfsk_long, fs_psd, nperseg=nperseg, scaling='density')
    
    # Normalize dB
    psd_bask_db = 10 * np.log10(psd_bask / np.max(psd_bask) + 1e-12)
    psd_bfsk_db = 10 * np.log10(psd_bfsk / np.max(psd_bfsk) + 1e-12)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    f_khz = f_bask / 1000.0
    
    # BASK Spectrum
    ax1.plot(f_khz, psd_bask_db, color=CLR_ACCENT, lw=1.8, label='Empirical Welch PSD (Monte Carlo 40k Bits)')
    ax1.axvline(FC_BASK / 1000.0, color='k', ls=':', lw=1.5, label=f'Carrier Spike fc = {int(FC_BASK/1000)} kHz')
    ax1.axvline((FC_BASK - RB) / 1000.0, color=CLR_SEC, ls='--', lw=1.2)
    ax1.axvline((FC_BASK + RB) / 1000.0, color=CLR_SEC, ls='--', lw=1.2, label=r'Null-to-Null Bandwidth $B = 2 R_b = 2\,\mathrm{kHz}$')
    ax1.set_ylabel('Normalized PSD [dB]', fontweight='bold')
    ax1.set_title('(a) BASK / OOK Spectrum: Carrier Impulse Delta + Scaled Sinc² Spectral Envelopes', fontsize=11, fontweight='bold', loc='left')
    ax1.set_ylim(-55, 5)
    ax1.grid(True)
    ax1.legend(loc='upper right', fontsize=9.5)
    
    # BFSK Spectrum
    ax2.plot(f_khz, psd_bfsk_db, color=CLR_GREEN, lw=1.8, label='Empirical Welch PSD (CPFSK 40k Bits)')
    ax2.axvline(F1_BFSK / 1000.0, color=CLR_AMBER, ls=':', lw=1.5, label=f'Space Tone f1 = {int(F1_BFSK/1000)} kHz')
    ax2.axvline(F2_BFSK / 1000.0, color=CLR_PRIMARY, ls=':', lw=1.5, label=f'Mark Tone f2 = {int(F2_BFSK/1000)} kHz')
    ax2.axvline((F1_BFSK - RB) / 1000.0, color=CLR_PURPLE, ls='--', lw=1.2)
    ax2.axvline((F2_BFSK + RB) / 1000.0, color=CLR_PURPLE, ls='--', lw=1.2, label=r'Carson Transmission Bandwidth $B \approx \Delta f + 2 R_b = 4\,\mathrm{kHz}$')
    ax2.set_ylabel('Normalized PSD [dB]', fontweight='bold')
    ax2.set_xlabel('Frequency f [kHz]', fontweight='bold', fontsize=11)
    ax2.set_title('(b) BFSK Spectrum: Dual Spectral Energy Concentration Around Both Tones', fontsize=11, fontweight='bold', loc='left')
    ax2.set_xlim(0, 10.0)
    ax2.set_ylim(-55, 5)
    ax2.grid(True)
    ax2.legend(loc='upper right', fontsize=9.5)
    
    fig.suptitle('Figure 5: Power Spectral Density and Transmission Bandwidth Occupancy',
                 fontsize=14, fontweight='bold', color=CLR_PRIMARY)
    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, "fig5_power_spectral_density_comparison.png")
    plt.savefig(out_path)
    plt.close()
    print(f"  -> Saved: {out_path}")

# ---------------------------------------------------------------------------
# FIGURE 6: ENVELOPE DETECTION RICIAN AND RAYLEIGH DISTRIBUTIONS
# ---------------------------------------------------------------------------
def generate_fig6_rician_rayleigh():
    print("[6/7] Generating Figure 6: Envelope Statistics (Rayleigh vs Rician)...")
    r = np.linspace(0.0, 5.0, 500)
    sigma = 0.8  # Noise standard deviation
    
    # Rayleigh for '0' (No signal, noise only):
    # p(r|0) = (r / sigma^2) * exp(-r^2 / (2 sigma^2))
    p_rayleigh = (r / (sigma**2)) * np.exp(-r**2 / (2 * (sigma**2)))
    
    # Rician for '1' across diverse carrier amplitudes A (representing varying SNRs)
    A_vals = [1.2, 2.0, 3.2]
    snr_labels = ['Weak Carrier (A = 1.2)', 'Moderate Carrier (A = 2.0)', 'Strong Carrier (A = 3.2)']
    colors = [CLR_SEC, CLR_AMBER, CLR_GREEN]
    
    fig, ax = plt.subplots(figsize=(11, 6))
    
    # Plot Rayleigh
    ax.plot(r, p_rayleigh, color=CLR_PRIMARY, lw=2.5, label=r'Rayleigh Distribution $p(R|0)$ (Space bit: Noise Only)')
    ax.fill_between(r, 0, p_rayleigh, color=CLR_PRIMARY, alpha=0.15)
    
    # Plot Rician curves
    # p(r|1) = (r / sigma^2) * exp(-(r^2 + A^2)/(2 sigma^2)) * I0(r * A / sigma^2)
    for A, lab, clr in zip(A_vals, snr_labels, colors):
        z = (r * A) / (sigma**2)
        p_rician = (r / (sigma**2)) * np.exp(-(r**2 + A**2) / (2 * (sigma**2))) * special.i0(z)
        ax.plot(r, p_rician, color=clr, lw=2.2, label=rf'Rician $p(R|1)$ — {lab}')
        
    # Optimum threshold example for A = 2.0
    # Threshold where p_rayleigh(r) == p_rician(r)
    z_mid = (r * 2.0) / (sigma**2)
    p_mid = (r / (sigma**2)) * np.exp(-(r**2 + 2.0**2) / (2 * (sigma**2))) * special.i0(z_mid)
    diff = np.abs(p_rayleigh - p_mid)
    idx_thresh = np.argmin(diff[r > 0.5]) + np.argmax(r > 0.5)
    r_thresh = r[idx_thresh]
    
    ax.axvline(r_thresh, color=CLR_ACCENT, ls='--', lw=2.0, label=rf'Optimum Slicing Threshold $\gamma_{{\mathrm{{env}}}} = {r_thresh:.2f}$')
    ax.plot(r_thresh, p_rayleigh[idx_thresh], 'ro', markersize=8)
    
    ax.set_xlabel('Received Envelope Amplitude R [Volts]', fontweight='bold', fontsize=12)
    ax.set_ylabel('Probability Density Function p(R)', fontweight='bold', fontsize=12)
    ax.set_title('Figure 6: Statistical Mechanics of Non-Coherent Detection (Rayleigh vs. Rician Fading Distributions)',
                 fontsize=14, fontweight='bold', color=CLR_PRIMARY)
    ax.set_xlim(0, 5.0)
    ax.set_ylim(0, 0.9)
    ax.grid(True)
    ax.legend(loc='upper right', fontsize=10.5)
    
    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, "fig6_envelope_detection_rician_rayleigh_distributions.png")
    plt.savefig(out_path)
    plt.close()
    print(f"  -> Saved: {out_path}")

# ---------------------------------------------------------------------------
# FIGURE 7: COMPREHENSIVE MONTE CARLO BER BENCHMARK
# ---------------------------------------------------------------------------
def generate_fig7_ber():
    print("[7/7] Generating Figure 7: Monte Carlo Bit Error Rate (BER) Simulation...")
    snr_db = np.arange(0, 13, 1)  # 0 to 12 dB
    snr_lin = 10.0 ** (snr_db / 10.0)
    
    # Theoretical Calculations:
    # 1. Coherent BPSK (Benchmark): Q(sqrt(2 * Eb/N0))
    ber_bpsk_th = 0.5 * special.erfc(np.sqrt(snr_lin))
    
    # 2. Coherent BFSK: Q(sqrt(Eb/N0))  (3 dB worse than BPSK)
    ber_bfsk_coh_th = 0.5 * special.erfc(np.sqrt(snr_lin / 2.0))
    
    # 3. Non-Coherent BFSK: 0.5 * exp(-0.5 * Eb/N0)
    ber_bfsk_noncoh_th = 0.5 * np.exp(-0.5 * snr_lin)
    
    # 4. Coherent BASK: Q(sqrt(Eb / (2 N0)))  (6 dB worse than BPSK for average Eb)
    ber_bask_coh_th = 0.5 * special.erfc(np.sqrt(snr_lin / 4.0))
    
    # 5. Non-Coherent BASK: approx 0.5 * exp(-Eb / (4 N0)) at high SNR
    ber_bask_noncoh_th = 0.5 * np.exp(-0.25 * snr_lin)
    
    # Monte Carlo Empirical Simulation (200,000 bits per SNR point)
    n_mc_bits = 200000
    print(f"    Running Monte Carlo simulation ({n_mc_bits:,} bits per SNR point)...")
    np.random.seed(2026)
    tx_bits = np.random.randint(0, 2, n_mc_bits)
    
    ber_bfsk_coh_sim = []
    ber_bfsk_noncoh_sim = []
    ber_bask_coh_sim = []
    
    for snr in snr_lin:
        # Standard deviation of noise for unit energy Eb = 1
        # Eb/N0 = snr => N0 = 1 / snr => sigma^2 = N0 / 2 = 1 / (2 * snr)
        sigma_n = np.sqrt(1.0 / (2.0 * snr))
        
        # --- Coherent BASK Simulation ---
        # s1 = sqrt(2), s0 = 0 (average energy = 1)
        s_bask = np.where(tx_bits == 1, np.sqrt(2.0), 0.0)
        r_bask = s_bask + np.random.normal(0, sigma_n, n_mc_bits)
        gamma = np.sqrt(2.0) / 2.0
        dec_bask = (r_bask > gamma).astype(int)
        ber_bask_coh_sim.append(np.mean(tx_bits != dec_bask))
        
        # --- Coherent BFSK Simulation ---
        # s1 = [0, 1], s0 = [1, 0]
        # In noise: r1 = s_comp1 + n1, r2 = s_comp2 + n2
        n1 = np.random.normal(0, sigma_n, n_mc_bits)
        n2 = np.random.normal(0, sigma_n, n_mc_bits)
        r_space = np.where(tx_bits == 0, 1.0, 0.0) + n1
        r_mark = np.where(tx_bits == 1, 1.0, 0.0) + n2
        dec_bfsk_coh = (r_mark > r_space).astype(int)
        ber_bfsk_coh_sim.append(np.mean(tx_bits != dec_bfsk_coh))
        
        # --- Non-Coherent BFSK Simulation (Quadrature envelope branches) ---
        # Each branch has In-phase and Quadrature noise: n_i, n_q ~ N(0, sigma^2)
        ni1 = np.random.normal(0, sigma_n, n_mc_bits)
        nq1 = np.random.normal(0, sigma_n, n_mc_bits)
        ni2 = np.random.normal(0, sigma_n, n_mc_bits)
        nq2 = np.random.normal(0, sigma_n, n_mc_bits)
        
        env1 = np.sqrt((np.where(tx_bits == 0, 1.0, 0.0) + ni1)**2 + nq1**2)
        env2 = np.sqrt((np.where(tx_bits == 1, 1.0, 0.0) + ni2)**2 + nq2**2)
        dec_bfsk_noncoh = (env2 > env1).astype(int)
        ber_bfsk_noncoh_sim.append(np.mean(tx_bits != dec_bfsk_noncoh))
        
    # Plotting
    fig, ax = plt.subplots(figsize=(11, 8))
    
    # Theoretical lines
    ax.semilogy(snr_db, ber_bpsk_th, color='#64748b', lw=1.8, ls=':', label=r'Theoretical BPSK Benchmark: $Q\left(\sqrt{2 E_b / N_0}\right)$')
    ax.semilogy(snr_db, ber_bfsk_coh_th, color=CLR_PRIMARY, lw=2.2, label=r'Theoretical Coherent BFSK: $Q\left(\sqrt{E_b / N_0}\right)$')
    ax.semilogy(snr_db, ber_bfsk_noncoh_th, color=CLR_GREEN, lw=2.0, ls='--', label=r'Theoretical Non-Coherent BFSK: $\frac{1}{2} e^{-E_b / (2 N_0)}$')
    ax.semilogy(snr_db, ber_bask_coh_th, color=CLR_ACCENT, lw=2.0, label=r'Theoretical Coherent BASK: $Q\left(\sqrt{E_b / (2 N_0)}\right)$')
    ax.semilogy(snr_db, ber_bask_noncoh_th, color=CLR_AMBER, lw=1.8, ls='--', label=r'Theoretical Non-Coherent BASK: $\frac{1}{2} e^{-E_b / (4 N_0)}$')
    
    # Monte Carlo markers
    ax.semilogy(snr_db, ber_bfsk_coh_sim, 'o', color=CLR_PRIMARY, markersize=7, label='Monte Carlo Coherent BFSK (200k Bits)')
    ax.semilogy(snr_db, ber_bfsk_noncoh_sim, '^', color=CLR_GREEN, markersize=7, label='Monte Carlo Non-Coherent BFSK (200k Bits)')
    ax.semilogy(snr_db, ber_bask_coh_sim, 's', color=CLR_ACCENT, markersize=7, label='Monte Carlo Coherent BASK (200k Bits)')
    
    # Annotations
    ax.annotate('3.0 dB Power Penalty\n(BFSK vs Antipodal BPSK)',
                xy=(7.0, 1e-3), xytext=(3.0, 5e-5),
                arrowprops=dict(facecolor=CLR_PRIMARY, shrink=0.08, width=1.5, headwidth=6),
                fontsize=9.5, fontweight='bold', color=CLR_PRIMARY,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#e0f2fe', edgecolor=CLR_PRIMARY))
    
    ax.annotate('Non-Coherent BFSK Penalty\n(< 1.0 dB at BER = 1e-4)',
                xy=(10.0, 3e-3), xytext=(8.0, 1e-2),
                arrowprops=dict(facecolor=CLR_GREEN, shrink=0.08, width=1.5, headwidth=6),
                fontsize=9.5, fontweight='bold', color=CLR_GREEN,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0fdf4', edgecolor=CLR_GREEN))
    
    ax.annotate('BASK 6.0 dB Penalty\n(Due to On-Off Energy Waste)',
                xy=(9.0, 1.5e-2), xytext=(5.5, 0.15),
                arrowprops=dict(facecolor=CLR_ACCENT, shrink=0.08, width=1.5, headwidth=6),
                fontsize=9.5, fontweight='bold', color=CLR_ACCENT,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#fee2e2', edgecolor=CLR_ACCENT))
    
    ax.set_xlabel(r'Signal-to-Noise Ratio $E_b / N_0$ [dB]', fontweight='bold', fontsize=12)
    ax.set_ylabel(r'Bit Error Rate (BER) $P_b$', fontweight='bold', fontsize=12)
    ax.set_title('Figure 7: Monte Carlo Bit Error Rate Benchmark (Coherent vs. Non-Coherent BASK & BFSK)',
                 fontsize=14, fontweight='bold', color=CLR_PRIMARY)
    ax.set_xlim(0, 12)
    ax.set_ylim(1e-5, 0.5)
    ax.grid(True, which='both')
    ax.legend(loc='lower left', fontsize=9.2)
    
    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, "fig7_monte_carlo_ber_performance_curves.png")
    plt.savefig(out_path)
    plt.close()
    print(f"  -> Saved: {out_path}")

if __name__ == '__main__':
    generate_fig1_waveforms()
    generate_fig2_constellations()
    generate_fig3_demod_pipeline()
    generate_fig4_orthogonality()
    generate_fig5_psd()
    generate_fig6_rician_rayleigh()
    generate_fig7_ber()
    print("=" * 75)
    print("ALL 7 FIGURES SUCCESSFULLY GENERATED FOR EXPERIMENT 09!")
    print("=" * 75)
