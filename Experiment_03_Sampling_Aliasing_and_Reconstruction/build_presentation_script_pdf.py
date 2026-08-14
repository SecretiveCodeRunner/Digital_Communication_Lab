"""
Build mobile-ready, highly styled HTML and printable PDF for Experiment 3 Presentation Script.
"""

import os
import subprocess

EXP3_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(EXP3_DIR, "Experiment_03_Presentation_Script.html")
PDF_PATH = os.path.join(EXP3_DIR, "Experiment_03_Presentation_Script.pdf")

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exp 3 Video Presentation Script — Digital Comm Lab</title>
    <!-- KaTeX CSS & JS for Math Rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>
    <style>
        :root {
            --primary: #1e3c72;
            --primary-dark: #112244;
            --secondary: #2a5298;
            --accent: #15803d;
            --accent-bg: #f0fdf4;
            --cue-bg: #eff6ff;
            --cue-border: #3b82f6;
            --insight-bg: #fffbeb;
            --insight-border: #d97706;
            --danger: #b91c1c;
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #475569;
            --border: #e2e8f0;
            --code-bg: #0f172a;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-dark);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 860px;
            margin: 0 auto;
            padding: 24px 18px;
        }

        .header-card {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 26px 24px;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
            margin-bottom: 24px;
        }

        .header-card h1 {
            margin: 0 0 8px 0;
            font-size: 1.85rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .header-card p {
            margin: 4px 0;
            font-size: 0.96rem;
            opacity: 0.92;
        }

        .badge-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 14px;
        }

        .badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .badge.accent {
            background: #22c55e;
            color: #052e16;
        }

        .card {
            background: var(--bg-card);
            border-radius: 10px;
            padding: 22px;
            margin-bottom: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }

        h2 {
            color: var(--primary);
            font-size: 1.35rem;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
            margin-top: 0;
            margin-bottom: 14px;
        }

        h3 {
            color: var(--secondary);
            font-size: 1.15rem;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .screen-box {
            background: var(--cue-bg);
            border-left: 4px solid var(--cue-border);
            padding: 14px 18px;
            margin-bottom: 14px;
            border-radius: 0 8px 8px 0;
            font-size: 0.94rem;
        }

        .screen-title {
            font-weight: 700;
            color: #1d4ed8;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .speech-box {
            background: var(--accent-bg);
            border-left: 4px solid var(--accent);
            padding: 16px 20px;
            margin-bottom: 18px;
            border-radius: 0 8px 8px 0;
            font-size: 1.02rem;
            line-height: 1.65;
            color: #14532d;
        }

        .speech-title {
            font-weight: 700;
            color: #15803d;
            margin-bottom: 8px;
            font-size: 0.92rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .speech-box p {
            margin: 6px 0;
        }

        .insight-box {
            background: var(--insight-bg);
            border-left: 4px solid var(--insight-border);
            padding: 16px 20px;
            margin-bottom: 18px;
            border-radius: 0 8px 8px 0;
            font-size: 0.98rem;
        }

        .insight-title {
            font-weight: 700;
            color: #b45309;
            margin-bottom: 6px;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        code {
            background: #f1f5f9;
            color: #0f172a;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.9em;
        }

        pre {
            background: var(--code-bg);
            color: #f8fafc;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.88rem;
            line-height: 1.5;
            margin: 12px 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 0.92rem;
        }

        th, td {
            padding: 11px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            background: #f1f5f9;
            color: var(--primary-dark);
            font-weight: 600;
        }

        .checklist {
            list-style: none;
            padding-left: 0;
        }

        .checklist li {
            padding: 6px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .footer {
            text-align: center;
            padding: 24px 0;
            color: var(--text-muted);
            font-size: 0.85rem;
            border-top: 1px solid var(--border);
            margin-top: 20px;
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Header Card -->
    <div class="header-card">
        <h1>🎬 Video Presentation Script & Guide</h1>
        <p><strong>Experiment 3:</strong> Sampling, Aliasing & Whittaker-Shannon Sinc Reconstruction</p>
        <p><strong>Presenter:</strong> Apurba Maity (Roll No: <code>34900324001</code>)</p>
        <p><strong>Department:</strong> Electronics & Communication Engineering $|$ Cooch Behar GEC</p>
        <div class="badge-bar">
            <div class="badge">⏱️ Duration: 4:30 – 5:00 min</div>
            <div class="badge accent">🎯 Focus: Python Code & Plot Walkthrough</div>
            <div class="badge">🌟 Theory vs Practicality Deep-Dive</div>
        </div>
    </div>

    <!-- Pre-Recording Setup -->
    <div class="card">
        <h2>📋 Pre-Recording Windows & Setup</h2>
        <ul class="checklist">
            <li>🖥️ <strong>Window 1 (Main Focus — 75% of video):</strong> VS Code / Jupyter Notebook with <code>experiment_03.py</code> and <code>Experiment_03_Lab_Report.ipynb</code>.</li>
            <li>📊 <strong>Window 2 (Plots Viewer):</strong> Matplotlib generated figures in <code>plots/</code> directory.</li>
            <li>🌐 <strong>Window 3 (Closure — 30 seconds):</strong> Interactive Web Studio (<code>index.html</code>) in full-screen browser.</li>
            <li>🐙 <strong>Window 4 (Closing):</strong> GitHub Public Repository (<code>SecretiveCodeRunner/Digital_Communication_Lab</code>).</li>
        </ul>
    </div>

    <!-- SCENE 1 -->
    <div class="card">
        <h2>🟢 SCENE 1: Introduction & Objectives (0:00 – 0:40)</h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ ON-SCREEN ACTION</div>
            Show VS Code open to <code>Experiment_03_Lab_Report.ipynb</code> on the title banner, displaying your Name, Roll Number, and Subject Header.
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ SPOKEN NARRATION (Speak clearly and steadily)</div>
            <p>"Hello everyone and respected faculty. My name is <strong>Apurba Maity</strong>, Roll Number <strong>34900324001</strong>, from the Department of Electronics and Communication Engineering at Cooch Behar Government Engineering College.</p>
            <p>Today, I will be presenting <strong>Experiment 3</strong> of our Software-Based Digital Communication Laboratory: <strong>Sampling, Aliasing, and Whittaker-Shannon Sinc Reconstruction</strong>.</p>
            <p>Our core objective today is to explore the <strong>Nyquist-Shannon Sampling Theorem</strong> through Python numerical simulation, implement <strong>ideal sinc interpolation</strong> from first principles, observe <strong>spectral aliasing</strong> when undersampled, and most importantly, examine the critical differences between <strong>pure theoretical mathematical assumptions and practical computational realities</strong>."</p>
        </div>
    </div>

    <!-- SCENE 2 -->
    <div class="card">
        <h2>🔵 SCENE 2: Theoretical Formulation & Signal Model (0:40 – 1:25)</h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ ON-SCREEN ACTION</div>
            Scroll to Section 1 of the Notebook, highlighting the mathematical formulas for $x(t)$, $f_{\text{Nyquist}}$, and the aliasing folding formula.
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ SPOKEN NARRATION</div>
            <p>"Let us first establish our theoretical framework. We construct a deterministic continuous two-tone signal:</p>
            <p>$$x(t) = \sin(2\pi \cdot 100 t) + 0.5 \sin(2\pi \cdot 300 t)$$</p>
            <p>Here, the fundamental frequency is $f_1 = 100\text{ Hz}$ and the highest harmonic is $f_2 = 300\text{ Hz}$. Thus, the maximum signal bandwidth is $f_{\max} = 300\text{ Hz}$.</p>
            <p>According to the <strong>Nyquist-Shannon Sampling Theorem</strong>, exact lossless recovery requires a sampling frequency satisfying:</p>
            <p>$$f_s \ge 2 f_{\max} = 2 \times 300\text{ Hz} = 600\text{ Hz}$$</p>
            <p>Continuous-time reconstruction is governed by the <strong>Whittaker-Shannon sinc interpolation formula</strong>:</p>
            <p>$$\hat{x}(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \operatorname{sinc}\left(f_s (t - n T_s)\right), \quad \text{where } \operatorname{sinc}(u) = \frac{\sin(\pi u)}{\pi u}$$</p>
            <p>If we violate this by undersampling at $f_s = 400\text{ Hz}$, the high-frequency $300\text{ Hz}$ component folds across the Nyquist boundary $f_s/2 = 200\text{ Hz}$ according to the aliasing formula:</p>
            <p>$$f_{\text{alias}} = |f_2 - k \cdot f_s| = |300 - 1 \times 400| = |-100| = 100\text{ Hz}$$</p>
            <p>Now, let us examine how we implemented this in Python without using external black-box toolboxes."</p>
        </div>
    </div>

    <!-- SCENE 3 -->
    <div class="card">
        <h2>🟡 SCENE 3: Python Code Architecture & DSP Walkthrough (1:25 – 2:15)</h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ ON-SCREEN ACTION</div>
            Switch to <code>experiment_03.py</code> in VS Code. Highlight the <code>sinc_reconstruction()</code> function (lines 53–63) and <code>calculate_spectrum()</code> (lines 65–73).
        </div>
        <pre><code>def sinc_reconstruction(sample_times, sample_values, t_fine, fs):
    # Vectorized 2D broadcast: shape (N_samples, M_eval_points)
    dt_matrix = t_fine[None, :] - sample_times[:, None]
    sinc_matrix = np.sinc(fs * dt_matrix)  # np.sinc computes sin(pi*x)/(pi*x)
    # Sum overlapping sinc pulses across all discrete samples
    x_hat = np.dot(sample_values, sinc_matrix)
    return x_hat</code></pre>
        <div class="speech-box">
            <div class="speech-title">🎙️ SPOKEN NARRATION</div>
            <p>"Here in our Python implementation, we avoided black-box DSP functions and implemented the core mathematics directly using NumPy.</p>
            <p>As shown in lines 53 to 63 in <code>sinc_reconstruction</code>:</p>
            <ul>
                <li>To evaluate the Whittaker-Shannon summation efficiently for thousands of time points, we construct a 2D distance matrix using array broadcasting: <code>dt_matrix = t_fine[None, :] - sample_times[:, None]</code>.</li>
                <li>Passing this into <code>np.sinc(fs * dt_matrix)</code> creates our full interpolation kernel grid.</li>
                <li>A single vectorized dot product <code>np.dot(sample_values, sinc_matrix)</code> instantly sums all overlapping sinc pulses across the entire continuous evaluation grid in a fraction of a millisecond.</li>
            </ul>
            <p>For frequency analysis, lines 65 to 73 use <code>np.fft.rfft</code> to compute the single-sided discrete Fourier spectrum, normalized by $2/N$ to obtain exact physical peak amplitudes.</p>
            <p>Furthermore, in lines 110 to 125, we implemented sample boundary padding ($N_{\text{pad}} = 20$), eliminating artificial edge-truncation errors in our numerical reconstruction."</p>
        </div>
    </div>

    <!-- SCENE 4 -->
    <div class="card">
        <h2>🟣 SCENE 4: Plot Walkthrough & Empirical Validation (2:15 – 3:25)</h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ ON-SCREEN ACTION</div>
            Display the 4 generated Matplotlib figures from <code>plots/</code> or scroll through Section 3 of the Jupyter Notebook.
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ SPOKEN NARRATION</div>
            <p>"Let us now examine our empirical results across the 4 generated figures:</p>
            <p><strong>1. Discrete Sample Stems (Figure 1):</strong> Over our 50 ms test duration:
            <ul>
                <li>At <strong>1800 Hz</strong> (top), 91 dense samples capture 6 samples per cycle of the 300 Hz wave.</li>
                <li>At <strong>600 Hz</strong> (middle), 31 samples capture exactly 2 samples per cycle.</li>
                <li>At <strong>400 Hz</strong> (bottom), only 21 samples are recorded—barely 1.3 samples per cycle—missing the sinusoidal peaks.</li>
            </ul>
            </p>
            <p><strong>2. Reconstructed Waveforms & FFT Spectra (Figures 2 & 3):</strong>
            <ul>
                <li>In the <strong>1800 Hz Oversampled case</strong>, the reconstructed dashed curve overlays the original black reference signal perfectly, yielding a near-zero Mean Squared Error of $5.0 \times 10^{-6}\text{ V}^2$. The FFT spectrum cleanly recovers both the 100 Hz and 300 Hz peaks.</li>
                <li>In the <strong>400 Hz Undersampled case</strong>, the reconstructed waveform is heavily distorted. Looking at the FFT spectrum, the 300 Hz peak has completely vanished from its true position and folded directly onto <strong>100 Hz</strong>, exactly confirming our theoretical derivation $|300 - 400| = 100\text{ Hz}$!</li>
            </ul>
            </p>
            <p><strong>3. Time-Domain Error (Figure 4):</strong> The error waveform $e(t) = x(t) - \hat{x}(t)$ confirms this quantitatively: oversampling yields a flat zero line, while undersampling results in a massive oscillating error with $\text{MSE} = \mathbf{0.25\text{ V}^2}$."</p>
        </div>
    </div>

    <!-- SCENE 5 -->
    <div class="card">
        <h2>🟠 SCENE 5: 🌟 Theory vs. Practicality & Computational Realities (3:25 – 4:15)</h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ ON-SCREEN ACTION</div>
            Scroll to <strong>Section 4: Theory vs. Practicality</strong> in the Notebook. Point with mouse cursor to the comparative table and error numbers.
        </div>
        <div class="insight-box">
            <div class="insight-title">💡 KEY DEFENSE POINT</div>
            Explain why $f_s = 600\text{ Hz}$ produced $\text{MSE} = 0.1235$ despite being at the Nyquist rate, and discuss finite-window sinc truncation and hardware anti-aliasing filters.
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ SPOKEN NARRATION</div>
            <p>"Now, let us address the most insightful question of this experiment: <strong>Where does pure mathematical theory diverge from practical simulation and physical hardware?</strong></p>
            <p><strong>1. Phase Nulling at Critical Nyquist ($f_s = 2f_{\max} = 600\text{ Hz}$):</strong><br>
            In textbooks, theory states that $f_s = 2f_{\max}$ guarantees exact signal reconstruction. However, in our simulation, the 600 Hz critical case produced an MSE of <strong>0.1235</strong>! Why did this happen?</p>
            <p>Our test signal is a pure sine wave: $\sin(2\pi \cdot 300 t)$. When sampled at intervals of $T_s = 1/600\text{ s}$, every sample falls exactly on a zero crossing:</p>
            <p>$$x_{\text{harmonic}}[n] = 0.5 \sin\left(2\pi \cdot 300 \cdot \frac{n}{600}\right) = 0.5 \sin(n\pi) \equiv 0$$</p>
            <p>Every single sample of the 300 Hz tone evaluated to zero! The sinc interpolator was therefore blind to the 300 Hz wave and only reconstructed the 100 Hz tone. The missing harmonic power is exactly $\frac{A_2^2}{2} = \frac{0.5^2}{2} = \mathbf{0.125\text{ V}^2}$, which matches our measured MSE of $0.1235\text{ V}^2$!</p>
            <p>This proves that in real-world DSP and ADC design, we cannot operate right at the theoretical boundary; we must strictly oversample ($f_s \ge 2.2 f_{\max}$) with a safety guard band to avoid phase nulling.</p>
            <p><strong>2. Infinite Sinc Summation vs. Finite Observation Window:</strong><br>
            Theoretical Whittaker-Shannon interpolation requires an infinite summation from $-\infty$ to $+\infty$. Real DSP processors and digital scopes operate on finite time windows ($T = 50\text{ ms}$). Truncating the sinc series introduces boundary ripples, which we resolved by implementing sample padding ($N_{\text{pad}} = 20$).</p>
            <p><strong>3. Physical Anti-Aliasing Filtering (AAF):</strong><br>
            In software math, we can inspect and predict folded frequencies. But in physical ADC hardware, once an out-of-band high-frequency signal aliases into baseband, it is mathematically inseparable from legitimate data. Therefore, an analog active Low-Pass Anti-Aliasing Filter must always precede the hardware ADC."</p>
        </div>
    </div>

    <!-- SCENE 6 -->
    <div class="card">
        <h2>🔘 SCENE 6: Interactive Web Simulator (Bonus Closure) (4:15 – 4:45)</h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ ON-SCREEN ACTION</div>
            Switch to browser window displaying <code>index.html</code>. Click preset buttons (<strong>1800 Hz</strong>, <strong>600 Hz</strong>, <strong>400 Hz</strong>) and briefly drag the $f_s$ slider.
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ SPOKEN NARRATION</div>
            <p>"As a bonus interactive closure, we also compiled this lightweight 60 FPS HTML5 simulation studio.</p>
            <p>Here, we can dynamically drag the sampling frequency slider from 1800 Hz down to 300 Hz. Notice how the reconstructed green waveform morphs in real time, and in the live FFT spectrum below, you can watch the aliased red peak sweep continuously across the folding boundary as $f_s$ decreases. We can also synthesize Web Audio tones to hear how aliasing lowers the perceived auditory pitch."</p>
        </div>
    </div>

    <!-- SCENE 7 -->
    <div class="card">
        <h2>🔴 SCENE 7: Summary & Conclusion (4:45 – 5:00)</h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ ON-SCREEN ACTION</div>
            Switch to GitHub repository page (<code>SecretiveCodeRunner/Digital_Communication_Lab</code>).
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ SPOKEN NARRATION</div>
            <p>"In conclusion, this experiment successfully verified the Nyquist-Shannon Sampling Theorem, implemented vectorized sinc reconstruction in Python, validated spectral aliasing folding, and clarified the boundary between continuous theory and discrete DSP implementation.</p>
            <p>The complete Python code, Jupyter lab notebook, printable study guides, and the interactive studio are published on my open-source GitHub repository.</p>
            <p>Thank you very much for your time and attention!"</p>
        </div>
    </div>

    <!-- Summary Table & Viva -->
    <div class="card">
        <h2>📊 Summary Data Table & Faculty Viva Defense</h2>
        <table>
            <thead>
                <tr>
                    <th>Regime</th>
                    <th>$f_s$ (Hz)</th>
                    <th>Ratio</th>
                    <th>Samples</th>
                    <th>MSE ($\text{V}^2$)</th>
                    <th>RMSE ($\text{V}$)</th>
                    <th>Harmonic Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Oversampled</strong></td>
                    <td>1800</td>
                    <td>$3.0\times$</td>
                    <td>91</td>
                    <td>$5.0 \times 10^{-6}$</td>
                    <td>0.0022</td>
                    <td>Clean recovery at 300 Hz</td>
                </tr>
                <tr>
                    <td><strong>Critical</strong></td>
                    <td>600</td>
                    <td>$1.0\times$</td>
                    <td>31</td>
                    <td>0.1235</td>
                    <td>0.3514</td>
                    <td>Phase Null ($\sin(n\pi)=0$)</td>
                </tr>
                <tr style="background: #fef2f2;">
                    <td><strong style="color: var(--danger);">Undersampled</strong></td>
                    <td>400</td>
                    <td>$0.67\times$</td>
                    <td>21</td>
                    <td>0.2500</td>
                    <td>0.5000</td>
                    <td><strong style="color: var(--danger);">Aliased to 100 Hz</strong></td>
                </tr>
            </tbody>
        </table>

        <h3>🎯 Predictive Viva Q&A Defense</h3>
        <p><strong>Q1: Why did Critical Sampling ($f_s = 600\text{ Hz}$) yield an MSE of 0.1235 instead of 0?</strong><br>
        <em>Answer:</em> The 300 Hz harmonic was $0.5\sin(2\pi \cdot 300 t)$. At $t_n = n/600$, $\sin(n\pi) \equiv 0$. All samples were zero, so sinc interpolation missed the 300 Hz tone. The energy of the lost harmonic is $\frac{1}{2} A_2^2 = \frac{1}{2}(0.5)^2 = 0.125\text{ V}^2$, matching our measured MSE of $0.1235\text{ V}^2$.</p>

        <p><strong>Q2: How does Python evaluate sinc reconstruction so fast?</strong><br>
        <em>Answer:</em> Vectorized 2D distance matrix <code>dt = t_fine[None, :] - sample_times[:, None]</code> and matrix product <code>np.dot(sample_values, sinc_matrix)</code>.</p>

        <p><strong>Q3: Why is an Anti-Aliasing Filter essential in hardware ADCs?</strong><br>
        <em>Answer:</em> Once an out-of-band signal aliases into baseband, it is mathematically inseparable from true data; analog low-pass filtering must precede sampling.</p>
    </div>

    <div class="footer">
        Digital Communication Laboratory $|$ Apurba Maity (Roll: 34900324001) $|$ Cooch Behar Government Engineering College
    </div>
</div>

</body>
</html>
"""

with open(HTML_PATH, "w") as f:
    f.write(html_content)
print("Created Presentation Script HTML:", HTML_PATH)

# Convert HTML to PDF via LibreOffice headless
cmd = f"libreoffice --headless --convert-to pdf {HTML_PATH} --outdir {EXP3_DIR}"
subprocess.run(cmd, shell=True, check=True)
print("Generated PDF Presentation Script:", PDF_PATH)
