# Experiment 10: BPSK, Gray QPSK & Differential PSK (DPSK)

**Subject:** EC592 / EC593 Software-Based Digital Communication Laboratory  
**Institution:** Cooch Behar Government Engineering College  
**Author:** Apurba Maity | Roll No: `34900324001` | 5th Semester ECE  

---

## 1. Overview & Key Objectives
This experiment investigates the mathematics, geometric signal space representations, time-domain simulation, and empirical performance benchmarking of Phase Shift Keying (PSK) systems:
- **Binary Phase Shift Keying (BPSK):** 1-dimensional antipodal signaling ($N = 1$), maximum Euclidean distance $d = 2\sqrt{E_b}$, and bit error probability $P_b = Q\left(\sqrt{\frac{2 E_b}{N_0}}\right)$.
- **Quadrature Phase Shift Keying (QPSK):** 2-dimensional 4-phase signaling ($N = 2$) with dibit symbol grouping ($T_s = 2 T_b$, $E_s = 2 E_b$).
- **The Gray Coding Equivalence Theorem:** Rigorous proof and empirical demonstration that Gray-coded QPSK achieves the **exact same Bit Error Rate as BPSK** ($P_b = Q\left(\sqrt{2 E_b / N_0}\right)$) while **halving required transmission bandwidth** and **doubling spectral efficiency** ($\eta = 2.0\,\mathrm{b/s/Hz}$).
- **Non-Gray QPSK Penalty:** Demonstration that natural binary mapping causes adjacent symbol errors with 2 bit flips, increasing bit error rate by $\approx 1.5\times$.
- **Differential PSK (DPSK):** Differential encoding rule $d_k = b_k \oplus d_{k-1}$ and non-coherent delay-line detection resolving the $180^\circ$ Costas loop phase ambiguity with an SNR penalty of only $0.8\,\mathrm{dB}$ at $10^{-4}$ ($P_b = \frac{1}{2} e^{-E_b / N_0}$).
- **Power Spectral Density & Bandwidth:** Welch FFT PSD estimates proving QPSK's $50\%$ mainlobe compression ($B_{\mathrm{null}} = R_b$ vs. $2 R_b$).
- **Monte Carlo BER Benchmark:** Large-scale empirical verification ($250,000$ bits per SNR point) across $E_b/N_0 \in [0, 11]\,\mathrm{dB}$.

---

## 2. Directory Artifacts

| File / Folder | Purpose & Content |
| :--- | :--- |
| **[`experiment_10.py`](experiment_10.py)** | Master Python physical-layer simulation script; executes Monte Carlo runs and generates all 7 publication-grade figures at 300 DPI. |
| **[`plots/`](plots/)** | Contains all 7 high-resolution figures in PNG format. |
| **[`Experiment_10_Presentation_Script.pdf`](Experiment_10_Presentation_Script.pdf)** | Dedicated **Video Presentation & Defense Script** (5:00–5:30 min) with scene-by-scene delivery, on-screen cues, spoken dialogue, and viva strategies. |
| **[`Digital_Comm_Exp10_Study_Guide.pdf`](Digital_Comm_Exp10_Study_Guide.pdf)** | 11-page Comprehensive Academic Study & Viva Guide Monograph. |
| **[`Experiment_10_Lab_Report.ipynb`](Experiment_10_Lab_Report.ipynb)** | Complete interactive Jupyter Notebook with theory, live Python cells, and visualizers. |
| **[`build_exp10_presentation_script.py`](build_exp10_presentation_script.py)** | Automated compilation script for the Video Presentation Script PDF. |
| **[`build_exp10_study_guide.py`](build_exp10_study_guide.py)** | Automated compilation script for the Academic Study Guide PDF. |
| **[`build_notebook.py`](build_notebook.py)** | Automated builder script for the interactive Jupyter Notebook. |

---

## 3. Generated Figures

1. **`fig1_bpsk_qpsk_dpsk_time_domain_waveforms.png`**: Time-domain bitstream, BPSK $180^\circ$ phase inversions, QPSK 4-phase wave, and DPSK differentially encoded wave.
2. **`fig2_constellations_and_decision_boundaries.png`**: BPSK 1D antipodal constellation ($d = 2\sqrt{E_b}$) and QPSK 2D Gray-coded constellation with constant envelope circle and orthogonal quadrants.
3. **`fig3_qpsk_iq_demodulation_pipeline.png`**: Coherent I/Q receiver multiplier-integrator sampling states recovering even and odd bitstreams without cross-talk.
4. **`fig4_constellation_noise_scatter_evolution.png`**: 4-panel 2D Gaussian scatter clouds across SNR = 3 dB, 7 dB, 12 dB, and 18 dB showing noise margin expansion.
5. **`fig5_dpsk_differential_encoding_decoding_pipeline.png`**: Input bits, differentially encoded bits, received phase differences $\Delta\phi_k$ (canceling carrier phase offset $\phi_0 = 35^\circ$), and error-free recovery without PLL.
6. **`fig6_power_spectral_density_spectral_efficiency.png`**: Welch PSD comparison showing QPSK's $50\%$ narrower mainlobe ($B = R_b$) and double spectral efficiency.
7. **`fig7_monte_carlo_ber_performance_curves.png`**: Master semilog BER benchmark across $E_b/N_0 \in [0, 11]\,\mathrm{dB}$ comparing BPSK, Gray QPSK, Non-Gray QPSK, and DPSK.
