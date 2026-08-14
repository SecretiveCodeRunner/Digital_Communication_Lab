"""
Script to construct Experiment_03_Lab_Report.ipynb with full theoretical writeup, 
LaTeX math, system diagrams, embedded python code, inline figures, and 
a comprehensive Theory vs Practicality (Computational Realities) analysis.
"""

import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

# Cell 1: Header & Student Information
cell1_md = r"""# DIGITAL COMMUNICATION LABORATORY
## Experiment 3 — Sampling, Aliasing and Whittaker-Shannon Sinc Reconstruction

**Student Name:** Apurba Maity  
**Roll Number:** 34900324001  
**Department:** Electronics and Communication Engineering  
**Institution:** Cooch Behar Government Engineering College  
**Course:** Software-Based Digital Communication Laboratory  
**Software Used:** Python 3.14 (NumPy 2.4.6, SciPy 1.18.0, Matplotlib 3.11.1, Pandas 3.0.5)  
**Date:** August 14, 2026  

---
"""

# Cell 2: Objectives & Minimum Theory
cell2_md = r"""### 1. Objectives & Theoretical Formulations

#### 🎯 Experiment Objectives:
1. Empirically verify the **Nyquist-Shannon Sampling Theorem** for bandlimited continuous signals.
2. Implement **ideal Whittaker-Shannon sinc interpolation** from first principles using vectorized matrix operations in Python (without specialized black-box toolboxes).
3. Evaluate three distinct sampling regimes:
   - **Oversampled Regime** ($f_s = 1800\text{ Hz} > 2 f_{\max}$)
   - **Critically Sampled Regime** ($f_s = 600\text{ Hz} = 2 f_{\max}$)
   - **Undersampled Regime** ($f_s = 400\text{ Hz} < 2 f_{\max}$)
4. Quantify time-domain reconstruction errors using **Mean Squared Error (MSE)** and **Root Mean Squared Error (RMSE)**.
5. Mathematically derive and experimentally validate **spectral folding and aliasing** under undersampling.
6. Conduct a deep **Theory vs. Practicality (Computational Realities)** analysis comparing ideal mathematical assumptions with discrete numerical execution.

---

#### 📐 Mathematical Formulations:

1. **Continuous-Time Test Signal:**
   We construct a deterministic two-tone multi-frequency signal:
   $$x(t) = \sin(2\pi f_1 t) + 0.5 \sin(2\pi f_2 t)$$
   where:
   - Fundamental frequency: $f_1 = 100\text{ Hz}$ (Amplitude $A_1 = 1.0\text{ V}$)
   - High-frequency harmonic: $f_2 = 300\text{ Hz}$ (Amplitude $A_2 = 0.5\text{ V}$)
   - Maximum signal bandwidth: $f_{\max} = f_2 = 300\text{ Hz}$

2. **Nyquist-Shannon Sampling Criterion:**
   To reconstruct $x(t)$ without loss of information, the sampling rate $f_s$ must satisfy:
   $$f_s \ge 2 f_{\max} = f_{\text{Nyquist}} = 2 \times 300\text{ Hz} = 600\text{ Hz}$$
   The corresponding sampling interval is $T_s = \frac{1}{f_s}$, yielding discrete sample sequence $x[n] = x(n T_s)$.

3. **Whittaker-Shannon Sinc Interpolation Formula:**
   The continuous signal is reconstructed by passing the sampled sequence through an ideal continuous brick-wall low-pass filter with cutoff $f_c = f_s / 2$, whose impulse response is $h(t) = \operatorname{sinc}(f_s t)$:
   $$\hat{x}(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \operatorname{sinc}\left( \frac{t - n T_s}{T_s} \right) = \sum_{n=-\infty}^{\infty} x[n] \cdot \operatorname{sinc}\left(f_s (t - n T_s)\right)$$
   where $\operatorname{sinc}(u) = \frac{\sin(\pi u)}{\pi u}$ for $u \neq 0$, and $\operatorname{sinc}(0) = 1$.

4. **Spectral Aliasing & Frequency Folding Derivation:**
   When sampled at rate $f_s$, any continuous spectral component $f$ generates periodic replicas at $f \pm k f_s$ for integer $k$.
   When undersampled at $f_s = 400\text{ Hz}$ ($f_s < f_{\text{Nyquist}} = 600\text{ Hz}$):
   - **Component 1 ($f_1 = 100\text{ Hz}$):** $\frac{f_1}{f_s} = \frac{100}{400} = 0.25 \le 0.5 \implies f_{1,\text{alias}} = 100\text{ Hz}$ (Preserved).
   - **Component 2 ($f_2 = 300\text{ Hz}$):** $\frac{f_2}{f_s} = \frac{300}{400} = 0.75 > 0.5$ (Exceeds Nyquist boundary $f_s/2 = 200\text{ Hz}$).
   - The aliased frequency folded back into the principal Nyquist zone $[0, f_s/2]$ is:
     $$f_{2,\text{alias}} = |f_2 - k \cdot f_s| = |300 - 1 \times 400| = |-100| = 100\text{ Hz}$$
   - **Theoretical Outcome:** The $300\text{ Hz}$ tone folds directly on top of the $100\text{ Hz}$ tone, corrupting the original signal.
"""

