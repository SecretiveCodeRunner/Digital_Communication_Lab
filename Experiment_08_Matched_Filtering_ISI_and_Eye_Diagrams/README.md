# Experiment 08: Optimum Receiver Detection, Matched Filtering, Channel ISI & Eye Diagrams

**Department of Electronics and Communication Engineering**  
**Cooch Behar Government Engineering College**  
**Course:** Software-Based Digital Communication Laboratory (EC592)  
**Student Name:** Apurba Maity | **Roll No.:** 34900324001 | **Semester:** 5th Sem ECE  

---

## 1. Overview
This laboratory module implements from first principles in Python (NumPy, SciPy, Matplotlib) the complete analytical, simulation, and diagnostic framework for optimum baseband signal detection in Additive White Gaussian Noise (AWGN):

- **The Matched Filter Theorem:**
  - Formulated the receiver detection problem for signals corrupted by AWGN ($S_n(f) = N_0/2$).
  - Derived the optimum filter transfer function $H_{\mathrm{opt}}(f) = k S^*(f) e^{-j 2\pi f T}$ and causal impulse response $h_{\mathrm{opt}}(t) = k s(T - t)$ via the Cauchy-Schwarz inequality.
  - Proved that the matched filter maximizes the instantaneous peak signal-to-noise ratio at the decision instant $t = T$.
- **The Energy Invariance Theorem:**
  - Proved analytically and verified numerically that $\mathrm{SNR}_{\max} = \frac{2E}{N_0}$.
  - Demonstrated that the maximum attainable output SNR depends strictly on pulse energy $E$ and noise spectral density $N_0/2$, remaining **completely invariant to the physical pulse waveshape**.
- **Deterministic Autocorrelation Equivalence:**
  - Proved that the continuous output of the matched filter is the deterministic autocorrelation function of the transmitted waveform: $s_o(t) = R_{ss}(t - T)$.
  - Verified that $s_o(T) = R_{ss}(0) = E$, attaining the global peak at zero lag.
- **Correlator vs. Matched Filter Equivalence:**
  - Demonstrated the mathematical identity between the passive LTI matched filter convolution and the active multiplier-integrator correlator $\int_0^T r(t) s(t) dt$ at sampling instant $t = T$.
  - Contrasted continuous running convolution with active integrate-and-dump reset cycles.
- **Analysis Across Diverse Canonical Pulse Geometries:**
  - Implemented unit-energy ($E = 1.0$) Rectangular, Half-Sine, Triangular, and Truncated Raised-Cosine pulses.
  - Verified that all four geometries yield identical peak output $y(T) = 1.000$ and identical maximum instantaneous SNR.
- **Sampling Clock Phase Error & Jitter Sensitivity:**
  - Quantified signal amplitude degradation and SNR penalty across normalized timing offsets $\Delta t / T \in [-0.5, 0.5]$.
  - Contrasted the steep linear falloff of rectangular pulses ($1 - |\Delta t|/T$, losing $1.0\,\mathrm{dB}$ at $\Delta t = 0.11 T$) with the smooth quadratic curvature of half-sine and raised-cosine pulses ($\Delta t^2$, losing $< 0.22\,\mathrm{dB}$ at $\Delta t = 0.10 T$).
- **Channel Dispersion, Bandwidth Limitation & Inter-Symbol Interference (ISI):**
  - Modeled band-limited channels via 2nd-order Butterworth filters across cutoffs $f_c / R_s \in \{0.4, 0.75, 1.5\}$.
  - Evaluated temporal pulse broadening, composite link impulse responses $g(t) = s(t) * h_c(t) * h(t)$, and Nyquist Peak Distortion $D_{\mathrm{ISI}}$.
- **High-Density Eye Diagram Telemetry:**
  - Synthesized eye diagrams ($N = 1,500$ symbols) across 4 scenarios: Ideal Matched Filter, Dispersive Channel, Sub-optimal RC Low-Pass Filter ($B \cdot T = 0.5$), and Severe Timing Jitter ($\sigma_\tau = 0.12 T$).
  - Extracted quantitative telemetry: Vertical Eye Height (Noise Margin $\approx 96\%$), Horizontal Eye Width (Timing Jitter Margin), and eye closure percentage ($42\%$).
