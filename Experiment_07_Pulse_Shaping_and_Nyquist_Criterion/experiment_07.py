#!/usr/bin/env python3
"""
================================================================================
EXPERIMENT 7: PULSE SHAPING & NYQUIST CRITERION FOR ZERO INTER-SYMBOL INTERFERENCE (ISI)
================================================================================
Department of Electronics and Communication Engineering
Cooch Behar Government Engineering College
Course: Software-Based Digital Communication Laboratory (EC593 / EC592)
Student Name: Apurba Maity | Roll No.: 34900324001 | Semester: 5th Sem ECE

Description:
  This script implements from first principles in Python (NumPy, SciPy, Matplotlib):
    1. The Nyquist First Criterion for Zero Inter-Symbol Interference (ISI) in baseband digital transmission.
    2. Time-domain generators for Sinc, Raised-Cosine (RC), and Root-Raised-Cosine (RRC/SRRC) pulses
       with exact singularity handling at t = 0, t = +-Ts/(2*alpha), and t = +-Ts/(4*alpha).
    3. Frequency-domain spectral evaluation verifying the Nyquist vestigial symmetry and excess bandwidth
       B = (1 + alpha) * Rs / 2.
    4. Multi-symbol digital pulse train transmission showing zero-ISI sampling at t = k*Ts.
    5. Square-Root Raised-Cosine (SRRC) matched filter partitioning:
       - Proving single RRC pulse exhibits non-zero ISI.
       - Proving cascaded Tx RRC * Rx RRC convolution synthesizes full Raised-Cosine with zero ISI.
    6. Timing jitter sensitivity and Peak ISI distortion analysis under sampling clock phase errors.
    7. High-density Eye Diagram synthesis across roll-off factors alpha in {0.0, 0.25, 0.5, 1.0} under AWGN.

Outputs:
  Generates 6 publication-grade figures (300 DPI) in the 'plots/' subfolder.
================================================================================
"""

import os
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Configure publication-grade styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 1.0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')
os.makedirs(PLOTS_DIR, exist_ok=True)


# ==============================================================================
# 1. CORE PULSE SHAPING ENGINES (FIRST PRINCIPLES)
# ==============================================================================

def raised_cosine_pulse(t, Ts=1.0, alpha=0.5):
    """
    Generate Raised-Cosine (RC) pulse p_RC(t).
    
    Formula:
      p_RC(t) = sinc(t / Ts) * [ cos(pi * alpha * t / Ts) / (1 - (2 * alpha * t / Ts)^2) ]
      
    Singularity handling:
      - At t = 0: p_RC(0) = 1.0
      - At t = +- Ts / (2 * alpha): p_RC(t) = (pi / 4) * sinc(1 / (2 * alpha))
    """
    t = np.asarray(t, dtype=float)
    if alpha == 0.0:
        return np.sinc(t / Ts)
    
    out = np.zeros_like(t)
    denom = 1.0 - (2.0 * alpha * t / Ts) ** 2
    sing_mask = np.isclose(np.abs(denom), 0.0, atol=1e-7)
    
    # Singularity points
    out[sing_mask] = (np.pi / 4.0) * np.sinc(1.0 / (2.0 * alpha))
    
    # Regular points
    reg_mask = ~sing_mask
    t_reg = t[reg_mask]
    out[reg_mask] = np.sinc(t_reg / Ts) * np.cos(np.pi * alpha * t_reg / Ts) / denom[reg_mask]
    return out


def root_raised_cosine_pulse(t, Ts=1.0, alpha=0.5):
    """
    Generate Root-Raised-Cosine (RRC / SRRC) pulse h_RRC(t).
    
    Formula:
      h_RRC(t) = (1 / sqrt(Ts)) * [ sin(pi*t*(1-alpha)/Ts) + 4*alpha*(t/Ts)*cos(pi*t*(1+alpha)/Ts) ] /
                                   [ pi*(t/Ts) * (1 - (4*alpha*t/Ts)^2) ]
                                   
    Singularities:
      - At t = 0: h_RRC(0) = (1 / sqrt(Ts)) * [ 1 - alpha + 4*alpha / pi ]
      - At t = +- Ts / (4*alpha):
          h_RRC(t) = (alpha / sqrt(2*Ts)) * [ (1 + 2/pi)*sin(pi/(4*alpha)) + (1 - 2/pi)*cos(pi/(4*alpha)) ]
    """
    t = np.asarray(t, dtype=float)
    if alpha == 0.0:
        return (1.0 / np.sqrt(Ts)) * np.sinc(t / Ts)
    
    out = np.zeros_like(t)
    
    # Singularity 1: t = 0
    zero_mask = np.isclose(t, 0.0, atol=1e-7)
    out[zero_mask] = (1.0 / np.sqrt(Ts)) * (1.0 - alpha + 4.0 * alpha / np.pi)
    
    # Singularity 2: t = +- Ts / (4*alpha)
    denom = 1.0 - (4.0 * alpha * t / Ts) ** 2
    sing_mask = np.isclose(np.abs(denom), 0.0, atol=1e-7) & ~zero_mask
    val_sing = (alpha / np.sqrt(2.0 * Ts)) * (
        (1.0 + 2.0 / np.pi) * np.sin(np.pi / (4.0 * alpha)) +
        (1.0 - 2.0 / np.pi) * np.cos(np.pi / (4.0 * alpha))
    )
    out[sing_mask] = val_sing
    
    # Regular points
    reg_mask = ~zero_mask & ~sing_mask
    t_reg = t[reg_mask]
    num = (np.sin(np.pi * t_reg * (1.0 - alpha) / Ts) + 
           4.0 * alpha * (t_reg / Ts) * np.cos(np.pi * t_reg * (1.0 + alpha) / Ts))
    den = np.pi * (t_reg / Ts) * (1.0 - (4.0 * alpha * t_reg / Ts) ** 2)
    out[reg_mask] = (1.0 / np.sqrt(Ts)) * (num / den)
    return out


