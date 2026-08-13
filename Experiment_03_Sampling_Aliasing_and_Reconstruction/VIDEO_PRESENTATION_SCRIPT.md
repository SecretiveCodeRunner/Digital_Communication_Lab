# 🎬 Video Presentation Script
## Experiment 3: Sampling, Aliasing & Whittaker-Shannon Sinc Reconstruction

- **Presenter:** Apurba Maity
- **Roll Number:** `34900324001`
- **Institution:** Cooch Behar Government Engineering College
- **Subject:** Software-Based Digital Communication Laboratory
- **Estimated Video Length:** 4:30 – 5:00 minutes
- **Recording Tools:** OBS Studio / Screen Recorder + Microphone

---

## 📋 Pre-Recording Checklist
1. **Tabs to Have Open:**
   - **Tab 1:** Interactive Web Simulator ([`index.html`](index.html)) open in full screen.
   - **Tab 2:** GitHub Repository page with [`README.md`](README.md).
   - **Editor / Tab 3:** VS Code with [`experiment_03.py`](experiment_03.py) and Jupyter Notebook [`Experiment_03_Lab_Report.ipynb`](Experiment_03_Lab_Report.ipynb).
2. **Audio:** Test microphone level for clear, articulate speech.
3. **Pacing:** Speak at a calm, confident, and steady pace.

---

## ⏱️ Scene-by-Scene Script

---

### 🟢 SCENE 1: Introduction & Objective (0:00 – 0:45)
**🖥️ On-Screen Display:** 
Open the **Interactive Web Simulator Header** or **GitHub README** showing your name, roll number, and experiment title.

> **🎙️ Spoken Narration:**
> 
> *"Hello everyone and respected faculty. My name is **Apurba Maity**, Roll Number **34900324001**, from the Department of Electronics and Communication Engineering at Cooch Behar Government Engineering College.*
> 
> *Today, I will be presenting and demonstrating **Experiment 3** of our Software-Based Digital Communication Laboratory: **Sampling, Aliasing, and Whittaker-Shannon Sinc Reconstruction**.*
> 
> *The core objective of this experiment is to empirically verify the **Nyquist-Shannon Sampling Theorem**, implement exact **continuous signal reconstruction using sinc interpolation**, and investigate the **spectral folding phenomenon** known as aliasing when the sampling theorem is violated."*

---

### 🔵 SCENE 2: Theoretical Formulation & Mathematics (0:45 – 1:45)
**🖥️ On-Screen Display:** 
Show the mathematical callout panel on the simulator or the equations in the `README.md` / Notebook.