# Cell 3: Flowchart
cell3_md = r"""### 2. DSP Architecture & Simulation Flowchart

```mermaid
graph TD
    A["Continuous Signal x(t) = sin(2π·100t) + 0.5·sin(2π·300t)"] --> B["Discretize at Sampling Frequency fs"]
    
    B --> C1["Case 1: Oversampling (fs = 1800 Hz)"]
    B --> C2["Case 2: Critical Nyquist (fs = 600 Hz)"]
    B --> C3["Case 3: Undersampling (fs = 400 Hz)"]
    
    C1 --> D1["Vectorized Sinc Matrix Interpolation"]
    C2 --> D2["Vectorized Sinc Matrix Interpolation"]
    C3 --> D3["Vectorized Sinc Matrix Interpolation"]
    
    D1 --> E1["Error Calculation e(t) = x(t) - x_hat(t)"]
    D2 --> E2["Error Calculation e(t) = x(t) - x_hat(t)"]
    D3 --> E3["Error Calculation e(t) = x(t) - x_hat(t)"]
    
    E1 --> F["Compute Real FFT Spectra (rfft)"]
    E2 --> F
    E3 --> F
    
    F --> G["Plot Figures & Tabulate Metrics (MSE, RMSE, Max Error)"]
```
"""

# Cell 4: Python Code
cell4_code = r"""import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

# Execute modular experiment script
import experiment_03
experiment_03.run_experiment_3()
"""

# Cell 5: Figures
cell5_md = r"""### 3. Experimental Figures & Comprehensive Plot Analysis

#### Figure 1: Reference Continuous Signal vs. Sampled Discrete Stems
![Sampled Discrete Stems](plots/exp3_sampled_signals.png)

* **Analysis:**
  - **Oversampled ($1800\text{ Hz}$):** 91 discrete points across $50\text{ ms}$ provide dense sampling ($6$ samples per cycle of $300\text{ Hz}$), clearly tracing the envelope.
  - **Critically Sampled ($600\text{ Hz}$):** 31 points capture exactly 2 samples per cycle of the $300\text{ Hz}$ component.
  - **Undersampled ($400\text{ Hz}$):** Only 21 points are recorded ($1.33$ samples per cycle of $300\text{ Hz}$), failing to capture the underlying sinusoidal variations.

---

#### Figure 2: Original Reference vs. Sinc Reconstructed Waveforms
![Reconstructed Waveforms](plots/exp3_reconstructed_waveforms.png)

* **Analysis:**
  - **Oversampled ($1800\text{ Hz}$):** The dashed green reconstructed curve $\hat{x}(t)$ overlays the solid black reference signal $x(t)$ with near-zero error.
  - **Critically Sampled ($600\text{ Hz}$):** Because the $300\text{ Hz}$ sine wave samples fall on zero-crossings ($\sin(n\pi)=0$), the sinc sum only recovers the $100\text{ Hz}$ fundamental, resulting in envelope flattening.
  - **Undersampled ($400\text{ Hz}$):** Severe distortion occurs as the aliased $300\text{ Hz}$ tone superimposes constructively/destructively on the $100\text{ Hz}$ tone.

---

#### Figure 3: Single-Sided Magnitude Spectra (Original vs. Reconstructed FFTs)
![Magnitude Spectra](plots/exp3_magnitude_spectra.png)

* **Analysis:**
  - **Original Spectrum:** Shows exact peaks at $f_1 = 100\text{ Hz}$ (magnitude $1.0$) and $f_2 = 300\text{ Hz}$ (magnitude $0.5$).
  - **Oversampled Spectrum ($1800\text{ Hz}$):** Perfectly reproduces both $100\text{ Hz}$ and $300\text{ Hz}$ spectral lines within the $[0, 900\text{ Hz}]$ Nyquist band.
  - **Undersampled Spectrum ($400\text{ Hz}$):** The $300\text{ Hz}$ peak completely disappears. It folds across the $f_s/2 = 200\text{ Hz}$ Nyquist folding frequency directly to $|300 - 400| = 100\text{ Hz}$, merging into the $100\text{ Hz}$ spectral line!

---

#### Figure 4: Time-Domain Reconstruction Error Waveforms
![Reconstruction Error Waveforms](plots/exp3_reconstruction_error.png)

* **Analysis:**
  - **Oversampled ($1800\text{ Hz}$):** Residual error is flat with $\text{MSE} = 5.0 \times 10^{-6}\text{ V}^2$.
  - **Critically Sampled ($600\text{ Hz}$):** Pure sinusoidal error with $\text{MSE} \approx 0.1235\text{ V}^2$, corresponding to the uncaptured $0.5\sin(2\pi \cdot 300 t)$ component ($\frac{A_2^2}{2} = \frac{0.5^2}{2} = 0.125\text{ V}^2$).
  - **Undersampled ($400\text{ Hz}$):** Massive time-varying error waveform with $\text{MSE} \approx 0.25\text{ V}^2$.
"""