def raised_cosine_spectrum(f, Ts=1.0, alpha=0.5):
    """
    Analytical continuous Fourier spectrum P_RC(f) of Raised-Cosine filter.
    
    B0 = 1 / (2 * Ts)
    Bandwidth = B0 * (1 + alpha)
    """
    f = np.asarray(f, dtype=float)
    f_abs = np.abs(f)
    B0 = 1.0 / (2.0 * Ts)
    
    if alpha == 0.0:
        return np.where(f_abs <= B0, Ts, 0.0)
    
    f1 = (1.0 - alpha) * B0
    f2 = (1.0 + alpha) * B0
    
    P = np.zeros_like(f_abs)
    # Passband
    P[f_abs <= f1] = Ts
    # Transition band
    trans_mask = (f_abs > f1) & (f_abs <= f2)
    P[trans_mask] = (Ts / 2.0) * (1.0 + np.cos((np.pi * Ts / alpha) * (f_abs[trans_mask] - f1)))
    # Stopband is 0
    return P


# ==============================================================================
# 2. EXPERIMENTAL MODULE 1: TIME-DOMAIN NYQUIST PULSE COMPARISON (FIGURE 1)
# ==============================================================================

def generate_figure_1():
    """
    Figure 1: Time-Domain Impulse Responses of Nyquist Pulses
      - Left: Linear time waveforms p_RC(t) showing zero-crossings and side-lobe dampening.
      - Right: Semi-log decay |p_RC(t)| showing 1/t (alpha=0) vs. 1/t^3 (alpha>0) tail suppression.
    """
    print("Generating Figure 1: Time-Domain Nyquist Pulse Responses...")
    Ts = 1.0
    sps = 200
    t_span = 6.0
    t = np.linspace(-t_span * Ts, t_span * Ts, int(2 * t_span * sps) + 1)
    
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    colors = ['#dc2626', '#d97706', '#0284c7', '#16a34a', '#9333ea']
    labels = [r'$\alpha = 0.0$ (Ideal Sinc)', r'$\alpha = 0.25$', r'$\alpha = 0.50$',
              r'$\alpha = 0.75$', r'$\alpha = 1.00$ (Full Roll-off)']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    
    # Subplot 1: Linear Time Domain
    for alpha, color, label in zip(alphas, colors, labels):
        p = raised_cosine_pulse(t, Ts=Ts, alpha=alpha)
        lw = 2.2 if alpha in [0.0, 0.5, 1.0] else 1.5
        ax1.plot(t / Ts, p, label=label, color=color, linewidth=lw)
    
    # Highlight zero crossings
    sampling_instants = np.arange(-int(t_span), int(t_span) + 1)
    for k in sampling_instants:
        if k != 0:
            ax1.axvline(x=k, color='#94a3b8', linestyle=':', linewidth=0.8, alpha=0.7)
            ax1.plot(k, 0, 'o', color='#0f172a', markersize=4.5, zorder=5)
        else:
            ax1.plot(0, 1.0, 's', color='#0f172a', markersize=6, zorder=5)
    
    ax1.axhline(0, color='#64748b', linestyle='-', linewidth=0.8)
    ax1.set_xlim(-t_span, t_span)
    ax1.set_ylim(-0.35, 1.15)
    ax1.set_xlabel(r'Normalized Time $t / T_s$', fontsize=12, fontweight='bold', color='#1e293b')
    ax1.set_ylabel(r'Normalized Amplitude $p(t)$', fontsize=12, fontweight='bold', color='#1e293b')
    ax1.set_title(r'(a) Nyquist Raised-Cosine Impulse Response $p_{\mathrm{RC}}(t)$' + '\n' +
                  r'Zero ISI Property: $p(m T_s) = \delta[m]$', fontsize=13, fontweight='bold', color='#0f172a')
    ax1.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax1.legend(loc='upper right', framealpha=0.95, edgecolor='#cbd5e1', fontsize=10)
    ax1.set_facecolor('#f8fafc')
    
    # Subplot 2: Log-Magnitude Envelope Decay
    t_pos = np.linspace(0.01, 8.0, 1000)
    for alpha, color, label in zip(alphas, colors, labels):
        p = np.abs(raised_cosine_pulse(t_pos, Ts=Ts, alpha=alpha))
        p_db = 20.0 * np.log10(np.clip(p, 1e-5, None))
        lw = 2.0 if alpha in [0.0, 0.5, 1.0] else 1.4
        ax2.plot(t_pos, p_db, label=label, color=color, linewidth=lw)
    
    # Asymptotic reference lines
    t_ref = np.linspace(1.5, 8.0, 200)
    decay_sinc = 20.0 * np.log10(1.0 / (np.pi * t_ref))
    decay_rc = 20.0 * np.log10(1.0 / (4.0 * np.pi * t_ref**3))
    ax2.plot(t_ref, decay_sinc, '--', color='#7f1d1d', linewidth=1.5, label=r'Asymptotic $\propto 1/t$ (Sinc)')
    ax2.plot(t_ref, decay_rc, '--', color='#14532d', linewidth=1.5, label=r'Asymptotic $\propto 1/t^3$ (RC)')
    
    ax2.set_xlim(0, 8.0)
    ax2.set_ylim(-80, 5)
    ax2.set_xlabel(r'Normalized Time $t / T_s$', fontsize=12, fontweight='bold', color='#1e293b')
    ax2.set_ylabel(r'Envelope Attenuation $20 \log_{10}|p(t)|$ [dB]', fontsize=12, fontweight='bold', color='#1e293b')
    ax2.set_title(r'(b) Side-Lobe Decay Rate Comparison' + '\n' +
                  r'$1/t$ Harmonic Tail Divergence vs. $1/t^3$ Rapid Convergence', fontsize=13, fontweight='bold', color='#0f172a')
    ax2.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax2.legend(loc='upper right', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9.5)
    ax2.set_facecolor('#f8fafc')
    
    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, 'fig1_nyquist_pulse_shapes_time_domain.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


