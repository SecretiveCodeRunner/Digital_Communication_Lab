# Digital Communication Laboratory — Study & Viva Guide
## Experiment 3: Sampling, Aliasing & Whittaker-Shannon Sinc Reconstruction

**Student Name:** Apurba Maity  
**Roll Number:** 34900324001  
**Target:** Beginners in Python & Digital Signal Processing (DSP)  

---

## SECTION 1: Python & DSP Libraries Explained Simply

If you don't know Python yet, don't worry! In Digital Communication, Python replaces expensive hardware equipment (like Oscilloscopes, Function Generators, and Spectrum Analyzers) with software functions.

Here are the 4 core libraries we use and why:

### 1. NumPy (`import numpy as np`)
- **What it is:** The "Number Crunching Engine".
- **Why we need it:** Standard Python is too slow for processing signals with millions of numbers. NumPy creates **n-dimensional arrays** (vectors of numbers stored contiguously in memory) and performs instant operations on all of them at once (**Vectorization**).
- **Key Functions Used:**
  - `np.linspace(start, stop, num)`: Generates evenly spaced time points (like generating a smooth time axis $t = 0$ to $0.05$ seconds with 10,000 points).
  - `np.sin()`: Calculates the sine of every angle in an array.
  - `np.arange(start, stop)`: Generates integer index counts (e.g. sample indices $n = 0, 1, 2, \dots$).
  - `np.sinc(x)`: Computes the mathematical cardinal sine function $\frac{\sin(\pi x)}{\pi x}$. Note: NumPy automatically includes $\pi$ inside the formula!
  - `np.dot(A, B)`: Performs matrix multiplication (summing products of samples and sinc curves).
  - `np.mean()`, `np.max()`, `np.abs()`: Statistical helpers to compute mean error, peak values, and absolute values.

### 2. SciPy (`import scipy.stats as stats`)
- **What it is:** The "Scientific & Engineering Toolbox".
- **Why we need it:** Provides built-in advanced statistical probability functions (Gaussian/Uniform distributions, cumulative probabilities, filtering).

### 3. Matplotlib (`import matplotlib.pyplot as plt`)
- **What it is:** The "Plotting & Oscilloscope Screen".
- **Why we need it:** Plots signals on your computer screen just like a digital oscilloscope or spectrum analyzer!
- **Key Functions Used:**
  - `plt.subplots(rows, cols)`: Creates a grid of plot windows.
  - `ax.plot(x, y)`: Draws a continuous line graph (like continuous signals $x(t)$).
  - `ax.stem(x, y)`: Draws discrete impulse stems with dots on top (representing discrete samples $x[n]$).
  - `ax.axvline(x)`: Draws a vertical marker line (e.g. marking theoretical frequency locations).
  - `plt.savefig()`: Saves high-resolution images (`.png`) for lab reports.

### 4. Pandas (`import pandas as pd`)
- **What it is:** The "Data Table Generator".
- **Why we need it:** Formats raw simulation numbers into clean, tabular columns with headers (e.g. Sampling Rate, MSE, Aliased Frequency) for easy reading.

---

## SECTION 2: Step-by-Step Code & Math Walkthrough

Let's break down `experiment_03.py` line-by-line so you can explain every detail with confidence in your lab viva.

### Step 1: Defining the Continuous Signal
```python
def continuous_signal(t):
    return np.sin(2.0 * np.pi * 100.0 * t) + 0.5 * np.sin(2.0 * np.pi * 300.0 * t)
```
- **Math Equation:** $x(t) = \sin(2\pi \cdot 100 t) + 0.5 \sin(2\pi \cdot 300 t)$
- **Why $2\pi f t$?** Sine functions in computer math take angles in **radians**. Since $1\text{ Hz} = 2\pi\text{ radians/sec}$, we multiply frequency $f$ by $2\pi t$.
- **Frequencies:**
  - Tone 1: $f_1 = 100\text{ Hz}$ (Amplitude = 1.0 V)
  - Tone 2: $f_2 = 300\text{ Hz}$ (Amplitude = 0.5 V)
  - **Highest Frequency ($f_{\max}$):** $300\text{ Hz}$.
  - **Nyquist Rate ($f_{\text{Nyquist}}$):** $2 \times f_{\max} = 2 \times 300 = 600\text{ Hz}$.

---

### Step 2: Sampling the Signal
```python
ts = 1.0 / fs  # Sampling Interval (seconds per sample)
t_samples = n_indices * ts  # Discrete sample time points
x_samples = continuous_signal(t_samples)  # Sample values x[n]
```
- **Concept:** Analog-to-Digital Conversion (ADC) takes snapshots of the continuous wave $x(t)$ every $T_s = 1/f_s$ seconds.
- **Three Cases Tested:**
  1. **Oversampling ($f_s = 1800\text{ Hz}$):** Sampling 3x faster than Nyquist ($3 \times 600\text{ Hz}$). Takes 90 samples in 50 ms.
  2. **Critical Sampling ($f_s = 600\text{ Hz}$):** Sampling at exactly Nyquist rate ($1 \times 600\text{ Hz}$). Takes 30 samples in 50 ms.
  3. **Undersampling ($f_s = 400\text{ Hz}$):** Sampling below Nyquist rate ($0.67 \times 600\text{ Hz}$). Takes 20 samples in 50 ms.

