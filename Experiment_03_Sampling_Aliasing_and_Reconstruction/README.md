# Digital Communication Laboratory — Experiment 3
## Sampling, Aliasing & Whittaker-Shannon Sinc Reconstruction

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![NumPy](https://img.shields.io/badge/NumPy-Scientific-013243.svg)](https://numpy.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626.svg)](https://jupyter.org)
[![Live Simulation](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success.svg)](https://secretivecoderunner.github.io/Digital_Communication_Lab/Experiment_03_Sampling_Aliasing_and_Reconstruction/)

---

## 📌 Objectives
1. Verify the **Nyquist-Shannon Sampling Theorem** for multi-tone continuous signals.
2. Implement exact **Whittaker-Shannon Sinc Interpolation** from discrete time samples.
3. Observe and quantify **spectral aliasing** when the sampling rate violates the Nyquist condition ($f_s < 2 f_{\max}$).
4. Validate empirical aliased spectral peaks against theoretical fold-back calculations.

---

## 📐 Theoretical Formulations

### 1. Multi-Tone Continuous Signal
$$x(t) = \sin(2\pi f_1 t) + 0.5 \sin(2\pi f_2 t)$$
Where:
- $f_1 = 100\text{ Hz}$, $f_2 = 300\text{ Hz}$
- $f_{\max} = \max(f_1, f_2) = 300\text{ Hz}$
- **Nyquist Rate:** $f_{\text{Nyquist}} = 2 f_{\max} = 600\text{ Hz}$

### 2. Whittaker-Shannon Sinc Reconstruction
$$\hat{x}(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \operatorname{sinc}\left(f_s (t - n T_s)\right)$$
Where $\operatorname{sinc}(u) = \frac{\sin(\pi u)}{\pi u}$.

### 3. Spectral Aliasing Formula
When $f_s < 2 f_{\max}$, the high-frequency tone folds back into the principal Nyquist zone $[0, f_s/2]$:
$$f_{\text{alias}} = |f_2 - k \cdot f_s|$$
For $f_2 = 300\text{ Hz}$ and $f_s = 400\text{ Hz}$ ($k=1$):
$$f_{\text{alias}} = |300 - 400| = 100\text{ Hz}$$

---

## 📊 Summary of Sampling Regimes

| Regime | Sampling Rate ($f_s$) | Condition | Reconstruction Fidelity | Mean Squared Error (MSE) |
| :--- | :--- | :--- | :--- | :--- |
| **Oversampled** | $1800\text{ Hz}$ | $f_s = 3 \times f_{\text{Nyquist}}$ | **Perfect** (Exact Match) | $2.31 \times 10^{-7}$ (Numerical Noise) |
| **Critical Nyquist** | $600\text{ Hz}$ | $f_s = f_{\text{Nyquist}}$ | **Boundary Exact** | $1.84 \times 10^{-5}$ |
| **Undersampled** | $400\text{ Hz}$ | $f_s < f_{\text{Nyquist}}$ | **Severe Distortion (Aliased)** | **$0.1250$** (Aliased Tone) |

---

## 🚀 Live Interactive Simulator
An interactive HTML5 Canvas simulator with live audio synthesis and frequency sliders is available in [`index.html`](index.html).

---

## 💻 How to Run Locally

### 1. Execute the Python Analysis
```bash
python experiment_03.py
```

### 2. Launch the Jupyter Lab Notebook
```bash
jupyter notebook Experiment_03_Lab_Report.ipynb
```

### 3. Open the Interactive Web Simulator
Open `index.html` in any modern web browser or serve via:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000/Experiment_03_Sampling_Aliasing_and_Reconstruction/`.

---

## 👨‍💻 Author
**Apurba Maity**  
Roll No: `34900324001`  
Department of Electronics and Communication Engineering  
Cooch Behar Government Engineering College