# ==============================================================================
# 3. EXPERIMENTAL MODULE 2: FREQUENCY-DOMAIN SPECTRAL CHARACTERISTICS (FIGURE 2)
# ==============================================================================

def generate_figure_2():
    """
    Figure 2: Frequency-Domain Spectral Characteristics of Raised-Cosine Filters
      - Left: Linear magnitude spectrum showing Nyquist vestigial symmetry around (B0, 0.5).
      - Right: Logarithmic spectrum in dB illustrating stopband roll-off and excess bandwidth.
    """
    print("Generating Figure 2: Frequency-Domain Spectral Characteristics...")
    Ts = 1.0
    Rs = 1.0 / Ts
    B0 = Rs / 2.0
    f = np.linspace(-1.2 * Rs, 1.2 * Rs, 2000)
    
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    colors = ['#dc2626', '#d97706', '#0284c7', '#16a34a', '#9333ea']
    labels = [r'$\alpha = 0.0$ ($B = B_0$)', r'$\alpha = 0.25$ ($B = 1.25 B_0$)',
              r'$\alpha = 0.50$ ($B = 1.50 B_0$)', r'$\alpha = 0.75$ ($B = 1.75 B_0$)',
              r'$\alpha = 1.00$ ($B = 2.00 B_0$)']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    
    # Subplot 1: Linear Magnitude
    for alpha, color, label in zip(alphas, colors, labels):
        P = raised_cosine_spectrum(f, Ts=Ts, alpha=alpha) / Ts
        lw = 2.2 if alpha in [0.0, 0.5, 1.0] else 1.5
        ax1.plot(f / Rs, P, label=label, color=color, linewidth=lw)
    
    # Mark Nyquist frequency and -6 dB (0.5) point
    ax1.axvline(x=B0 / Rs, color='#0f172a', linestyle='--', linewidth=1.2, label=r'Nyquist Bandwidth $B_0 = R_s / 2$')
    ax1.axhline(y=0.5, color='#64748b', linestyle=':', linewidth=1.0)
    ax1.plot([B0 / Rs], [0.5], 'ko', markersize=6, zorder=6)
    ax1.annotate(r'Vestigial Symmetry Point $(B_0, 0.5)$' + '\n' + r'$P(B_0 - \Delta f) + P(B_0 + \Delta f) = T_s$',
                 xy=(B0 / Rs, 0.5), xytext=(0.58, 0.70),
                 arrowprops=dict(facecolor='#0f172a', shrink=0.08, width=1.2, headwidth=6),
                 fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#e2e8f0', edgecolor='#94a3b8'))
    
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-0.05, 1.1)
    ax1.set_xlabel(r'Normalized Frequency $f / R_s$', fontsize=12, fontweight='bold', color='#1e293b')
    ax1.set_ylabel(r'Normalized Spectrum $|P_{\mathrm{RC}}(f)| / T_s$', fontsize=12, fontweight='bold', color='#1e293b')
    ax1.set_title(r'(a) Linear Frequency Response $|P_{\mathrm{RC}}(f)|$' + '\n' +
                  r'Nyquist First Criterion: Flat Aliased Spectrum Sum', fontsize=13, fontweight='bold', color='#0f172a')
    ax1.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax1.legend(loc='lower left', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9.5)
    ax1.set_facecolor('#f8fafc')
    
    # Subplot 2: Logarithmic Power Spectrum (dB)
    f_pos = np.linspace(0, 1.2 * Rs, 1500)
    for alpha, color, label in zip(alphas, colors, labels):
        P = raised_cosine_spectrum(f_pos, Ts=Ts, alpha=alpha) / Ts
        P_db = 10.0 * np.log10(np.clip(P ** 2, 1e-8, 1.0))
        lw = 2.0 if alpha in [0.0, 0.5, 1.0] else 1.4
        ax2.plot(f_pos / Rs, P_db, label=label, color=color, linewidth=lw)
    
    ax2.axvline(x=B0 / Rs, color='#0f172a', linestyle='--', linewidth=1.2, label=r'Nyquist Cutoff $f = 0.5 R_s$ (-6 dB)')
    ax2.axhline(y=-6.02, color='#64748b', linestyle=':', linewidth=1.0)
    
    ax2.set_xlim(0, 1.15)
    ax2.set_ylim(-65, 3)
    ax2.set_xlabel(r'Normalized Frequency $f / R_s$', fontsize=12, fontweight='bold', color='#1e293b')
    ax2.set_ylabel(r'Power Attenuation $10 \log_{10}|P(f)|^2$ [dB]', fontsize=12, fontweight='bold', color='#1e293b')
    ax2.set_title(r'(b) Logarithmic Frequency Spectrum [dB]' + '\n' +
                  r'Transmission Bandwidth: $B = \frac{R_s}{2}(1 + \alpha)$', fontsize=13, fontweight='bold', color='#0f172a')
    ax2.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax2.legend(loc='lower left', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9.5)
    ax2.set_facecolor('#f8fafc')
    
    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, 'fig2_raised_cosine_frequency_spectra.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