- **Comprehensive Monte Carlo Bit Error Rate (BER) Simulation:**
  - Transmitted $200,000$ bits per SNR point across $E_b/N_0 \in [0, 10]\,\mathrm{dB}$.
  - Validated that the empirical matched filter achieves exact agreement with the theoretical bound $Q\left(\sqrt{2 E_b / N_0}\right)$.
  - Quantified exact SNR penalties: **$1.2\,\mathrm{dB}$ loss** for sub-optimal RC filter ($B \cdot T = 0.5$) at $P_e = 10^{-3}$, and **$1.7\,\mathrm{dB}$ loss** for clock jitter ($\Delta t = 0.18 T$) at $P_e = 10^{-4}$.

---

## 2. Directory Artifacts

| File | Description |
| :--- | :--- |
| [`experiment_08.py`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/experiment_08.py) | Standalone Python simulation script generating all 7 publication-grade figures (300 DPI). |
| [`Experiment_08_Lab_Report.ipynb`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/Experiment_08_Lab_Report.ipynb) | Master interactive Jupyter Notebook report with derivations, executable code cells, and inline figures. |
| [`plots/`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/plots/) | High-resolution simulation plots (`fig1` to `fig7`) rendered at 300 DPI. |

---

## 3. Generated Figures

1. [`fig1_matched_filter_impulse_response_and_convolution.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/plots/fig1_matched_filter_impulse_response_and_convolution.png): Transmitted pulse $s(t)$, time-reversed impulse response $h(t) = s(T-t)$, AWGN-corrupted input $r(t)$, and continuous convolution output $y(t) = R_{ss}(t - T)$ peaking at $t = T$.
2. [`fig2_matched_filtering_diverse_pulse_shapes.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/plots/fig2_matched_filtering_diverse_pulse_shapes.png): Four-pulse comparison (Rectangular, Half-Sine, Triangular, Raised-Cosine) verifying the Energy Invariance Theorem ($\mathrm{SNR}_{\max} = \frac{2E}{N_0}$ at $t = T$).
3. [`fig3_correlator_vs_matched_filter_equivalence.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/plots/fig3_correlator_vs_matched_filter_equivalence.png): Three-panel time evolution proving dynamic equivalence between LTI matched filter convolution and active correlator integrate-and-dump cycles.
4. [`fig4_timing_offset_and_snr_sensitivity.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/plots/fig4_timing_offset_and_snr_sensitivity.png): Decision variable normalized amplitude and SNR penalty (dB loss) vs. clock timing offset $\Delta t / T$, highlighting sharp linear cusp vs. smooth quadratic curvature.
5. [`fig5_channel_dispersion_and_isi_broadening.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/plots/fig5_channel_dispersion_and_isi_broadening.png): Butterworth channel frequency responses ($f_c / R_s \in \{0.4, 0.75, 1.5\}$), dispersed pulses $p(t)$, and composite link responses $g(t)$ exhibiting residual ISI tails.
6. [`fig6_eye_diagrams_matched_vs_suboptimal_comparison.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/plots/fig6_eye_diagrams_matched_vs_suboptimal_comparison.png): Four-panel high-density eye diagram comparison under AWGN ($\mathrm{SNR} = 25\,\mathrm{dB}$) displaying Noise Margin, Jitter Margin, and eye closure percentage.
7. [`fig7_monte_carlo_ber_performance_curves.png`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_08_Matched_Filtering_ISI_and_Eye_Diagrams/plots/fig7_monte_carlo_ber_performance_curves.png): Semi-log BER vs $E_b/N_0$ curves ($N = 200,000$ bits) validating theoretical $Q\left(\sqrt{2 E_b / N_0}\right)$ and quantifying SNR penalties for sub-optimal RC filters and clock jitter.
