# Experiment 05: Differential PCM (DPCM), Delta Modulation (DM) & Adaptive Delta Modulation (ADM)

**Department of Electronics and Communication Engineering**  
**Cooch Behar Government Engineering College**  
**Course:** Software-Based Digital Communication Laboratory (EC593 / EC592)  
**Student Name:** Apurba Maity | **Roll No.:** 34900324001 | **Semester:** 5th Sem ECE  

---

## 1. Overview
This module implements first-principles mathematical modeling and computational simulation of differential waveform coding systems:
- **DPCM:** Linear prediction ($p=1, 2$), prediction residual quantization, and prediction gain ($G_p \approx 7.2\,\mathrm{dB}$).
- **Linear Delta Modulation (DM):** 1-bit comparator and accumulator, slope overload distortion condition ($\Delta \ge \frac{2\pi f_m A_m}{f_s}$), and granular noise ($N_g = \frac{\Delta^2}{3}$).
- **Adaptive Delta Modulation (ADM):** Jayant/Song step-size multiplier algorithm ($K_e = 1.5$, $K_c = 0.66$).
- **Reconstruction Filtering:** 4th-order Butterworth low-pass filter and $+9\,\mathrm{dB/octave}$ SNR scaling with oversampling ratio ($OSR$).

---

## 2. Directory Artifacts

| File | Description |
| :--- | :--- |
| [`experiment_05.py`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/experiment_05.py) | Standalone Python simulation generating 6 publication-grade figures (300 DPI). |
| [`Experiment_05_Lab_Report.ipynb`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/Experiment_05_Lab_Report.ipynb) | Master Jupyter Notebook report with derivations, code cells, and embedded figures. |
| [`Digital_Comm_Exp5_Study_Guide.pdf`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/Digital_Comm_Exp5_Study_Guide.pdf) | 9-Page Comprehensive Academic Study & Viva-Voce Guide (PDF). |
| [`Digital_Comm_Exp5_Study_Guide.tex`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/Digital_Comm_Exp5_Study_Guide.tex) | Complete LaTeX source code. |
| [`plots/`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/plots/) | High-resolution simulation plots (`fig1` to `fig6`). |

---

## 3. Generated Figures

1. [`fig1_dpcm_architecture_and_prediction_gain.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/plots/fig1_dpcm_architecture_and_prediction_gain.png): DPCM predictor, residual $d[n]$, and reconstruction $\tilde{x}[n]$.
2. [`fig2_dm_slope_overload_vs_granular_noise.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/plots/fig2_dm_slope_overload_vs_granular_noise.png): Slope overload vs. optimal step vs. granular noise.
3. [`fig3_adm_adaptive_tracking.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/plots/fig3_adm_adaptive_tracking.png): Jayant ADM step-size multiplier dynamics.
4. [`fig4_dm_snr_vs_sampling_frequency.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/plots/fig4_dm_snr_vs_sampling_frequency.png): SNR scaling $\propto (f_s)^3$ ($9\,\mathrm{dB/octave}$).
5. [`fig5_sqnr_comparison_pcm_dpcm_dm_adm.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/plots/fig5_sqnr_comparison_pcm_dpcm_dm_adm.png): Comparative SQNR benchmark across bit rates.
6. [`fig6_reconstruction_filtering_and_psd.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation/plots/fig6_reconstruction_filtering_and_psd.png): Frequency-domain noise attenuation by Butterworth LPF.
