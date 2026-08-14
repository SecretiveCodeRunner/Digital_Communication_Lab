"""
Build ultra-clean, beautifully formatted HTML and publication-grade PDF for Experiment 3 Presentation Script.
Uses Google Chrome headless to guarantee 100% accurate KaTeX math rendering, syntax highlighting, and clean typography.
"""

import os
import subprocess
import time

EXP3_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(EXP3_DIR, "Experiment_03_Presentation_Script.html")
PDF_PATH = os.path.join(EXP3_DIR, "Experiment_03_Presentation_Script.pdf")

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Experiment 3 Video Presentation Script — Digital Comm Lab</title>
    
    <!-- KaTeX CSS & JS for 100% Crisp Math Rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
    
    <style>
        @page {
            size: A4;
            margin: 14mm 12mm;
        }

        :root {
            --primary: #1e3c72;
            --primary-dark: #0f172a;
            --secondary: #2563eb;
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
            --code-bg: #1e293b;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-dark);
            line-height: 1.6;
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }

        .container {
            max-width: 860px;
            margin: 0 auto;
            padding: 10px 14px;
        }

        .header-card {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 22px 24px;
            border-radius: 10px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .header-card h1 {
            margin: 0 0 6px 0;
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .header-card p {
            margin: 3px 0;
            font-size: 0.95rem;
            opacity: 0.95;
        }

        .meta-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.25);
            font-size: 0.9rem;
        }

        .badge-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }

        .badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 10px;
            border-radius: 16px;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .badge.accent {
            background: #22c55e;
            color: #052e16;
        }

        .badge.gold {
            background: #f59e0b;
            color: #451a03;
        }

        .card {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 18px 20px;
            margin-bottom: 18px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
            page-break-inside: avoid;
            break-inside: avoid;
        }

        h2 {
            color: var(--primary);
            font-size: 1.25rem;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 6px;
            margin-top: 0;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .time-badge {
            font-size: 0.82rem;
            font-weight: 600;
            background: #e2e8f0;
            color: #334155;
            padding: 2px 8px;
            border-radius: 12px;
        }

        h3 {
            color: var(--secondary);
            font-size: 1.05rem;
            margin-top: 14px;
            margin-bottom: 8px;
        }

        .screen-box {
            background: var(--cue-bg);
            border-left: 4px solid var(--cue-border);
            padding: 10px 14px;
            margin-bottom: 12px;
            border-radius: 0 6px 6px 0;
            font-size: 0.92rem;
        }

        .screen-title {
            font-weight: 700;
            color: #1d4ed8;
            margin-bottom: 3px;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .speech-box {
            background: var(--accent-bg);
            border-left: 4px solid var(--accent);
            padding: 14px 18px;
            margin-bottom: 14px;
            border-radius: 0 6px 6px 0;
            font-size: 0.98rem;
            line-height: 1.65;
            color: #14532d;
        }

        .speech-title {
            font-weight: 700;
            color: #15803d;
            margin-bottom: 6px;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .speech-box p {
            margin: 6px 0;
        }

        .insight-box {
            background: var(--insight-bg);
            border-left: 4px solid var(--insight-border);
            padding: 14px 18px;
            margin-bottom: 14px;
            border-radius: 0 6px 6px 0;
            font-size: 0.94rem;
        }

        .insight-title {
            font-weight: 700;
            color: #b45309;
            margin-bottom: 4px;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .math-display-card {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            padding: 12px 16px;
            border-radius: 6px;
            margin: 10px 0;
            text-align: center;
        }

        code {
            background: #f1f5f9;
            color: #0f172a;
            padding: 2px 5px;
            border-radius: 4px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.88em;
        }

        pre {
            background: var(--code-bg);
            color: #f8fafc;
            padding: 12px 14px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.84rem;
            line-height: 1.45;
            margin: 10px 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 0.88rem;
        }

        th, td {
            padding: 8px 10px;
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
            margin: 6px 0;
        }

        .checklist li {
            padding: 5px 0;
            font-size: 0.92rem;
        }

        .footer {
            text-align: center;
            padding: 16px 0;
            color: var(--text-muted);
            font-size: 0.82rem;
            border-top: 1px solid var(--border);
            margin-top: 16px;
        }

        .spoken-emphasis {
            font-weight: 600;
            color: #064e3b;
        }

        .highlight-red {
            color: #b91c1c;
            font-weight: 700;
        }

        @media print {
            body {
                background: white;
            }
            .container {
                max-width: 100%;
                padding: 0;
            }
            .card {
                box-shadow: none;
                border: 1px solid #cbd5e1;
                margin-bottom: 14px;
            }
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Header Card -->
    <div class="header-card">
        <h1>Video Presentation Script & Guide</h1>
        <p><strong>Experiment 3:</strong> Sampling, Aliasing and Whittaker-Shannon Sinc Reconstruction</p>
        <p><strong>Subject:</strong> Software-Based Digital Communication Laboratory (ECE Dept.)</p>
        
        <div class="meta-grid">
            <div><strong>Presenter:</strong> Apurba Maity (Roll: <code>34900324001</code>)</div>
            <div><strong>Institution:</strong> Cooch Behar Govt. Engineering College</div>
        </div>

        <div class="badge-bar">
            <div class="badge">⏱️ Duration: 4:30 – 5:00 min</div>
            <div class="badge accent">🎯 Core Focus: Python Code & Plot Walkthrough</div>
            <div class="badge gold">🌟 Theory vs Practicality Deep-Dive</div>
        </div>
    </div>

    <!-- Pre-Recording Setup -->
    <div class="card">
        <h2>📋 Pre-Recording Setup & Windows to Open</h2>
        <ul class="checklist">
            <li>🖥️ <strong>Window 1 (Main Focus — 75% of video):</strong> VS Code open with <code>experiment_03.py</code> and <code>Experiment_03_Lab_Report.ipynb</code>.</li>
            <li>📊 <strong>Window 2 (Plots Viewer):</strong> High-resolution figures open from the <code>plots/</code> directory.</li>
            <li>🌐 <strong>Window 3 (Closure — 30 seconds):</strong> Interactive Simulation Studio (<code>index.html</code>) in full-screen browser.</li>
            <li>🐙 <strong>Window 4 (Closing):</strong> Public GitHub Repository (<code>SecretiveCodeRunner/Digital_Communication_Lab</code>).</li>
        </ul>
    </div>

    <!-- SCENE 1 -->
    <div class="card">
        <h2>
            <span>Scene 1: Introduction & Objective</span>
            <span class="time-badge">0:00 – 0:40</span>
        </h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ On-Screen Action</div>
            Show VS Code editor open to <code>Experiment_03_Lab_Report.ipynb</code> on the title banner, displaying your Name, Roll Number, Department, and Subject header.
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ Spoken Narration (Read aloud steadily)</div>
            <p>"Hello everyone and respected faculty. My name is <span class="spoken-emphasis">Apurba Maity</span>, Roll Number <span class="spoken-emphasis">34900324001</span>, from the Department of Electronics and Communication Engineering at Cooch Behar Government Engineering College.</p>
            <p>Today, I will be presenting <strong>Experiment 3</strong> of our Software-Based Digital Communication Laboratory: <strong>Sampling, Aliasing, and Whittaker-Shannon Sinc Reconstruction</strong>.</p>
            <p>Our core objective today is to explore the <strong>Nyquist-Shannon Sampling Theorem</strong> through Python numerical simulation, implement <strong>ideal sinc interpolation</strong> from first principles, observe <strong>spectral aliasing</strong> when undersampled, and most importantly, examine the critical differences between <strong>pure theoretical mathematical assumptions and practical computational realities</strong>."</p>
        </div>
    </div>

    <!-- SCENE 2 -->
    <div class="card">
        <h2>
            <span>Scene 2: Theoretical Formulation & Signal Model</span>
            <span class="time-badge">0:40 – 1:25</span>
        </h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ On-Screen Action</div>
            Scroll to Section 1 of the Notebook, highlighting the mathematical formulas for continuous test signal $x(t)$, Nyquist rate $f_{\text{Nyquist}}$, and the aliasing folding equation.
        </div>

        <div class="math-display-card">
            $$x(t) = \sin(2\pi \cdot 100 t) + 0.5 \sin(2\pi \cdot 300 t)$$
            $$f_s \ge 2 f_{\max} = 2 \times 300\text{ Hz} = 600\text{ Hz}$$
            $$\hat{x}(t) = \sum_{n=-\infty}^{\infty} x[n] \cdot \operatorname{sinc}\left(f_s (t - n T_s)\right)$$
            $$f_{\text{alias}} = |f_2 - k \cdot f_s| = |300 - 1 \times 400| = 100\text{ Hz}$$
        </div>

        <div class="speech-box">
            <div class="speech-title">🎙️ Spoken Narration</div>
            <p>"Let us first establish our theoretical framework. We construct a deterministic continuous two-tone signal: <strong>x of t equals sine of 2 pi times 100 t, plus 0.5 sine of 2 pi times 300 t</strong>.</p>
            <p>Here, the fundamental frequency is <strong>100 Hertz</strong> and the highest harmonic is <strong>300 Hertz</strong>. Thus, our maximum signal bandwidth is <strong>300 Hertz</strong>.</p>
            <p>According to the <strong>Nyquist-Shannon Sampling Theorem</strong>, exact lossless recovery requires a sampling frequency of at least twice the maximum frequency, which is <strong>2 times 300 = 600 Hertz</strong>.</p>
            <p>Continuous-time reconstruction is governed by the <strong>Whittaker-Shannon sinc interpolation formula</strong>, which convolves discrete samples with ideal sinc pulses.</p>
            <p>If we violate this by undersampling at <strong>400 Hertz</strong>, the high-frequency 300 Hertz component folds across the 200 Hertz Nyquist boundary down to <strong>100 Hertz</strong>, according to the formula: <strong>f-alias equals the absolute value of 300 minus 400, which equals 100 Hertz</strong>.</p>
            <p>Now, let us examine how we implemented this in Python without using external black-box toolboxes."</p>
        </div>
    </div>

    <!-- SCENE 3 -->
    <div class="card">
        <h2>
            <span>Scene 3: Python Code Architecture & DSP Walkthrough</span>
            <span class="time-badge">1:25 – 2:15</span>
        </h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ On-Screen Action</div>
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
            <div class="speech-title">🎙️ Spoken Narration</div>
            <p>"Here in our Python implementation, we avoided black-box DSP functions and implemented the core mathematics directly using NumPy.</p>
            <p>As shown in lines 53 to 63 in <code>sinc_reconstruction</code>:</p>
            <ul>
                <li>To evaluate the Whittaker-Shannon summation efficiently for thousands of time points, we construct a 2D distance matrix using array broadcasting: <code>dt_matrix = t_fine[None, :] - sample_times[:, None]</code>.</li>
                <li>Passing this into <code>np.sinc(fs * dt_matrix)</code> creates our full interpolation kernel grid.</li>
                <li>A single vectorized dot product <code>np.dot(sample_values, sinc_matrix)</code> instantly sums all overlapping sinc pulses across the entire continuous evaluation grid in a fraction of a millisecond.</li>
            </ul>
            <p>For frequency analysis, lines 65 to 73 use <code>np.fft.rfft</code> to compute the single-sided discrete Fourier spectrum, normalized by <strong>2 divided by N</strong> to obtain exact physical peak amplitudes.</p>
            <p>Furthermore, in lines 110 to 125, we implemented sample boundary padding of <strong>20 extra samples</strong> on either end, eliminating artificial edge-truncation errors in our numerical reconstruction."</p>
        </div>
    </div>

    <!-- SCENE 4 -->
    <div class="card">
        <h2>
            <span>Scene 4: Plot Walkthrough & Empirical Validation</span>
            <span class="time-badge">2:15 – 3:25</span>
        </h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ On-Screen Action</div>
            Display the 4 generated Matplotlib figures from the <code>plots/</code> folder or scroll through Section 3 of the Jupyter Notebook.
        </div>

        <div class="speech-box">
            <div class="speech-title">🎙️ Spoken Narration</div>
            <p>"Let us now examine our empirical results across the 4 generated figures:</p>
            <p><strong>1. Discrete Sample Stems (Figure 1):</strong> Over our 50 millisecond test duration:
            <ul>
                <li>At <strong>1800 Hertz</strong> (top), 91 dense samples capture 6 samples per cycle of the 300 Hertz wave.</li>
                <li>At <strong>600 Hertz</strong> (middle), 31 samples capture exactly 2 samples per cycle.</li>
                <li>At <strong>400 Hertz</strong> (bottom), only 21 samples are recorded—barely 1.3 samples per cycle—completely missing the sinusoidal peaks.</li>
            </ul>
            </p>
            <p><strong>2. Reconstructed Waveforms & FFT Spectra (Figures 2 & 3):</strong>
            <ul>
                <li>In the <strong>1800 Hertz Oversampled case</strong>, the reconstructed dashed curve overlays the original black reference signal perfectly, yielding a near-zero Mean Squared Error of <strong>5.0 times 10 to the minus 6</strong>. The FFT spectrum cleanly recovers both the 100 Hertz and 300 Hertz peaks.</li>
                <li>In the <strong>400 Hertz Undersampled case</strong>, the reconstructed waveform is heavily distorted. Looking at the FFT spectrum, the 300 Hertz peak has completely vanished from its true position and folded directly onto <strong class="highlight-red">100 Hertz</strong>, exactly confirming our theoretical derivation: <strong>absolute value of 300 minus 400 equals 100 Hertz</strong>!</li>
            </ul>
            </p>
            <p><strong>3. Time-Domain Error (Figure 4):</strong> The error waveform confirms this quantitatively: oversampling yields a flat zero baseline, while undersampling results in a massive oscillating error with a Mean Squared Error of <strong class="highlight-red">0.25</strong>."</p>
        </div>
    </div>

    <!-- SCENE 5 -->
    <div class="card">
        <h2>
            <span>Scene 5: 🌟 Theory vs. Practicality & Computational Realities</span>
            <span class="time-badge">3:25 – 4:15</span>
        </h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ On-Screen Action</div>
            Scroll to <strong>Section 4: Theory vs. Practicality</strong> in the Notebook. Point with mouse cursor to the comparative table and error numbers.
        </div>

        <div class="insight-box">
            <div class="insight-title">💡 Critical Viva & Defense Insight</div>
            Explain why $f_s = 600\text{ Hz}$ produced $\text{MSE} \approx 0.1235$ despite meeting the Nyquist rate, and explain the physical necessity of Anti-Aliasing filters and finite-window padding.
        </div>

        <div class="speech-box">
            <div class="speech-title">🎙️ Spoken Narration</div>
            <p>"Now, let us address the most insightful question of this experiment: <strong>Where does pure mathematical theory diverge from practical simulation and physical hardware?</strong></p>
            <p><strong>1. Phase Nulling at Critical Nyquist (600 Hertz):</strong><br>
            In textbooks, theory states that <strong>f_s = 2 f_max</strong> guarantees exact signal reconstruction. However, in our simulation, the 600 Hertz critical case produced an MSE of <strong>0.1235</strong>! Why did this happen?</p>
            <p>Our test signal is a pure sine wave: <strong>sine of 2 pi times 300 t</strong>. When sampled at intervals of <strong>1 divided by 600 seconds</strong>, every single sample falls exactly on a zero crossing: <strong>sine of n pi is identically zero</strong>!</p>
            <p>Every discrete sample of the 300 Hertz tone evaluated to zero! The sinc interpolator was therefore blind to the 300 Hertz wave and only reconstructed the 100 Hertz tone. The missing harmonic power is exactly <strong>0.5 squared divided by 2 = 0.125</strong>, which matches our measured MSE of <strong>0.1235</strong>!</p>
            <p>This proves that in real-world DSP and ADC design, we cannot operate right at the theoretical boundary; we must strictly oversample (for example at <strong>2.2 times f_max</strong>) with a safety guard band to avoid phase nulling.</p>
            <p><strong>2. Infinite Sinc Summation vs. Finite Observation Window:</strong><br>
            Theoretical Whittaker-Shannon interpolation requires an infinite summation from minus infinity to plus infinity. Real DSP processors and digital scopes operate on finite time windows (such as 50 milliseconds). Truncating the sinc series introduces boundary ripples, which we resolved by implementing sample padding of 20 extra points.</p>
            <p><strong>3. Physical Anti-Aliasing Filtering:</strong><br>
            In software math, we can inspect and predict folded frequencies. But in physical ADC hardware, once an out-of-band high-frequency signal aliases into baseband, it is mathematically inseparable from legitimate data. Therefore, an analog active Low-Pass Anti-Aliasing Filter must always precede the hardware ADC."</p>
        </div>
    </div>

    <!-- SCENE 6 -->
    <div class="card">
        <h2>
            <span>Scene 6: Interactive Web Simulator (Bonus Closure)</span>
            <span class="time-badge">4:15 – 4:45</span>
        </h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ On-Screen Action</div>
            Switch to browser window displaying <code>index.html</code>. Click preset buttons (<strong>1800 Hz</strong>, <strong>600 Hz</strong>, <strong>400 Hz</strong>) and briefly drag the $f_s$ slider.
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ Spoken Narration</div>
            <p>"As a bonus interactive closure, we also compiled this lightweight 60 FPS HTML5 simulation studio.</p>
            <p>Here, we can dynamically drag the sampling frequency slider from 1800 Hertz down to 300 Hertz. Notice how the reconstructed green waveform morphs in real time, and in the live FFT spectrum below, you can watch the aliased red peak sweep continuously across the folding boundary as sampling frequency decreases. We can also synthesize Web Audio tones to hear how aliasing lowers the perceived auditory pitch."</p>
        </div>
    </div>

    <!-- SCENE 7 -->
    <div class="card">
        <h2>
            <span>Scene 7: Summary & Conclusion</span>
            <span class="time-badge">4:45 – 5:00</span>
        </h2>
        <div class="screen-box">
            <div class="screen-title">🖥️ On-Screen Action</div>
            Switch to GitHub repository page (<code>SecretiveCodeRunner/Digital_Communication_Lab</code>).
        </div>
        <div class="speech-box">
            <div class="speech-title">🎙️ Spoken Narration</div>
            <p>"In conclusion, this experiment successfully verified the Nyquist-Shannon Sampling Theorem, implemented vectorized sinc reconstruction in Python, validated spectral aliasing folding, and clarified the boundary between continuous theory and discrete DSP implementation.</p>
            <p>The complete Python code, Jupyter lab notebook, printable study guides, and the interactive studio are published on my open-source GitHub repository.</p>
            <p>Thank you very much for your time and attention!"</p>
        </div>
    </div>

    <!-- Summary Table & Viva -->
    <div class="card">
        <h2>📊 Summary Results Table & Viva Q&A Defense</h2>
        <table>
            <thead>
                <tr>
                    <th>Regime</th>
                    <th>Sampling Rate ($f_s$)</th>
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
                    <td>1800 Hz</td>
                    <td>3.0x Nyquist</td>
                    <td>91</td>
                    <td>$5.0 \times 10^{-6}$</td>
                    <td>0.0022</td>
                    <td>Clean recovery at 300 Hz</td>
                </tr>
                <tr>
                    <td><strong>Critical</strong></td>
                    <td>600 Hz</td>
                    <td>1.0x Nyquist</td>
                    <td>31</td>
                    <td>0.1235</td>
                    <td>0.3514</td>
                    <td>Phase Null ($\sin(n\pi) \equiv 0$)</td>
                </tr>
                <tr style="background: #fef2f2;">
                    <td><strong style="color: var(--danger);">Undersampled</strong></td>
                    <td>400 Hz</td>
                    <td>0.67x Nyquist</td>
                    <td>21</td>
                    <td>0.2500</td>
                    <td>0.5000</td>
                    <td><strong style="color: var(--danger);">Aliased to 100 Hz</strong></td>
                </tr>
            </tbody>
        </table>

        <h3>🎯 Predictive Viva Q&A Defense Sheet</h3>
        <p><strong>Q1: Why did Critical Sampling ($f_s = 600\text{ Hz}$) yield an MSE of 0.1235 instead of 0?</strong><br>
        <em>Answer:</em> The 300 Hz harmonic was $0.5\sin(2\pi \cdot 300 t)$. When sampled at intervals of $T_s = 1/600\text{ s}$, the sample times are $t_n = n/600$, resulting in $0.5\sin(n\pi) \equiv 0$ for all integers $n$. Thus, all discrete samples of the 300 Hz component were identically zero! Sinc interpolation could only recover the 100 Hz tone. The energy of the lost 300 Hz tone is $\frac{1}{2} A_2^2 = \frac{1}{2}(0.5)^2 = 0.125\text{ V}^2$, which matches our measured MSE of $0.1235\text{ V}^2$.</p>

        <p><strong>Q2: How does your Python code implement sinc reconstruction without slow loops?</strong><br>
        <em>Answer:</em> Through 2D array broadcasting and matrix multiplication: <code>dt = t_fine[None, :] - sample_times[:, None]</code>, evaluated with <code>np.sinc(fs * dt)</code> and summed via <code>np.dot(sample_values, sinc_matrix)</code>.</p>

        <p><strong>Q3: Why is an Anti-Aliasing Filter essential in hardware ADCs?</strong><br>
        <em>Answer:</em> Once an out-of-band analog frequency higher than $f_s/2$ enters the ADC sampler, it aliases into baseband $[0, f_s/2]$ and produces identical discrete samples as a legitimate low-frequency signal. It is mathematically impossible to distinguish or filter out aliased components after digitization. Therefore, an analog active Low-Pass Filter must attenuate out-of-band frequencies <em>before</em> the ADC.</p>

        <p><strong>Q4: Why did we pad samples ($N_{\text{pad}} = 20$) in the time domain?</strong><br>
        <em>Answer:</em> Theoretical Whittaker-Shannon interpolation requires an infinite summation ($-\infty \le n \le +\infty$). In numerical simulation over a finite window $[0, T]$, truncating the sinc series leaves points near $t = 0$ and $t = T$ without neighboring sinc pulses, causing boundary edge distortion. Evaluating samples slightly beyond the plotting window ensures full sinc overlap across the entire evaluation interval.</p>
    </div>

    <div class="footer">
        Digital Communication Laboratory $|$ Apurba Maity (Roll: 34900324001) $|$ Cooch Behar Government Engineering College
    </div>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        if (typeof renderMathInElement !== 'undefined') {
            renderMathInElement(document.body, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ],
                throwOnError: false
            });
        }
    });
</script>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)
print("Created Presentation Script HTML:", HTML_PATH)

# Convert HTML to PDF using Google Chrome Headless (Runs JS, renders KaTeX math & print CSS)
cmd = [
    "google-chrome-stable",
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=5000",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]

print("Compiling PDF with Google Chrome Headless...")
subprocess.run(cmd, check=True)
print("Successfully generated pixel-perfect PDF Presentation Script:", PDF_PATH)
