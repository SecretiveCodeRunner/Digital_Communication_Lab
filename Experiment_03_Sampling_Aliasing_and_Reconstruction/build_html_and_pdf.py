"""
Build mobile-friendly HTML & PDF versions of the Study Guide for Experiment 3.
"""

import os
import subprocess

EXP3_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(EXP3_DIR, "Python_and_DSP_Study_Guide_Exp3.md")
HTML_PATH = os.path.join(EXP3_DIR, "Python_and_DSP_Study_Guide_Exp3.html")
PDF_PATH = os.path.join(EXP3_DIR, "Digital_Comm_Exp3_Study_Guide.pdf")

# HTML Template with inline mobile CSS styling and KaTeX for LaTeX Math
html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digital Communication Lab — Exp 3 Study & Viva Guide</title>
    <!-- KaTeX CSS & JS for Math Rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"></script>
    <style>
        :root {
            --primary: #2B579A;
            --primary-dark: #1b3864;
            --accent: #008A00;
            --danger: #D8000C;
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #475569;
            --border: #e2e8f0;
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
            max-width: 800px;
            margin: 0 auto;
            padding: 20px 15px;
        }

        .header-card {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 25px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 25px;
        }

        .header-card h1 {
            margin: 0 0 10px 0;
            font-size: 1.7rem;
            font-weight: 700;
        }

        .header-card p {
            margin: 4px 0;
            font-size: 0.95rem;
            opacity: 0.9;
        }

        .badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 10px;
        }

        .card {
            background: var(--bg-card);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }

        h2 {
            color: var(--primary);
            font-size: 1.35rem;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
            margin-top: 0;
        }

        h3 {
            color: var(--primary-dark);
            font-size: 1.15rem;
            margin-top: 18px;
            margin-bottom: 8px;
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
            background: #0f172a;
            color: #f8fafc;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.88rem;
            line-height: 1.5;
        }

        .viva-box {
            background: #f0fdf4;
            border-left: 4px solid #16a34a;
            padding: 12px 16px;
            margin-bottom: 15px;
            border-radius: 0 8px 8px 0;
        }

        .viva-q {
            font-weight: 700;
            color: #15803d;
            margin-bottom: 4px;
        }

        .viva-a {
            color: #166534;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 0.9rem;
        }

        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            background: #f1f5f9;
            color: var(--primary-dark);
            font-weight: 600;
        }

        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 10px 0;
            border: 1px solid var(--border);
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: var(--text-muted);
            font-size: 0.85rem;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header-card">
        <h1>Digital Communication Laboratory</h1>
        <p><strong>Experiment 3:</strong> Sampling, Aliasing & Whittaker-Shannon Sinc Reconstruction</p>
        <p><strong>Student:</strong> Apurba Maity (Roll No: 34900324001)</p>
        <div class="badge">Study & Viva Reference Guide</div>
    </div>

    <div class="card">
        <h2>1. Core Python Libraries Explained Simply</h2>
        <p>Digital Signal Processing in Python uses 4 fundamental libraries instead of physical lab instruments:</p>
        
        <h3>NumPy (<code>import numpy as np</code>)</h3>
        <p>The fast math engine. It handles large arrays of numbers simultaneously (Vectorization). Used to create time axes, calculate sines, compute FFTs, and evaluate sinc matrices.</p>

        <h3>SciPy (<code>import scipy</code>)</h3>
        <p>The scientific toolbox for advanced statistics, filtering, and signal processing routines.</p>

        <h3>Matplotlib (<code>import matplotlib.pyplot as plt</code>)</h3>
        <p>The visual oscilloscope screen. Draws continuous signals, stem plots for discrete samples, and frequency magnitude spectra.</p>

        <h3>Pandas (<code>import pandas as pd</code>)</h3>
        <p>The data table formatter. Organizes test results into clean tables with headers.</p>
    </div>

    <div class="card">
        <h2>2. Key Functions & Code Breakdown</h2>
        
        <h3>Signal Definition</h3>
        <pre><code>def continuous_signal(t):
    return np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2 * np.pi * 300 * t)</code></pre>
        <p>Generates two sinusoidal tones: $f_1 = 100\text{ Hz}$ (1.0 V) and $f_2 = 300\text{ Hz}$ (0.5 V). Maximum frequency $f_{\max} = 300\text{ Hz} \implies f_{\text{Nyquist}} = 600\text{ Hz}$.</p>

        <h3>Whittaker-Shannon Sinc Reconstruction</h3>
        <pre><code>def sinc_reconstruction(sample_times, sample_values, t_fine, fs):
    dt_matrix = t_fine[None, :] - sample_times[:, None]
    sinc_matrix = np.sinc(fs * dt_matrix)
    return np.dot(sample_values, sinc_matrix)</code></pre>
        <p>Implements $\hat{x}(t) = \sum x[n] \operatorname{sinc}(f_s(t - n T_s))$. <code>np.sinc</code> computes $\frac{\sin(\pi x)}{\pi x}$, and <code>np.dot</code> performs instant matrix multiplication to sum overlapping sinc curves.</p>

        <h3>Spectral Aliasing Calculation</h3>
        <p>When undersampling at $f_s = 400\text{ Hz}$ ($f_s < 600\text{ Hz}$):</p>
        <p>$$f_{2,\text{alias}} = |f_2 - k f_s| = |300 - 1 \times 400| = 100\text{ Hz}$$</p>
        <p>The $300\text{ Hz}$ tone folds back into the $[0, 200\text{ Hz}]$ band and appears at <strong>100 Hz</strong>!</p>
    </div>

    <div class="card">
        <h2>3. Summary Results Table</h2>
        <table>
            <thead>
                <tr>
                    <th>Sampling Case</th>
                    <th>Sampling Rate ($f_s$)</th>
                    <th>Ratio ($f_s / f_{\text{Nyquist}}$)</th>
                    <th>MSE Error</th>
                    <th>Aliased $f_2$ Peak</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Oversampled</strong></td>
                    <td>1800 Hz</td>
                    <td>3.0x Nyquist</td>
                    <td>0.000005</td>
                    <td>300 Hz (No Alias)</td>
                </tr>
                <tr>
                    <td><strong>Critically Sampled</strong></td>
                    <td>600 Hz</td>
                    <td>1.0x Nyquist</td>
                    <td>0.123513</td>
                    <td>300 Hz (No Alias)</td>
                </tr>
                <tr style="background: #fef2f2;">
                    <td><strong style="color: var(--danger);">Undersampled</strong></td>
                    <td>400 Hz</td>
                    <td>0.67x Nyquist</td>
                    <td>0.250021</td>
                    <td><strong style="color: var(--danger);">100 Hz (Aliased!)</strong></td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="card">
        <h2>4. Predictive Viva Questions & Answers</h2>
        
        <div class="viva-box">
            <div class="viva-q">Q1: What is the Nyquist-Shannon Sampling Theorem?</div>
            <div class="viva-a">A signal with maximum frequency $f_{\max}$ can be perfectly reconstructed if sampled at $f_s \ge 2 f_{\max}$.</div>
        </div>

        <div class="viva-box">
            <div class="viva-q">Q2: What is Aliasing?</div>
            <div class="viva-a">High frequencies fold back into lower frequencies when $f_s < 2 f_{\max}$, distorting the reconstructed wave.</div>
        </div>

        <div class="viva-box">
            <div class="viva-q">Q3: How do real systems prevent aliasing?</div>
            <div class="viva-a">By placing an analog Low-Pass Anti-Aliasing Filter before the Analog-to-Digital Converter (ADC).</div>
        </div>

        <div class="viva-box">
            <div class="viva-q">Q4: Why does sinc interpolation work?</div>
            <div class="viva-a">The sinc pulse is the time-domain impulse response of an ideal brick-wall low-pass filter.</div>
        </div>
    </div>

    <div class="footer">
        Prepared by Ciel for Apurba Maity • Cooch Behar Government Engineering College
    </div>
</div>

</body>
</html>
"""

with open(HTML_PATH, "w") as f:
    f.write(html_content)
print("Created Mobile HTML Guide:", HTML_PATH)

# Convert HTML to PDF using LibreOffice
cmd = f"libreoffice --headless --convert-to pdf {HTML_PATH} --outdir {EXP3_DIR}"
subprocess.run(cmd, shell=True, check=True)

# Rename generated PDF to Digital_Comm_Exp3_Study_Guide.pdf if needed
gen_pdf = os.path.join(EXP3_DIR, "Python_and_DSP_Study_Guide_Exp3.pdf")
if os.path.exists(gen_pdf):
    os.rename(gen_pdf, PDF_PATH)

print("Created PDF Study Guide:", PDF_PATH)
