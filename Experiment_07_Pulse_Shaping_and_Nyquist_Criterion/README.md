# Experiment 07: Pulse Shaping, Nyquist Criterion for Zero ISI, Raised-Cosine & SRRC Filtering

**Department of Electronics and Communication Engineering**  
**Cooch Behar Government Engineering College**  
**Course:** Software-Based Digital Communication Laboratory (EC592)  
**Student Name:** Apurba Maity | **Roll No.:** 34900324001 | **Semester:** 5th Sem ECE  

---

## 1. Overview
This module implements first-principles mathematical modeling, spectral analysis, and transient simulation of baseband Nyquist pulse shaping filters:
- **Nyquist First Criterion:** Formulated in both time ($g(m T_s) = \delta[m]$) and frequency ($\sum G(f - k R_s) = \text{const}$) domains for zero Inter-Symbol Interference (ISI).
- **The Sinc Fallacy:** Proved why the ideal sinc pulse ($B_0 = R_s / 2$) fails in physical hardware due to non-causality and $1/t$ harmonic divergence under clock jitter ($\sum 1/n \to \infty$).
- **Raised-Cosine (RC) Filter Family:** Parametric pulse generator across roll-off factors $\alpha \in [0, 1]$ providing $B = \frac{R_s}{2}(1 + \alpha)$, $1/t^3$ accelerated tail decay, and absolute convergence of ISI under timing errors ($\sum 1/n^3 < \infty$).
- **Square-Root Raised-Cosine (SRRC / RRC) Matched Filter Partitioning:**
  - Evaluated the joint requirement of zero ISI and maximized SNR in AWGN ($H_{\mathrm{tx}}(f) = H_{\mathrm{rx}}(f) = \sqrt{P_{\mathrm{RC}}(f)}$).
  - Mathematically demonstrated that an isolated SRRC pulse exhibits significant ISI ($|h(T_s)| \approx 0.18$).
  - Confirmed via numerical convolution that the cascade $h_{\mathrm{tx}}(t) * h_{\mathrm{rx}}(t)$ reproduces the full Raised-Cosine characteristic with residual error $< 2.5 \times 10^{-5}$.
- **Timing Jitter & Peak Distortion:** Evaluated Nyquist's Peak Distortion Criterion $D_{\mathrm{ISI}}(\tau)$, proving divergence for Sinc vs. bounded stability for Raised-Cosine.
- **Eye Diagram Diagnostics:** Synthesized synchronized 4-panel eye diagrams ($N = 2,000$ symbols, AWGN $\mathrm{SNR} = 28\,\mathrm{dB}$) extracting vertical eye height (noise margin) and horizontal eye width (jitter margin).

---

## 2. Directory Artifacts

| File | Description |
| :--- | :--- |
| [`experiment_07.py`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/experiment_07.py) | Standalone Python simulation script generating all 6 publication-grade figures (300 DPI). |
| [`Experiment_07_Lab_Report.ipynb`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/Experiment_07_Lab_Report.ipynb) | Master interactive Jupyter Notebook report with derivations, code cells, and inline plots. |
| [`plots/`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/plots/) | High-resolution simulation plots (`fig1` to `fig6`) at 300 DPI. |

---

## 3. Generated Figures

1. [`fig1_nyquist_pulse_shapes_time_domain.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/plots/fig1_nyquist_pulse_shapes_time_domain.png): Time-domain Raised-Cosine waveforms ($p(m T_s) = \delta[m]$) and semi-log side-lobe decay ($1/t$ vs. $1/t^3$).
2. [`fig2_raised_cosine_frequency_spectra.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/plots/fig2_raised_cosine_frequency_spectra.png): Linear and logarithmic frequency spectra illustrating vestigial symmetry around $(B_0, 0.5)$ and excess bandwidth $B = B_0(1+\alpha)$.
3. [`fig3_multi_symbol_transmission_and_zero_isi.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/plots/fig3_multi_symbol_transmission_and_zero_isi.png): Multi-symbol superposition showing overlapping pulses passing through zero at sampling instants.
4. [`fig4_rrc_split_transmitter_receiver_cascade.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/plots/fig4_rrc_split_transmitter_receiver_cascade.png): Transmitter RRC, Receiver Matched RRC, and cascaded convolution reproducing full Raised-Cosine (residual error $< 2.5 \times 10^{-5}$).
5. [`fig5_timing_jitter_and_peak_isi_sensitivity.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/plots/fig5_timing_jitter_and_peak_isi_sensitivity.png): Peak ISI $D_{\mathrm{ISI}}(\tau)$ vs. sampling phase error and cumulative error growth under $5\%$ clock jitter.
6. [`fig6_eye_diagrams_roll_off_comparison.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_07_Pulse_Shaping_and_Nyquist_Criterion/plots/fig6_eye_diagrams_roll_off_comparison.png): High-density eye diagram comparison across $\alpha \in \{0.0, 0.25, 0.5, 1.0\}$ under AWGN with annotated noise margin and timing margin.
