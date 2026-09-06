# Experiment 06: Digital Line Coding Schemes & Power Spectral Density (PSD) Analysis

**Department of Electronics and Communication Engineering**  
**Cooch Behar Government Engineering College**  
**Course:** Software-Based Digital Communication Laboratory (EC593 / EC592)  
**Student Name:** Apurba Maity | **Roll No.:** 34900324001 | **Semester:** 5th Sem ECE  

---

## 1. Overview
This module implements first-principles mathematical modeling, spectral analysis, and transient simulation of baseband digital line codes:
- **Encoders:** Unipolar NRZ/RZ, Polar NRZ/RZ, Bipolar AMI, Split-Phase / Manchester (IEEE 802.3), and Differential Manchester.
- **Spectral Theory:** Closed-form PSD derivation via Wiener-Khinchin theorem for cyclostationary pulse trains.
- **Validation:** Monte Carlo numerical spectral estimation (Welch periodogram over $65,536$ bits) showing flawless convergence against analytical curves.
- **Channel Degradation:** AC coupling / transformer isolation demonstrating baseline wandering on Unipolar NRZ vs. perfect DC balance on Bipolar AMI and Manchester.
- **Clock Recovery:** Extraction of bit timing clock ($f_0 = R_b$) via non-linear squaring and high-$Q$ bandpass filtering.
- **Eye Diagrams:** Evaluation of noise margins, timing jitter sensitivity, and Inter-Symbol Interference (ISI).

---

## 2. Directory Artifacts

| File | Description |
| :--- | :--- |
| [`experiment_06.py`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/experiment_06.py) | Standalone Python simulation generating 6 publication-grade figures (300 DPI). |
| [`Experiment_06_Lab_Report.ipynb`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/Experiment_06_Lab_Report.ipynb) | Master Jupyter Notebook report with derivations, code cells, and embedded figures. |
| [`Digital_Comm_Exp6_Study_Guide.pdf`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/Digital_Comm_Exp6_Study_Guide.pdf) | 9-Page Comprehensive Academic Study & Viva-Voce Guide (PDF). |
| [`Digital_Comm_Exp6_Study_Guide.tex`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/Digital_Comm_Exp6_Study_Guide.tex) | Complete LaTeX source code. |
| [`plots/`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/plots/) | High-resolution simulation plots (`fig1` to `fig6`). |

---

## 3. Generated Figures

1. [`fig1_line_coding_time_domain_waveforms.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/plots/fig1_line_coding_time_domain_waveforms.png): Synchronized multi-panel plot of 6 line codes over 16-bit test stream.
2. [`fig2_theoretical_psd_master_comparison.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/plots/fig2_theoretical_psd_master_comparison.png): Linear and semi-log analytical PSD curves.
3. [`fig3_empirical_vs_theoretical_psd_validation.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/plots/fig3_empirical_vs_theoretical_psd_validation.png): Welch FFT spectrum ($65,536$ bits) vs. analytical curves.
4. [`fig4_baseline_wander_ac_coupling_transient.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/plots/fig4_baseline_wander_ac_coupling_transient.png): AC-coupling transient response and DC baseline droop.
5. [`fig5_clock_recovery_spectral_line_extraction.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/plots/fig5_clock_recovery_spectral_line_extraction.png): Clock extraction via squarer and bandpass filter.
6. [`fig6_eye_diagram_and_noise_margin_analysis.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD/plots/fig6_eye_diagram_and_noise_margin_analysis.png): Eye diagram noise margins for Polar NRZ vs. Manchester.