# ==============================================================================
# 4. EXPERIMENTAL MODULE 3: MULTI-SYMBOL TRANSMISSION & ZERO-ISI PROOF (FIGURE 3)
# ==============================================================================

def generate_figure_3():
    """
    Figure 3: Multi-Symbol Baseband Transmission and Zero-ISI Sampling
      - Demonstrates 8 transmitted bipolar symbols shaped by Raised-Cosine (alpha = 0.5).
      - Displays overlapping individual pulse contributions and composite analog waveform.
      - Graphically confirms that at t = m*Ts, all neighboring pulses are precisely zero.
    """
    print("Generating Figure 3: Multi-Symbol Transmission & Zero-ISI Sampling...")
    Ts = 1.0
    sps = 100
    alpha = 0.5
    
    # 8-symbol sequence
    symbols = np.array([+1, -1, +1, +1, -1, +1, -1, -1])
    N = len(symbols)
    
    t_pulse_span = 5.0
    t_start = -2.0 * Ts
    t_end = (N + 1.0) * Ts
    t_cont = np.linspace(t_start, t_end, int((t_end - t_start) * sps) + 1)
    
    # Calculate composite waveform and individual pulses
    composite_signal = np.zeros_like(t_cont)
    pulse_matrix = []
    
    for k, ak in enumerate(symbols):
        t_shift = t_cont - k * Ts
        p_k = ak * raised_cosine_pulse(t_shift, Ts=Ts, alpha=alpha)
        composite_signal += p_k
        pulse_matrix.append(p_k)
    
    fig, ax = plt.subplots(figsize=(15, 6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    
    # Distinct pastel colors for individual pulses
    pulse_colors = ['#f87171', '#fb923c', '#fbbf24', '#4ade80', '#38bdf8', '#818cf8', '#c084fc', '#f472b6']
    
    for k in range(N):
        ax.plot(t_cont / Ts, pulse_matrix[k], linestyle='--', linewidth=1.3, color=pulse_colors[k],
                label=f'$a_{k} = {symbols[k]:+d} \\cdot p(t - {k}T_s)$' if k < 4 else None, alpha=0.85)
    
    # Composite line
    ax.plot(t_cont / Ts, composite_signal, color='#0f172a', linewidth=2.8, label=r'Composite Signal $s(t) = \sum a_k p(t - k T_s)$', zorder=4)
    
    # Sampling instants
    for k, ak in enumerate(symbols):
        ax.axvline(x=k, color='#64748b', linestyle=':', linewidth=1.0)
        ax.plot(k, ak, 'o', color='#dc2626' if ak > 0 else '#2563eb', markersize=8, zorder=6)
        ax.annotate(f'$t = {k}T_s$\n$y = {ak:+d}$', xy=(k, ak),
                    xytext=(k, ak + (0.25 if ak > 0 else -0.38)),
                    ha='center', fontsize=9.5, fontweight='bold',
                    color='#0f172a',
                    bbox=dict(boxstyle='round,pad=0.25', facecolor='#f1f5f9', edgecolor='#94a3b8', alpha=0.9))
    
    ax.axhline(0, color='#94a3b8', linestyle='-', linewidth=0.8)
    ax.set_xlim(t_start / Ts, t_end / Ts)
    ax.set_ylim(-2.2, 2.2)
    ax.set_xlabel(r'Normalized Time $t / T_s$', fontsize=12, fontweight='bold', color='#1e293b')
    ax.set_ylabel(r'Signal Amplitude', fontsize=12, fontweight='bold', color='#1e293b')
    ax.set_title(r'Time-Domain Superposition & Nyquist Zero-ISI Proof ($\alpha = 0.50$)' + '\n' +
                 r'At $t = m T_s$: $s(m T_s) = a_m p(0) + \sum_{k \ne m} a_k p((m-k)T_s) = a_m + 0 = a_m$',
                 fontsize=13, fontweight='bold', color='#0f172a')
    ax.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax.legend(loc='lower left', framealpha=0.95, edgecolor='#cbd5e1', fontsize=9.5, ncol=2)
    ax.set_facecolor('#f8fafc')
    
    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, 'fig3_multi_symbol_transmission_and_zero_isi.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


# ==============================================================================
# 5. EXPERIMENTAL MODULE 4: SRRC MATCHED FILTER CASCADE (FIGURE 4)
# ==============================================================================

def generate_figure_4():
    """
    Figure 4: Square-Root Raised-Cosine (SRRC) Matched Filter Cascade
      - Top-Left: Transmitter SRRC filter h_tx(t).
      - Top-Right: Receiver Matched SRRC filter h_rx(t) = h_tx(-t).
      - Bottom-Left: Convolution h_cascade(t) = h_tx(t) * h_rx(t) vs. analytical p_RC(t).
      - Bottom-Right: Discrete samples at t = m*Ts for Single RRC vs. Cascaded RRC (Zero-ISI proof).
    """
    print("Generating Figure 4: SRRC Matched Filter Partition & Cascade...")
    Ts = 1.0
    alpha = 0.5
    sps = 64
    span = 6.0  # filter spans +-6 symbols
    
    t = np.linspace(-span * Ts, span * Ts, int(2 * span * sps) + 1)
    dt = t[1] - t[0]
    
    # 1. Transmitter RRC
    h_tx = root_raised_cosine_pulse(t, Ts=Ts, alpha=alpha)
    # Energy normalize filter so sum(h^2)*dt = 1
    h_tx = h_tx / np.sqrt(np.sum(h_tx**2) * dt)
    
    # 2. Receiver Matched RRC (h_rx(t) = h_tx(-t))
    h_rx = h_tx[::-1]
    
    # 3. Cascade convolution
    h_cascade = np.convolve(h_tx, h_rx, mode='same') * dt
    # Normalize peak to 1.0 for direct comparison with p_RC
    h_cascade = h_cascade / np.max(h_cascade)
    
    # Analytical full Raised-Cosine
    p_rc_theory = raised_cosine_pulse(t, Ts=Ts, alpha=alpha)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 11), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    
    # 1. Transmitter SRRC
    ax1.plot(t / Ts, h_tx, color='#2563eb', linewidth=2.0, label=r'Tx SRRC Pulse $h_{\mathrm{tx}}(t)$')
    ax1.axhline(0, color='#64748b', linestyle='-', linewidth=0.8)
    for m in range(-4, 5):
        if m != 0:
            val = np.interp(m * Ts, t, h_tx)
            ax1.plot(m, val, 'ro', markersize=5)
    ax1.set_xlim(-4, 4)
    ax1.set_xlabel(r'Normalized Time $t / T_s$', fontsize=11, fontweight='bold', color='#1e293b')
    ax1.set_ylabel(r'Amplitude', fontsize=11, fontweight='bold', color='#1e293b')
    ax1.set_title(r'(a) Transmitter Pulse Shaping Filter: $H_{\mathrm{tx}}(f) = \sqrt{P_{\mathrm{RC}}(f)}$' + '\n' +
                  r'Notice Non-Zero Values at $t = m T_s$ (Single SRRC has ISI!)', fontsize=11.5, fontweight='bold', color='#0f172a')
    ax1.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax1.legend(loc='upper right', framealpha=0.95, edgecolor='#cbd5e1')
    ax1.set_facecolor('#f8fafc')
    
    # 2. Receiver Matched SRRC
    ax2.plot(t / Ts, h_rx, color='#16a34a', linewidth=2.0, label=r'Rx Matched SRRC $h_{\mathrm{rx}}(t) = h_{\mathrm{tx}}(-t)$')
    ax2.axhline(0, color='#64748b', linestyle='-', linewidth=0.8)
    ax2.set_xlim(-4, 4)
    ax2.set_xlabel(r'Normalized Time $t / T_s$', fontsize=11, fontweight='bold', color='#1e293b')
    ax2.set_ylabel(r'Amplitude', fontsize=11, fontweight='bold', color='#1e293b')
    ax2.set_title(r'(b) Receiver Matched Filter: $H_{\mathrm{rx}}(f) = H_{\mathrm{tx}}^*(f)$' + '\n' +
                  r'Maximizes Received Signal-to-Noise Ratio (SNR) in AWGN', fontsize=11.5, fontweight='bold', color='#0f172a')
    ax2.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax2.legend(loc='upper right', framealpha=0.95, edgecolor='#cbd5e1')
    ax2.set_facecolor('#f8fafc')
    
    # 3. Cascaded End-to-End Convolution vs Analytical RC
    ax3.plot(t / Ts, p_rc_theory, color='#dc2626', linewidth=2.5, label=r'Target Analytical $p_{\mathrm{RC}}(t)$ ($\alpha = 0.50$)', alpha=0.7)
    ax3.plot(t / Ts, h_cascade, '--', color='#0f172a', linewidth=2.0, label=r'Cascaded Output $h_{\mathrm{tx}}(t) * h_{\mathrm{rx}}(t)$')
    
    # Residual Error inset/plot
    err = np.abs(p_rc_theory - h_cascade)
    ax3_inset = ax3.inset_axes([0.62, 0.45, 0.35, 0.28])
    ax3_inset.plot(t / Ts, err, color='#9333ea', linewidth=1.2)
    ax3_inset.set_title(f'Residual Error (Max: {np.max(err):.2e})', fontsize=8.5, fontweight='bold')
    ax3_inset.grid(True, linestyle=':', alpha=0.6)
    ax3_inset.set_xlim(-3, 3)
    ax3_inset.set_facecolor('#ffffff')
    
    ax3.set_xlim(-4, 4)
    ax3.set_xlabel(r'Normalized Time $t / T_s$', fontsize=11, fontweight='bold', color='#1e293b')
    ax3.set_ylabel(r'Amplitude', fontsize=11, fontweight='bold', color='#1e293b')
    ax3.set_title(r'(c) Cascaded Convolution Synthesis: $H_{\mathrm{total}}(f) = |H_{\mathrm{tx}}(f)|^2 = P_{\mathrm{RC}}(f)$' + '\n' +
                  r'Numerical Convolution Exactly Reproduces Full Raised-Cosine', fontsize=11.5, fontweight='bold', color='#0f172a')
    ax3.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax3.legend(loc='upper left', framealpha=0.95, edgecolor='#cbd5e1')
    ax3.set_facecolor('#f8fafc')
    
    # 4. Discrete Sample Comparison (Zero-ISI Confirmation)
    m_indices = np.arange(-4, 5)
    rrc_samples = np.interp(m_indices * Ts, t, h_tx / np.max(h_tx))
    cascade_samples = np.interp(m_indices * Ts, t, h_cascade)
    
    x = np.arange(len(m_indices))
    width = 0.35
    ax4.bar(x - width/2, np.abs(rrc_samples), width, label='Single SRRC Filter (Has ISI)', color='#f87171', edgecolor='#dc2626')
    ax4.bar(x + width/2, np.abs(cascade_samples), width, label='Cascaded SRRC*SRRC = RC (Zero ISI)', color='#4ade80', edgecolor='#16a34a')
    
    ax4.set_xticks(x)
    ax4.set_xticklabels([f'$m={m}$' for m in m_indices], fontsize=10, fontweight='bold')
    ax4.set_ylabel(r'Normalized Sample Magnitude $|p(m T_s)|$', fontsize=11, fontweight='bold', color='#1e293b')
    ax4.set_title(r'(d) Sampled Values at Symbol Instants $t = m T_s$' + '\n' +
                  r'Proof: Isolated SRRC fails Nyquist; Cascaded SRRC recovers Zero ISI', fontsize=11.5, fontweight='bold', color='#0f172a')
    ax4.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax4.legend(loc='upper right', framealpha=0.95, edgecolor='#cbd5e1')
    ax4.set_facecolor('#f8fafc')
    
    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, 'fig4_rrc_split_transmitter_receiver_cascade.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


# ==============================================================================
# 6. EXPERIMENTAL MODULE 5: TIMING JITTER & PEAK ISI SENSITIVITY (FIGURE 5)
# ==============================================================================

def generate_figure_5():
    """
    Figure 5: Timing Jitter Sensitivity and Peak ISI vs. Sampling Phase Offset
      - Evaluates Nyquist's Peak Distortion Criterion:
          D_ISI(tau) = sum_{k != 0} |p(k*Ts + tau)| / |p(tau)|
      - Left: Peak ISI vs normalized timing offset tau / Ts in [-0.5, +0.5].
      - Right: Cumulative Peak ISI vs truncation window N under 5% clock error (tau = 0.05 Ts).
        Shows divergence for sinc (harmonic 1/n series) vs. bounded convergence for alpha > 0.
    """
    print("Generating Figure 5: Timing Jitter Sensitivity & Peak ISI...")
    Ts = 1.0
    tau = np.linspace(-0.45, 0.45, 181) * Ts
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    colors = ['#dc2626', '#d97706', '#0284c7', '#16a34a', '#9333ea']
    labels = [r'$\alpha = 0.0$ (Ideal Sinc)', r'$\alpha = 0.25$', r'$\alpha = 0.50$',
              r'$\alpha = 0.75$', r'$\alpha = 1.00$']
    
    N_symbols = 50  # evaluate over +-50 neighboring symbols
    k_indices = np.concatenate([np.arange(-N_symbols, 0), np.arange(1, N_symbols + 1)])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    
    # Subplot 1: Peak ISI vs. Timing Offset
    for alpha, color, label in zip(alphas, colors, labels):
        peak_isi = np.zeros_like(tau)
        for i, t_off in enumerate(tau):
            center_val = np.abs(raised_cosine_pulse(t_off, Ts=Ts, alpha=alpha))
            isi_sum = np.sum(np.abs(raised_cosine_pulse(k_indices * Ts + t_off, Ts=Ts, alpha=alpha)))
            peak_isi[i] = isi_sum / center_val
        
        lw = 2.2 if alpha in [0.0, 0.5, 1.0] else 1.5
        ax1.plot(tau / Ts, peak_isi, label=label, color=color, linewidth=lw)
    
    ax1.set_xlim(-0.45, 0.45)
    ax1.set_ylim(-0.05, 3.5)
    ax1.set_xlabel(r'Normalized Clock Timing Error $\tau / T_s$', fontsize=12, fontweight='bold', color='#1e293b')
    ax1.set_ylabel(r'Peak ISI Distortion $D_{\mathrm{ISI}}(\tau)$', fontsize=12, fontweight='bold', color='#1e293b')
    ax1.set_title(r'(a) Peak Inter-Symbol Interference vs. Clock Phase Offset' + '\n' +
                  r'$D_{\mathrm{ISI}}(\tau) = \frac{1}{|p(\tau)|} \sum_{k \ne 0} |p(k T_s + \tau)|$',
                  fontsize=13, fontweight='bold', color='#0f172a')
    ax1.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax1.legend(loc='upper center', framealpha=0.95, edgecolor='#cbd5e1', fontsize=10)
    ax1.set_facecolor('#f8fafc')
    
    # Subplot 2: Cumulative ISI vs Truncation Window N under 5% Timing Error
    tau_fixed = 0.05 * Ts  # 5% timing offset
    N_range = np.arange(1, 101)
    
    for alpha, color, label in zip(alphas, colors, labels):
        cum_isi = np.zeros(len(N_range))
        center_val = np.abs(raised_cosine_pulse(tau_fixed, Ts=Ts, alpha=alpha))
        for idx, N_curr in enumerate(N_range):
            k_win = np.concatenate([np.arange(-N_curr, 0), np.arange(1, N_curr + 1)])
            cum_isi[idx] = np.sum(np.abs(raised_cosine_pulse(k_win * Ts + tau_fixed, Ts=Ts, alpha=alpha))) / center_val
        
        lw = 2.2 if alpha in [0.0, 0.5, 1.0] else 1.5
        ax2.plot(N_range, cum_isi, label=label, color=color, linewidth=lw)
    
    ax2.set_xlim(1, 100)
    ax2.set_xlabel(r'Truncation Window Radius $N$ [Number of Adjacent Symbols]', fontsize=12, fontweight='bold', color='#1e293b')
    ax2.set_ylabel(r'Cumulative Peak ISI $D_{\mathrm{ISI}}$ at $\tau = 0.05 T_s$', fontsize=12, fontweight='bold', color='#1e293b')
    ax2.set_title(r'(b) Cumulative ISI Growth under 5% Clock Error ($\tau = 0.05 T_s$)' + '\n' +
                  r'Sinc Diverges as $\sum 1/n$; Raised-Cosine Bounded as $\sum 1/n^3 < \infty$',
                  fontsize=13, fontweight='bold', color='#0f172a')
    ax2.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax2.legend(loc='lower right', framealpha=0.95, edgecolor='#cbd5e1', fontsize=10)
    ax2.set_facecolor('#f8fafc')
    
    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, 'fig5_timing_jitter_and_peak_isi_sensitivity.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


# ==============================================================================
# 7. EXPERIMENTAL MODULE 6: EYE DIAGRAM SYNTHESIS ACROSS ROLL-OFF FACTORS (FIGURE 6)
# ==============================================================================

def generate_figure_6():
    """
    Figure 6: High-Density Eye Diagram Comparison across Roll-off Factors
      - 4-panel comparison for alpha = 0.0, 0.25, 0.5, 1.0.
      - Transmits N = 2,000 random bipolar symbols with AWGN channel (SNR = 28 dB).
      - Visual annotations: Eye Opening Height (Noise Margin), Eye Width (Jitter Margin),
        Zero-Crossing Slope, and Boundary Thickness.
    """
    print("Generating Figure 6: High-Density Eye Diagrams across Roll-Off Factors...")
    np.random.seed(42)
    N_symbols = 2000
    bits = np.random.randint(0, 2, N_symbols)
    symbols = 2 * bits - 1.0  # Bipolar {-1, +1}
    
    Ts = 1.0
    sps = 32  # 32 samples per symbol
    snr_db = 28.0
    
    alphas = [0.0, 0.25, 0.5, 1.0]
    titles = [r'(a) $\alpha = 0.0$ (Ideal Sinc - Severe Jitter Sensitivity)',
              r'(b) $\alpha = 0.25$ (Narrow Transition, Moderate Margin)',
              r'(c) $\alpha = 0.50$ (Standard Telecommunication Trade-off)',
              r'(d) $\alpha = 1.00$ (Maximal Eye Opening & Timing Margin)']
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    axes = axes.flatten()
    
    # Pre-generate AWGN
    sig_power = 1.0
    noise_power = sig_power / (10.0 ** (snr_db / 10.0))
    noise_std = np.sqrt(noise_power)
    
    span = 6.0
    t_pulse = np.linspace(-span * Ts, span * Ts, int(2 * span * sps) + 1)
    
    for idx, (alpha, ax, title) in enumerate(zip(alphas, axes, titles)):
        # Generate pulse and upsampled symbol train
        p = raised_cosine_pulse(t_pulse, Ts=Ts, alpha=alpha)
        
        # Upsample symbols
        upsampled = np.zeros(N_symbols * sps)
        upsampled[::sps] = symbols
        
        # Convolve with RC pulse
        tx_waveform = np.convolve(upsampled, p, mode='same')
        # Add AWGN channel noise
        rx_waveform = tx_waveform + np.random.normal(0, noise_std, len(tx_waveform))
        
        # Discard transient edges
        guard = int(span * sps * 2)
        valid_signal = rx_waveform[guard:-guard]
        
        # Segment into 2-symbol traces (2 * sps samples per trace)
        samples_per_trace = 2 * sps
        num_traces = len(valid_signal) // samples_per_trace
        traces = valid_signal[:num_traces * samples_per_trace].reshape((num_traces, samples_per_trace))
        
        t_trace = np.linspace(-1.0, 1.0, samples_per_trace)
        
        # Plot up to 350 traces for high clarity
        max_plot_traces = min(350, num_traces)
        for tr in traces[:max_plot_traces]:
            ax.plot(t_trace, tr, color='#0284c7', alpha=0.15, linewidth=0.9)
        
        # Highlight nominal zero lines and decision boundaries
        ax.axhline(0, color='#64748b', linestyle='--', linewidth=1.0)
        ax.axvline(0, color='#dc2626', linestyle=':', linewidth=1.2, label='Nominal Sampling Instant ($t=0$)')
        ax.axvline(-0.5, color='#94a3b8', linestyle=':', linewidth=0.8)
        ax.axvline(0.5, color='#94a3b8', linestyle=':', linewidth=0.8)
        
        # Annotate Key Diagnostic Features on panel (c)
        if alpha == 0.5:
            # Eye height arrow
            ax.annotate('', xy=(0.0, 0.82), xytext=(0.0, -0.82),
                        arrowprops=dict(arrowstyle='<->', color='#dc2626', lw=2.0))
            ax.text(0.04, 0.0, 'Eye Height\n(Noise Margin)', color='#dc2626', fontweight='bold', fontsize=9.5)
            
            # Eye width arrow
            ax.annotate('', xy=(-0.42, 0.0), xytext=(0.42, 0.0),
                        arrowprops=dict(arrowstyle='<->', color='#16a34a', lw=2.0))
            ax.text(0.0, -0.28, 'Eye Width (Timing Margin)', color='#16a34a', fontweight='bold', fontsize=9.5, ha='center')
        
        ax.set_xlim(-1.0, 1.0)
        ax.set_ylim(-1.8, 1.8)
        ax.set_xlabel(r'Time Relative to Symbol Center $t / T_s$', fontsize=11, fontweight='bold', color='#1e293b')
        ax.set_ylabel(r'Signal Amplitude', fontsize=11, fontweight='bold', color='#1e293b')
        ax.set_title(title, fontsize=11.5, fontweight='bold', color='#0f172a')
        ax.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
        ax.set_facecolor('#f8fafc')
    
    plt.tight_layout()
    out_file = os.path.join(PLOTS_DIR, 'fig6_eye_diagrams_roll_off_comparison.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_file}")


def run_simulation_and_generate_plots():
    """Run all simulation modules and render all 6 publication figures."""
    print("================================================================================")
    print("STARTING EXPERIMENT 07 SIMULATION SUITE: PULSE SHAPING & NYQUIST CRITERION")
    print("================================================================================")
    
    generate_figure_1()
    generate_figure_2()
    generate_figure_3()
    generate_figure_4()
    generate_figure_5()
    generate_figure_6()
    
    print("================================================================================")
    print("EXPERIMENT 07 PLOT GENERATION COMPLETE. ALL 6 FIGURES PERSISTED IN 'plots/'")
    print("================================================================================")


if __name__ == '__main__':
    run_simulation_and_generate_plots()