# Cell 6: Theory vs Practicality
cell6_md = r"""### 4. 🌟 Theory vs. Practicality (Computational Realities)

A critical outcome of this experiment is recognizing where **ideal mathematical theory** diverges from **real-world numerical computation and practical hardware**:

| Aspect | Theoretical Assumption | Computational / Practical Reality | Resolution in Code & Engineering |
| :--- | :--- | :--- | :--- |
| **1. Critical Sampling ($f_s = 2f_{\max}$)** | Theory states $f_s = 2f_{\max}$ guarantees complete signal recovery. | When sampling a pure sine wave $\sin(2\pi f_0 t)$ at $t_n = n/(2f_0)$, all sample points evaluate to $\sin(n\pi) \equiv 0$. The tone vanishes completely ($\text{MSE} = 0.125$). | In practical DSP/ADC design, strict oversampling ($f_s \ge 2.2 f_{\max}$) is mandatory to avoid phase nulling. |
| **2. Whittaker-Shannon Summation** | Sinc interpolation requires an infinite summation from $n = -\infty$ to $+\infty$. | Digital computers and real-time processors only capture finite observation windows ($T = 50\text{ ms}$). Truncating the sinc series introduces boundary ripples. | Extended sample padding ($N_{\text{pad}} = 20$) was implemented in `experiment_03.py` to eliminate edge distortion. |
| **3. Spectral Spikes (FFT)** | Continuous Fourier Transform yields infinitely sharp Dirac deltas $\delta(f - f_0)$. | Discrete FFT on finite-duration signals acts as a rectangular window $w(t)$, causing spectral leakage (sinc-shaped sidelobes and finite bin width). | Use sufficient record length ($T = 50\text{ ms}$) and higher zero-padded FFT resolution. |
| **4. Anti-Aliasing Filtering** | Mathematical formulas can track and predict folded frequencies ($|f - k f_s|$). | In real ADC hardware, once an out-of-band high-frequency signal aliases into baseband, it is mathematically inseparable from true data. | Physical hardware requires an analog **Anti-Aliasing Low-Pass Filter (AAF)** *before* the ADC. |

---

### 5. Summary Results Table & Quantitative Validation

| Sampling Case | Sampling Rate ($f_s$) | Ratio ($f_s / f_{\text{Nyquist}}$) | Sample Points | MSE ($\text{V}^2$) | RMSE ($\text{V}$) | Max Abs Error ($\text{V}$) | Expected $f_2$ Alias | Observed $f_2$ Peak |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Oversampled** | $1800\text{ Hz}$ | $3.0\times$ | 91 | $5.0 \times 10^{-6}$ | $0.0022$ | $0.0071$ | $300\text{ Hz}$ | $300\text{ Hz}$ (Clean) |
| **Critically Sampled** | $600\text{ Hz}$ | $1.0\times$ | 31 | $0.1235$ | $0.3514$ | $0.5003$ | $300\text{ Hz}$ | $0\text{ Hz}$ (Phase Null) |
| **Undersampled** | $400\text{ Hz}$ | $0.67\times$ | 21 | $0.2500$ | $0.5000$ | $0.7750$ | $100\text{ Hz}$ | **$100\text{ Hz}$ (Aliased!)** |

---

### 6. Final Conclusions
1. The **Nyquist-Shannon Sampling Theorem** was successfully validated. Reconstructing signals sampled at $f_s \ge 2f_{\max}$ is mathematically exact when phase alignment and infinite support conditions are met.
2. Sinc interpolation implemented from first principles via vectorized matrix products matches theoretical continuous curves with near-zero error ($\text{MSE} < 10^{-5}$) under oversampling.
3. Undersampling at $f_s = 400\text{ Hz}$ caused the $300\text{ Hz}$ tone to fold exactly back to $|300 - 400| = 100\text{ Hz}$, confirming the spectral aliasing equation.
4. Real-world computational considerations (phase sensitivity at $2f_{\max}$, finite-window sinc truncation, FFT spectral leakage) were empirically identified and explained.
"""

nb.cells = [
    nbf.v4.new_markdown_cell(cell1_md),
    nbf.v4.new_markdown_cell(cell2_md),
    nbf.v4.new_markdown_cell(cell3_md),
    nbf.v4.new_code_cell(cell4_code),
    nbf.v4.new_markdown_cell(cell5_md),
    nbf.v4.new_markdown_cell(cell6_md)
]

nb_path = "/home/apurba/Projects/Digital_Communication_Lab/Experiment_03_Sampling_Aliasing_and_Reconstruction/Experiment_03_Lab_Report.ipynb"
with open(nb_path, 'w') as f:
    nbf.write(nb, f)

print("Successfully generated updated Jupyter Notebook:", nb_path)
