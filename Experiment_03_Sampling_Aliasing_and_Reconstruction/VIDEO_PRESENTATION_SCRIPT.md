# 🎬 Video Presentation Script
## Experiment 3: Sampling, Aliasing & Whittaker-Shannon Sinc Reconstruction
### *Software-Based Digital Communication Laboratory*

- **Presenter:** Apurba Maity
- **Roll Number:** `34900324001`
- **Department:** Electronics and Communication Engineering
- **Institution:** Cooch Behar Government Engineering College
- **Subject:** Software-Based Digital Communication Laboratory
- **Target Video Length:** 4:30 – 5:00 minutes
- **Recording Mode:** Screen Capture (OBS Studio / Screen Recorder) + Clear Voiceover

---

## 📋 Pre-Recording Setup & Windows to Open
1. **Window 1 (Main Focus — 75% of video):** VS Code / Jupyter Notebook with [`experiment_03.py`](experiment_03.py) and [`Experiment_03_Lab_Report.ipynb`](Experiment_03_Lab_Report.ipynb).
2. **Window 2 (Plots):** Matplotlib plot window or image viewer showing the 4 generated figures from [`plots/`](plots/).
3. **Window 3 (Closure — 30 seconds):** Interactive Web Simulator ([`index.html`](index.html)) open in browser.
4. **Window 4 (Closing):** GitHub Repository page ([`SecretiveCodeRunner/Digital_Communication_Lab`](https://github.com/SecretiveCodeRunner/Digital_Communication_Lab)).

---

## ⏱️ Scene-by-Scene Presentation Script

---

### 🟢 SCENE 1: Introduction & Experiment Objectives (0:00 – 0:40)
**🖥️ On-Screen Action:**
Show VS Code editor with [`Experiment_03_Lab_Report.ipynb`](Experiment_03_Lab_Report.ipynb) showing the title banner, your Name, Roll Number, and Institution.

> **🎙️ Spoken Narration:**
> 
> *"Hello everyone and respected faculty. My name is **Apurba Maity**, Roll Number **34900324001**, from the Department of Electronics and Communication Engineering at Cooch Behar Government Engineering College.*
> 
> *Today, I will be presenting **Experiment 3** of our Software-Based Digital Communication Laboratory: **Sampling, Aliasing, and Whittaker-Shannon Sinc Reconstruction**.*
> 
> *Our core objective today is to explore the **Nyquist-Shannon Sampling Theorem** through Python numerical simulation, implement **ideal sinc interpolation** from first principles, observe **spectral aliasing** when undersampled, and most importantly, examine the critical differences between **pure theoretical assumptions and practical computational realities**."*

---

### 🔵 SCENE 2: Theoretical Formulation & Signal Definition (0:40 – 1:25)
**🖥️ On-Screen Action:**
Scroll to Section 1 of the Notebook, highlighting the mathematical formulas for $x(t)$, $f_{\text{Nyquist}}$, and $f_{\text{alias}}$.

> **🎙️ Spoken Narration:**
> 
> *"Let us first look at our signal model.*
> 
> *We construct a continuous two-tone multi-frequency signal:*
> $$x(t) = \sin(2\pi \cdot 100 t) + 0.5 \sin(2\pi \cdot 300 t)$$
> 
> *Here, the fundamental frequency is $f_1 = 100\text{ Hz}$ and the highest harmonic is $f_2 = 300\text{ Hz}$. Therefore, our maximum signal bandwidth is $f_{\max} = 300\text{ Hz}$.*
> 
> *According to the **Nyquist-Shannon theorem**, exact recovery requires a sampling frequency:*
> $$f_s \ge 2 f_{\max} = 2 \times 300 = 600\text{ Hz}$$
> 
> *Continuous signal reconstruction is governed by the **Whittaker-Shannon sinc interpolation formula**:*
> $$\hat{x}(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \operatorname{sinc}\left(f_s (t - n T_s)\right)$$
> 
> *If we violate this by undersampling at $f_s = 400\text{ Hz}$, theory predicts that the $300\text{ Hz}$ tone will fold across the Nyquist boundary $f_s/2 = 200\text{ Hz}$ according to:*
> $$f_{\text{alias}} = |f_2 - k \cdot f_s| = |300 - 1 \times 400| = 100\text{ Hz}$$
> 
> *Now, let us examine how we implemented this in Python."*

---

### 🟡 SCENE 3: Python Code Architecture & DSP Walkthrough (1:25 - 2:15)
**🖥️ On-Screen Action:**
Switch to [`experiment_03.py`](experiment_03.py) in VS Code. Highlight the `sinc_reconstruction()` and `calculate_spectrum()` functions.

> **🎙️ Spoken Narration:**
> 
> *"Here in our Python implementation, we avoided black-box toolboxes and implemented the core algorithms directly with NumPy.*
> 
> *Look at lines 53 to 63 in `sinc_reconstruction`. To evaluate the Whittaker-Shannon summation efficiently for thousands of time points, we construct a 2D distance matrix `dt_matrix = t_fine[None, :] - sample_times[:, None]`. Passing this into `np.sinc(fs * dt_matrix)` gives our sinc kernel matrix. A single vectorized matrix dot product `np.dot(sample_values, sinc_matrix)` sums all overlapping sinc pulses in a fraction of a millisecond.*
> 
> *For spectral analysis, lines 65 to 73 use `np.fft.rfft` to compute the single-sided discrete Fourier spectrum, normalized by $2/N$ to obtain exact physical peak amplitudes.*
> 
> *Notice also lines 110 to 125: we extended our sampling window by 20 samples on either boundary. This prevents artificial edge-truncation errors in our sinc reconstruction."*

---

### 🟣 SCENE 4: Plot Walkthrough & Empirical Validation (2:15 – 3:25)
**🖥️ On-Screen Action:**
Bring up the generated figures from the [`plots/`](plots/) folder one by one or scroll through Section 3 of the notebook.

#### 📍 Plot 1: Discrete Sampled Stems (`exp3_sampled_signals.png`)
> **🎙️ Spoken Narration:**
> *"In Figure 1, we observe our sampled discrete stems across the three test regimes over a 50 millisecond duration:*
> - *At **1800 Hz** (top), we capture 91 dense samples, yielding 6 samples per cycle of our 300 Hz wave.*
> - *At **600 Hz** (middle), we capture 31 samples, which is exactly 2 samples per cycle.*
> - *At **400 Hz** (bottom), we capture only 21 samples—barely 1.3 samples per cycle—which fails to capture the true peaks."*

#### 📍 Plot 2 & Plot 3: Reconstructed Waveforms & FFT Spectra (`exp3_reconstructed_waveforms.png` & `exp3_magnitude_spectra.png`)
> **🎙️ Spoken Narration:**
> *"Looking at Figure 2 and Figure 3 together:*
> - *In the **1800 Hz Oversampled case**, the reconstructed dashed curve overlays the original black reference signal perfectly, with a near-zero Mean Squared Error of $5.0 \times 10^{-6}$. The FFT spectrum cleanly recovers both the 100 Hz and 300 Hz peaks.*
> - *In the **400 Hz Undersampled case**, the reconstructed waveform is severely distorted. In the FFT spectrum, the 300 Hz peak has completely vanished from its true position and folded directly onto **100 Hz**, exactly matching our theoretical formula $|300 - 400| = 100\text{ Hz}$!"*

#### 📍 Plot 4: Error Waveforms (`exp3_reconstruction_error.png`)
> **🎙️ Spoken Narration:**
> *"In Figure 4, the error curve $e(t) = x(t) - \hat{x}(t)$ confirms this quantitatively: the oversampled error is a flat zero baseline, whereas the undersampled error oscillates with a massive MSE of **0.25**, reflecting the complete structural loss of the 300 Hz harmonic."*

---

### 🟠 SCENE 5: 🌟 Theory vs. Practicality & Computational Realities (3:25 – 4:15)
**🖥️ On-Screen Action:**
Scroll to **Section 4: Theory vs. Practicality** in the Notebook. Point with mouse to the comparative table.

> **🎙️ Spoken Narration:**
> 
> *"Now, let us address the most important insight of this laboratory: **Where does pure mathematical theory diverge from practical simulation and physical hardware?**"*
> 
> 1. **Phase Nulling at Critical Nyquist ($f_s = 2f_{\max}$):**
>    *"First, theory states that sampling at exactly $f_s = 2f_{\max} = 600\text{ Hz}$ is sufficient. But in our simulation, the 600 Hz case yielded an MSE of **0.1235**! Why?*
>    *Because our test signal is a pure sine wave $\sin(2\pi \cdot 300 t)$. When sampled at intervals of $1/600\text{ s}$, every sample falls exactly on a zero-crossing: $\sin(n\pi) \equiv 0$. The 300 Hz component completely vanished from the discrete sample array! This proves that in practical engineering, we cannot operate right at the theoretical boundary; we must strictly oversample ($f_s \ge 2.2 f_{\max}$) to avoid phase nulling."*
> 
> 2. **Infinite Sinc Summation vs. Finite Windowing:**
>    *"Second, the Whittaker-Shannon formula assumes an infinite summation from $-\infty$ to $+\infty$. In real DSP processors and computers, we only record finite time windows (e.g. 50 ms). Truncating the sinc series introduces boundary distortion, which is why we implemented boundary sample padding in Python."*
> 
> 3. **Anti-Aliasing Filter Requirement:**
>    *"Finally, in math, we can write equations for folded frequencies. But in physical ADC hardware, once aliasing occurs, the folded frequency is mathematically indistinguishable from true baseband data. Therefore, an analog **Anti-Aliasing Low-Pass Filter** must always precede the hardware ADC."*

---

### 🔘 SCENE 6: Interactive Web Studio Demonstration (Bonus Closure) (4:15 – 4:45)
**🖥️ On-Screen Action:**
Switch to the browser showing [`index.html`](index.html). Click the **1800 Hz**, **600 Hz**, and **400 Hz** preset buttons and briefly drag the $f_s$ slider.

> **🎙️ Spoken Narration:**
> 
> *"As an interactive companion to our Python code, we also compiled this lightweight simulation studio.*
> 
> *Here, we can dynamically drag the sampling frequency slider from 1800 Hz down to 300 Hz. Notice how the reconstructed green waveform morphs in real-time at 60 frames per second, and in the FFT spectrum below, you can watch the aliased red spectral peak sweep continuously as the Nyquist boundary moves.*
> 
> *We can also use the audio buttons to hear how aliasing lowers the perceived acoustic pitch."*

---

### 🔴 SCENE 7: Summary & Conclusion (4:45 – 5:00)
**🖥️ On-Screen Action:**
Switch to the GitHub repository page ([`SecretiveCodeRunner/Digital_Communication_Lab`](https://github.com/SecretiveCodeRunner/Digital_Communication_Lab)).

> **🎙️ Spoken Narration:**
> 
> *"In summary, this experiment successfully verified the Nyquist-Shannon Sampling Theorem, validated ideal sinc reconstruction in Python, demonstrated spectral aliasing, and established the critical differences between continuous theory and discrete DSP implementation.*
> 
> *The entire source code, Jupyter notebook, and study guide are open-source on my GitHub repository.*
> 
> *Thank you very much for your time and attention!"*

---

## 🎯 Faculty Viva & Defense Cheat-Sheet
- **Q: Why was MSE = 0.1235 at 600 Hz instead of 0?**
  - **A:** The 300 Hz component was $\sin(2\pi \cdot 300 t)$. At $t_n = n/600$, $\sin(n\pi) = 0$. All samples were zero, so sinc reconstruction only recovered the 100 Hz tone. The missing 300 Hz power is $\frac{A_2^2}{2} = \frac{0.5^2}{2} = 0.125\text{ V}^2$.
- **Q: What is the purpose of the 2D matrix in `sinc_reconstruction`?**
  - **A:** Vectorization. `t_fine[None, :] - sample_times[:, None]` creates an $(M \times N)$ distance grid, allowing `np.dot` to compute the full Whittaker-Shannon summation in $O(1)$ Python calls.
- **Q: How is aliasing prevented in real communication systems?**
  - **A:** By placing an analog active Low-Pass Anti-Aliasing Filter (e.g., Butterworth or Chebyshev) before the ADC sampler.