---

### Step 3: Whittaker-Shannon Sinc Reconstruction
```python
def sinc_reconstruction(sample_times, sample_values, t_fine, fs):
    dt_matrix = t_fine[None, :] - sample_times[:, None]
    sinc_matrix = np.sinc(fs * dt_matrix)
    x_hat = np.dot(sample_values, sinc_matrix)
    return x_hat
```
- **Math Formula:**
  $$\hat{x}(t) = \sum_{n} x[n] \cdot \operatorname{sinc}\left( f_s (t - n T_s) \right)$$
- **How it works intuitively:**
  - Each sample point $x[n]$ acts as an impulse that triggers a continuous $\operatorname{sinc}(u)$ pulse centered at $t = n T_s$.
  - Sinc pulses have zero-crossings at every other sample instant! Thus, at exact sample instants, only sample $x[n]$ contributes; between samples, the sinc tails overlap smoothly to reconstruct the exact original analog wave!
  - `np.dot` multiplies every sample value $x[n]$ by its corresponding sinc curve and sums them up across all time points in one single operation!

---

### Step 4: Measuring Spectrum with Real FFT
```python
def calculate_spectrum(signal, fs_fine):
    n = len(signal)
    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs_fine)
    magnitude = (2.0 / n) * np.abs(fft_vals)
    return freqs, magnitude
```
- **What is FFT?** Fast Fourier Transform converts time-domain signals $x(t)$ into frequency-domain magnitude spectra $X(f)$.
- **Why `rfft`?** Real FFT extracts only positive frequencies ($0$ to $f_s/2$), removing redundant negative frequencies.
- **Scaling `(2.0 / n)`:** Normalizes the FFT magnitude so that a $1\text{ V}$ sine wave shows an exact peak of $1.0\text{ V}$ on the graph!

---

### Step 5: Spectral Aliasing Derivation
When undersampling at $f_s = 400\text{ Hz}$:
- **Nyquist Limit:** $\frac{f_s}{2} = 200\text{ Hz}$. Any frequency above $200\text{ Hz}$ cannot be represented properly!
- **Aliased Frequency Formula:**
  $$f_{\text{alias}} = |f - k \cdot f_s| \quad \text{where } k = 1, 2, 3\dots$$
- **Calculation for $f_2 = 300\text{ Hz}$ tone:**
  $$f_{2,\text{alias}} = |300 - 1 \times 400| = |-100| = 100\text{ Hz}$$
- **What happens on the spectrum?**
  - The $300\text{ Hz}$ tone folds back into the $[0, 200\text{ Hz}]$ range and lands at **$100\text{ Hz}$**.
  - Since $f_1$ is already at $100\text{ Hz}$, the aliased $300\text{ Hz}$ tone combines with the $100\text{ Hz}$ tone.
  - The peak at $300\text{ Hz}$ completely disappears, while the peak at $100\text{ Hz}$ becomes distorted!

---

## SECTION 3: Predictive Viva-Voce Questions & Answers

**Q1: What is the Nyquist-Shannon Sampling Theorem?**  
*Answer:* It states that an analog bandlimited signal with maximum frequency $f_{\max}$ can be reconstructed perfectly without distortion if the sampling rate $f_s$ satisfies $f_s \ge 2 f_{\max}$.

**Q2: What is the Nyquist Rate vs Nyquist Frequency?**  
*Answer:*
- **Nyquist Rate:** Minimum sampling rate required ($2 f_{\max}$).
- **Nyquist Frequency (Folding Frequency):** Half the sampling rate ($f_s / 2$). Signals above $f_s / 2$ suffer aliasing.

**Q3: What is Aliasing and why does it occur?**  
*Answer:* Aliasing occurs when a signal is sampled below its Nyquist rate ($f_s < 2 f_{\max}$). High-frequency components overlap/fold into the lower frequency band, causing high frequencies to masquerade as lower frequencies in the reconstructed signal.

**Q4: How do you prevent aliasing in real-world systems?**  
*Answer:* By passing the analog signal through an **Anti-Aliasing Filter** (an analog low-pass filter) *before* sampling to remove any frequency components higher than $f_s / 2$.

**Q5: What is ideal reconstruction filter impulse response?**  
*Answer:* An ideal low-pass filter has a rectangular frequency response in the frequency domain, which corresponds to a **sinc pulse** $\operatorname{sinc}(f_s t)$ in the time domain.

**Q6: In your experiment, what was the aliased frequency when $f_2 = 300\text{ Hz}$ was sampled at $f_s = 400\text{ Hz}$?**  
*Answer:* The aliased frequency was $100\text{ Hz}$, calculated as $f_{\text{alias}} = |300 - 400| = 100\text{ Hz}$.

---

## SECTION 4: File Map & References

- **Python Implementation Script:** [`experiment_03.py`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_03_Sampling_Aliasing_and_Reconstruction/experiment_03.py)
- **Jupyter Notebook:** [`Experiment_03_Lab_Report.ipynb`](file:///home/apurba/Projects/Digital_Communication_Lab/Experiment_03_Sampling_Aliasing_and_Reconstruction/Experiment_03_Lab_Report.ipynb)
- **Master README:** [`README.md`](file:///home/apurba/Projects/Digital_Communication_Lab/README.md)
