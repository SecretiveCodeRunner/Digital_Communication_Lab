# Experiment 09: Binary ASK & BFSK Modulation and Demodulation

**Subject:** EC592 / EC593 Software-Based Digital Communication Laboratory  
**Institution:** Cooch Behar Government Engineering College  
**Author:** Apurba Maity | Roll No: `34900324001` | 5th Semester ECE  

---

## 1. Overview & Key Objectives
This experiment investigates the theory, signal space geometry, time-domain simulation, and empirical performance benchmarking of bandpass binary digital modulation:
- **Binary Amplitude Shift Keying (BASK / OOK):** 1-dimensional signal space ($N = 1$), optimum decision threshold $\gamma = \sqrt{E_b/2}$, and coherent error probability $P_e = Q\left(\sqrt{\frac{E_b}{2 N_0}}\right)$.
- **Binary Frequency Shift Keying (BFSK):** 2-dimensional orthogonal signal space ($N = 2$), Euclidean distance $d = \sqrt{2 E_b}$, and coherent error probability $P_e = Q\left(\sqrt{\frac{E_b}{N_0}}\right)$.
- **Orthogonality Conditions:** Derivation of cross-correlation $\rho = \mathrm{sinc}(2 \Delta f T_b)$, minimum coherent spacing $\Delta f = \frac{R_b}{2}$ (MSK), and non-coherent spacing $\Delta f = R_b$ (Sunde's BFSK).
- **Non-Coherent Detection:** Envelope detection without carrier phase synchronization, governed by Rayleigh distribution (noise only) and Rician distribution (signal + noise).
- **Power Spectral Density & Bandwidth:** Sinc squared lobes, carrier delta spikes, and Carson's rule bandwidth.
- **Monte Carlo BER Benchmark:** High-precision simulation ($200,000$ bits per SNR point) verifying closed-form limits and quantifying the $3\,\mathrm{dB}$ penalty of BFSK and $6\,\mathrm{dB}$ penalty of BASK relative to BPSK.

---

## 2. Directory Artifacts

| File / Folder | Purpose & Content |
| :--- | :--- |
| **[`experiment_09.py`](experiment_09.py)** | Master Python physical-layer simulation script; executes Monte Carlo runs and generates all 7 publication-grade figures at 300 DPI. |
| **[`plots/`](plots/)** | Contains all 7 high-resolution figures in PNG format. |
| **[`Experiment_09_Presentation_Script.pdf`](Experiment_09_Presentation_Script.pdf)** | Dedicated **Video Presentation & Defense Script** (5:00–5:30 min) with scene-by-scene delivery, on-screen cues, spoken dialogue, and viva strategies. |
| **[`Digital_Comm_Exp9_Study_Guide.pdf`](Digital_Comm_Exp9_Study_Guide.pdf)** | 11-page Comprehensive Academic Study & Viva Guide Monograph. |
| **[`Experiment_09_Lab_Report.ipynb`](Experiment_09_Lab_Report.ipynb)** | Complete interactive Jupyter Notebook with theory, live Python cells, and visualizers. |
| **[`build_exp09_presentation_script.py`](build_exp09_presentation_script.py)** | Automated compilation script for the Video Presentation Script PDF. |
| **[`build_exp09_study_guide.py`](build_exp09_study_guide.py)** | Automated compilation script for the Academic Study Guide PDF. |
| **[`build_notebook.py`](build_notebook.py)** | Automated builder script for the interactive Jupyter Notebook. |

---

## 3. Generated Figures

1. **`fig1_bask_bfsk_time_domain_waveforms.png`**: Time-domain bitstream, dual carrier tones, BASK envelope switching, and continuous-phase BFSK transitions.
2. **`fig2_signal_space_and_constellation.png`**: 1D BASK constellation with decision threshold and 2D BFSK orthogonal constellation with Euclidean distance $d = \sqrt{2 E_b}$ and decision regions.
3. **`fig3_coherent_vs_noncoherent_demod_pipeline.png`**: Internal waveforms for coherent correlators, envelope detectors, and BFSK difference decision statistic $d(t) = y_2(t) - y_1(t)$.
4. **`fig4_bfsk_orthogonality_vs_frequency_separation.png`**: Cross-correlation $\rho$ vs. normalized tone spacing $\Delta f \cdot T_b$, demonstrating MSK ($0.5$), Sunde's ($1.0$), and lab ($2.0$) orthogonality.
5. **`fig5_power_spectral_density_comparison.png`**: Welch PSD estimates vs. theoretical sinc and Carson bandwidth bounds.
6. **`fig6_envelope_detection_rician_rayleigh_distributions.png`**: Envelope probability distributions (Rayleigh for space, Rician for mark) with optimal slicing threshold.
7. **`fig7_monte_carlo_ber_performance_curves.png`**: Large-scale Monte Carlo BER benchmark across $E_b/N_0 \in [0, 12]\,\mathrm{dB}$ validating all theoretical curves.