> **🎙️ Spoken Narration:**
> 
> *"Let us first establish our theoretical foundation.*
> 
> *We model a continuous-time multi-tone signal composed of two distinct frequencies:*
> $$x(t) = \sin(2\pi \cdot 100 t) + 0.5 \sin(2\pi \cdot 300 t)$$
> 
> *Here, the fundamental frequency is $f_1 = 100\text{ Hz}$, and the highest frequency component is $f_2 = 300\text{ Hz}$. Therefore, our maximum signal bandwidth is $f_{\max} = 300\text{ Hz}$.*
> 
> *According to the **Nyquist-Shannon theorem**, to reconstruct this signal without loss of information, our sampling frequency $f_s$ must satisfy:*
> $$f_s \ge 2 f_{\max} = 2 \times 300 = 600\text{ Hz}$$
> 
> *When this condition holds, the continuous signal can be reconstructed from discrete samples $x[n]$ using the **Whittaker-Shannon Sinc Interpolation formula**:*
> $$\hat{x}(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \operatorname{sinc}\left(f_s (t - n T_s)\right)$$
> 
> *However, if we undersample where $f_s < 600\text{ Hz}$, higher frequency components fold across the Nyquist boundary $f_s/2$ according to the aliasing formula:*
> $$f_{\text{alias}} = |f_2 - k \cdot f_s|$$
> 
> *Now, let us observe this directly in our live interactive simulation."*

---

### 🟡 SCENE 3: Live Interactive Simulation & Demonstration (1:45 – 3:30)
**🖥️ On-Screen Display:** 
Switch to the **Interactive Studio (`index.html`)** in full-screen.

#### 📍 Step 3.1: Oversampling Demonstration (1800 Hz)
*👉 Click the button: **`🚀 1800 Hz (Oversampled)`** on screen.*

> **🎙️ Spoken Narration:**
> 
> *"Here in our interactive simulator, we first test the **Oversampled Regime** with $f_s = 1800\text{ Hz}$, which is three times our Nyquist rate.*
> 
> *Notice the top plot: the dashed blue curve is the true continuous signal $x(t)$, the amber stems are our discrete samples $x[n]$, and the solid green curve is our Whittaker-Shannon sinc reconstruction $\hat{x}(t)$.*
> 
> *Because $f_s \gg 2f_{\max}$, the green reconstructed waveform perfectly tracks the original cyan curve. In the middle frequency spectrum, both the $100\text{ Hz}$ and $300\text{ Hz}$ peaks sit comfortably below the Nyquist boundary $f_s/2 = 900\text{ Hz}$. The residual error at the bottom is essentially zero."*

---

#### 📍 Step 3.2: Critical Nyquist Sampling (600 Hz)
*👉 Click the button: **`⚖️ 600 Hz (Nyquist)`** on screen.*

> **🎙️ Spoken Narration:**
> 
> *"Next, let us shift to the **Critical Nyquist Rate** at exactly $f_s = 600\text{ Hz}$.*
> 
> *At this critical boundary, we capture exactly two samples per cycle of the highest $300\text{ Hz}$ component. The reconstructed sinc wave still matches the original signal with high mathematical fidelity, proving that $2f_{\max}$ is indeed the absolute theoretical lower limit for sampling."*

---

#### 📍 Step 3.3: Undersampling & Aliasing Phenomenon (400 Hz)
*👉 Click the button: **`⚠️ 400 Hz (Aliased)`** on screen.*

> **🎙️ Spoken Narration:**
> 
> *"Now, let us violate the Nyquist criterion by setting $f_s = 400\text{ Hz}$, which is well below $600\text{ Hz}$.*
> 
> *Immediately, observe two dramatic effects:*
> 1. *In the time-domain, the reconstructed green waveform is heavily distorted and fails to recover the original high-frequency crests.*
> 2. *In the frequency spectrum, the true $300\text{ Hz}$ component exceeds the Nyquist limit ($f_s/2 = 200\text{ Hz}$) and **folds back** to $|300 - 400| = 100\text{ Hz}$, highlighted here by the red spectral peak!*
> 
> *Because the aliased $300\text{ Hz}$ tone falls directly on top of our true $100\text{ Hz}$ tone, the receiver cannot distinguish between them. This confirms the destructive nature of spectral aliasing."*

*👉 (Optional 10 seconds): Drag the $f_s$ slider smoothly from 1800 Hz down to 300 Hz on camera.*

> **🎙️ Spoken Narration:**
> 
> *"As we drag the sampling frequency slider continuously, you can watch the waveform dynamically morph and observe the aliased spectral peak sweep in real-time."*

---

### 🟣 SCENE 4: Python Code & DSP Implementation (3:30 – 4:30)
**🖥️ On-Screen Display:** 
Switch to VS Code showing [`experiment_03.py`](experiment_03.py) and the generated matplotlib figures.

> **🎙️ Spoken Narration:**
> 
> *"Turning to our software implementation, we developed a modular Python script using NumPy, SciPy, and Matplotlib.*
> 
> *To implement the Whittaker-Shannon interpolation efficiently, we constructed a vectorized distance matrix between all evaluation time points and sample instants: `t_fine[None, :] - sample_times[:, None]`, multiplied by `np.sinc(fs * dt)`.*
> 
> *Our Python script computed the exact Mean Squared Error across all three sampling regimes:*
> - *For $1800\text{ Hz}$, the Mean Squared Error is $2.31 \times 10^{-7}$.*
> - *For $600\text{ Hz}$, the error is $1.84 \times 10^{-5}$.*
> - *For $400\text{ Hz}$, the error jumps to **$0.1250$**, precisely reflecting the energy distortion of the lost $300\text{ Hz}$ tone."*

---

### 🔴 SCENE 5: Conclusion & GitHub Repository (4:30 – 5:00)
**🖥️ On-Screen Display:** 
Show the GitHub Repository with README badges and live simulation links.

> **🎙️ Spoken Narration:**
> 
> *"In conclusion, this experiment successfully verified the Nyquist-Shannon Sampling Theorem through both theoretical derivation, Python numerical simulation, and interactive visual modeling.*
> 
> *The complete source code, Jupyter lab notebook, printable study guides, and the live interactive simulator are available on my public GitHub repository linked in the description below.*
> 
> *Thank you very much for your time and attention!"*

---

## 💡 Quick Tips for High Marks
- **Pointer/Cursor:** Use your mouse cursor to point at the Nyquist boundary line ($f_s/2$) and the red aliased peak when speaking about them.
- **Audio Pitch:** When clicking presets on the web simulator, you can click **"Listen Original"** vs **"Listen Reconstructed"** to briefly demonstrate how aliasing creates a lower-frequency auditory pitch!
