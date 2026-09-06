import os
import subprocess

exp_dir = "/home/apurba/Projects/Digital_Communication_Lab/Experiment_05_DPCM_and_Delta_Modulation"
tex_path = os.path.join(exp_dir, "Digital_Comm_Exp5_Study_Guide.tex")
pdf_path = os.path.join(exp_dir, "Digital_Comm_Exp5_Study_Guide.pdf")

tex_content = r'''\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[margin=1.8cm]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{hyperref}

% Define color palette
\definecolor{primary}{rgb}{0.11, 0.21, 0.36}      % Navy Blue
\definecolor{secondary}{rgb}{0.19, 0.51, 0.81}    % Slate Blue
\definecolor{accent}{rgb}{0.85, 0.42, 0.13}       % Amber/Orange
\definecolor{darktext}{rgb}{0.15, 0.20, 0.28}
\definecolor{lightbox}{rgb}{0.95, 0.97, 0.99}
\definecolor{codebg}{rgb}{0.94, 0.95, 0.97}

\hypersetup{
    colorlinks=true,
    linkcolor=secondary,
    filecolor=secondary,
    urlcolor=secondary
}

\renewcommand{\labelitemi}{$\bullet$}
\renewcommand{\labelitemii}{$\circ$}
\renewcommand{\labelitemiii}{$\diamond$}

\begin{document}

% Title Header Banner
\begin{center}
{\Large \textbf{\textcolor{primary}{COOCH BEHAR GOVERNMENT ENGINEERING COLLEGE}}}\\[1.5mm]
{\large Department of Electronics and Communication Engineering}\\[2.5mm]
{\Large \textbf{\textcolor{secondary}{Software-Based Digital Communication Laboratory (EC593 / EC592)}}}\\[2mm]
{\LARGE \textbf{Experiment 5: Differential PCM (DPCM), Delta Modulation (DM) \& Adaptive Delta Modulation (ADM)}}\\[2mm]
{\large \textbf{Comprehensive Theoretical, Mathematical \& Practical Study Guide}}\\[2.5mm]
\rule{\linewidth}{1.0pt}\\[2mm]
\small \textbf{Student Name:} Apurba Maity \quad \textbf{University Roll No.:} 34900324001 \quad \textbf{Semester:} 5th Sem ECE
\end{center}

\vspace{3mm}

\section{Introduction, Physical Foundations \& Source Redundancy}
In standard Pulse Code Modulation (PCM), each sampled analog value $x[n] = x(n T_s)$ is quantized and encoded independently of its neighbors. However, in almost all practical information signals---such as speech, acoustic music, physiological EEG/ECG waveforms, and physical sensor telemetry---the underlying physics dictates that amplitude variations cannot occur instantaneously. 

Consequently, when such signals are sampled at or above the Nyquist rate ($f_s \ge 2 f_{\max}$), adjacent samples exhibit exceptionally high statistical correlation:
\begin{equation}
\rho = \frac{E[x[n] x[n-1]]}{\sigma_x^2} = \frac{R_{xx}(1)}{R_{xx}(0)} \approx 0.85 - 0.98
\end{equation}

Transmitting each sample independently wastes critical transmission bandwidth and channel capacity on redundant information. To maximize information transmission efficiency without sacrificing fidelity, differential waveform encoding systems---namely \textbf{Differential Pulse Code Modulation (DPCM)}, \textbf{Linear Delta Modulation (DM)}, and \textbf{Adaptive Delta Modulation (ADM)}---exploit this inter-sample correlation by transmitting only the \textit{unpredictable new information} (the innovation or prediction residual).

\begin{center}
\fbox{\parbox{0.95\linewidth}{
\textbf{The Core Paradigm of Differential Modulation:}\\
Instead of quantizing the high-variance signal $x[n]$ ($\mathrm{Var}(x) = \sigma_x^2$), we compute an estimate $\hat{x}[n]$ based on past history and quantize only the prediction error residual:
\begin{equation*}
d[n] = x[n] - \hat{x}[n]
\end{equation*}
Because $\sigma_d^2 \ll \sigma_x^2$, the quantizer requires a significantly smaller dynamic range and fewer bits per sample, yielding a substantial \textbf{Prediction Gain ($G_p \approx 6 - 12\,\mathrm{dB}$)} that translates directly into bandwidth compression or enhanced Signal-to-Quantization-Noise Ratio (SQNR).
}}
\end{center}

\section{Differential Pulse Code Modulation (DPCM) Mathematical Architecture}

\subsection{Linear Prediction and Error Minimization}
Let $\hat{x}[n]$ be a linear combination of the $p$ previous reconstructed samples $\tilde{x}[n-k]$:
\begin{equation}
\hat{x}[n] = \sum_{k=1}^p a_k \tilde{x}[n-k]
\end{equation}
where $\{a_1, a_2, \dots, a_p\}$ are the optimal linear prediction coefficients. Assuming fine quantization ($\tilde{x}[n] \approx x[n]$), the mean squared prediction error is:
\begin{equation}
J = E[d^2[n]] = E\left[\left(x[n] - \sum_{k=1}^p a_k x[n-k]\right)^2\right]
\end{equation}

Setting the partial derivatives $\frac{\partial J}{\partial a_k} = 0$ for $k = 1, 2, \dots, p$ yields the classic \textbf{Wiener-Hopf (Yule-Walker) Equations}:
\begin{equation}
\sum_{k=1}^p a_k R_{xx}(|j - k|) = R_{xx}(j), \quad j = 1, 2, \dots, p
\end{equation}

For a first-order predictor ($p = 1$):
\begin{equation}
a_1 = \frac{R_{xx}(1)}{R_{xx}(0)} = \rho
\end{equation}
The resulting minimum prediction error variance is:
\begin{equation}
\sigma_d^2 = \sigma_x^2 (1 - \rho^2)
\end{equation}

\subsection{Proof of Non-Accumulation of Quantization Errors}
A fundamental question in differential encoding is whether quantization errors accumulate over time through the feedback loop. 

Let the quantizer introduce an additive quantization error $q[n] = d_q[n] - d[n]$. At the transmitter:
\begin{align}
d[n] &= x[n] - \hat{x}[n] \\
d_q[n] &= d[n] + q[n] \\
\tilde{x}[n] &= \hat{x}[n] + d_q[n] = \hat{x}[n] + (d[n] + q[n]) = (\hat{x}[n] + d[n]) + q[n] = x[n] + q[n]
\end{align}

The total overall reconstruction error is:
\begin{equation}
e[n] = x[n] - \tilde{x}[n] = -q[n] = -(d_q[n] - d[n])
\end{equation}
\textbf{Conclusion:} The overall system error is strictly bounded and identical to the instantaneous quantization error of that single sample. Quantization errors do \textbf{not} accumulate across samples because the feedback accumulator operates on $\tilde{x}[n]$ at both the encoder and decoder.

\subsection{Prediction Gain ($G_p$)}
The improvement in signal-to-noise ratio provided by DPCM over standard PCM is defined by the \textbf{Prediction Gain}:
\begin{equation}
G_p = \frac{\sigma_x^2}{\sigma_d^2} = \frac{1}{1 - \rho^2} \quad (\text{for } p = 1)
\end{equation}
In decibels:
\begin{equation}
G_{p,\mathrm{dB}} = 10 \log_{10}\left(\frac{1}{1 - \rho^2}\right)
\end{equation}
For telephone-band speech ($\rho \approx 0.90$):
\begin{equation}
G_p = \frac{1}{1 - (0.90)^2} = \frac{1}{1 - 0.81} = \frac{1}{0.19} \approx 5.26 \implies \mathbf{7.21\,\mathrm{dB}}
\end{equation}
Because every $6\,\mathrm{dB}$ corresponds to 1 bit of resolution, DPCM saves $\approx 1.2$ bits per sample compared to PCM for the same output quality.

\begin{figure}[h!]
\centering
\includegraphics[width=0.92\textwidth]{plots/fig1_dpcm_architecture_and_prediction_gain.png}
\caption{DPCM time-domain waveform execution: (a) Input $x[n]$ vs. 1st-order prediction $\hat{x}[n]$, (b) Unquantized prediction residual $d[n]$ exhibiting drastic variance reduction ($G_p = 7.18\,\mathrm{dB}$), (c) 3-bit mid-rise quantized residual $d_q[n]$, and (d) Final reconstructed signal $\tilde{x}[n]$.}
\label{fig:dpcm_arch}
\end{figure}

\section{Linear Delta Modulation (DM): Theory \& Noise Analysis}
Delta Modulation is the simplest 1-bit implementation of DPCM. The quantizer has only two output levels ($L = 2$): $\pm \Delta$. The transmitted bit stream is binary ($c[n] \in \{0, 1\}$).

\subsection{Transmitter and Receiver Equations}
At the transmitter:
\begin{align}
d[n] &= x[n] - \tilde{x}[n-1] \\
b[n] &= \mathrm{sgn}(d[n]) = \begin{cases} +1, & d[n] \ge 0 \\ -1, & d[n] < 0 \end{cases} \\
\tilde{x}[n] &= \tilde{x}[n-1] + \Delta \cdot b[n]
\end{align}
The transmission bit rate is directly equal to the sampling rate:
\begin{equation}
R_b = f_s \quad (\text{since } n = 1\text{ bit/sample})
\end{equation}

\subsection{The Two Fundamental Distortions in Linear DM}

\subsubsection{1. Slope Overload Distortion}
Slope overload occurs when the input signal changes faster than the maximum rate of change that the staircase accumulator can synthesize. 

The maximum slew rate of the DM staircase is:
\begin{equation}
\left(\frac{dx}{dt}\right)_{\mathrm{staircase}} = \frac{\Delta}{T_s} = \Delta \cdot f_s
\end{equation}
For a sinusoidal test signal $x(t) = A_m \sin(2\pi f_m t)$, the maximum slope is:
\begin{equation}
\left|\frac{dx(t)}{dt}\right|_{\max} = 2\pi f_m A_m = \omega_m A_m
\end{equation}

To completely eliminate slope overload distortion, the step size must satisfy:
\begin{equation}
\Delta \cdot f_s \ge 2\pi f_m A_m \implies \mathbf{\Delta \ge \frac{2\pi f_m A_m}{f_s}}
\end{equation}
If $\Delta < \frac{2\pi f_m A_m}{f_s}$, the staircase accumulator falls behind the rapid rising and falling edges, creating severe non-linear lag distortion.

\subsubsection{2. Granular (Idle-Channel) Noise}
Granular noise occurs when the input signal varies slowly or remains stationary ($|\dot{x}| \ll \Delta \cdot f_s$). Because the 1-bit quantizer can never output zero, the staircase must continuously toggle $+ \Delta$ and $- \Delta$ above and below the true signal level in a triangular hunting pattern.

Assuming the error is uniformly distributed over $[-\Delta, +\Delta]$, the granular noise power is:
\begin{equation}
N_g = \frac{(2\Delta)^2}{12} = \frac{\Delta^2}{3}
\end{equation}

\begin{figure}[h!]
\centering
\includegraphics[width=0.92\textwidth]{plots/fig2_dm_slope_overload_vs_granular_noise.png}
\caption{The fundamental linear Delta Modulation conflict: (a) Slope overload distortion when $\Delta < \Delta_{\mathrm{crit}}$, (b) Optimal step size $\Delta \approx \Delta_{\mathrm{crit}}$, and (c) Severe granular hunting noise when $\Delta > \Delta_{\mathrm{crit}}$.}
\label{fig:dm_noise}
\end{figure}

\section{Adaptive Delta Modulation (ADM): Jayant Algorithm}
Linear DM is trapped in an intractable design paradox: choosing a large $\Delta$ prevents slope overload on rapid transients but destroys quiet segments with excessive granular noise; choosing a small $\Delta$ quiets granular noise but causes catastrophic slope overload.

\textbf{Adaptive Delta Modulation (ADM)} eliminates this trade-off by making the step size $\Delta[n]$ time-varying and adaptive based on the recent output bit sequence.

\subsection{Jayant / Song Step Adaptation Rules}
The current step size $\Delta[n]$ is computed from the previous step size $\Delta[n-1]$ and the product of the current and previous output bits:
\begin{equation}
\Delta[n] = \Delta[n-1] \cdot M(b[n], b[n-1])
\end{equation}
where the step size multiplier $M$ is defined as:
\begin{equation}
M = \begin{cases} K_e, & \text{if } b[n] == b[n-1] \quad (\text{consecutive identical bits: slope overload}) \\ K_c, & \text{if } b[n] \ne b[n-1] \quad (\text{alternating bits: granular hunting}) \end{cases}
\end{equation}
with the constraints:
\begin{equation}
K_e > 1 \quad (\text{typically } 1.5), \qquad 0 < K_c < 1 \quad (\text{typically } 0.66), \qquad \Delta_{\min} \le \Delta[n] \le \Delta_{\max}
\end{equation}

\begin{figure}[h!]
\centering
\includegraphics[width=0.92\textwidth]{plots/fig3_adm_adaptive_tracking.png}
\caption{Adaptive Delta Modulation (ADM) performance: Upper panel illustrates superior dynamic tracking on both flat plateaus and steep $25\,\mathrm{V/s}$ ramps where linear DM fails. Lower panel displays the real-time adaptation of $\Delta[n]$.}
\label{fig:adm_tracking}
\end{figure}

\section{Reconstruction Filtering \& Oversampling SNR Scaling}

\subsection{The $(f_s)^3$ SNR Scaling Law}
In Delta Modulation, the quantization noise is spread uniformly across the entire Nyquist band from $0$ to $f_s / 2$. A low-pass reconstruction filter with cutoff $f_m \ll f_s / 2$ rejects all out-of-band noise beyond $f_m$.

The in-band quantization noise power is reduced by the Oversampling Ratio ($\mathrm{OSR} = \frac{f_s}{2 f_m}$):
\begin{equation}
N_{q,\mathrm{in-band}} = N_g \cdot \left(\frac{2 f_m}{f_s}\right) = \left(\frac{\Delta^2}{3}\right) \left(\frac{2 f_m}{f_s}\right)
\end{equation}

Substituting the optimal critical step size $\Delta = \frac{2\pi f_m A_m}{f_s}$:
\begin{equation}
N_{q,\mathrm{in-band}} = \frac{1}{3} \left(\frac{4\pi^2 f_m^2 A_m^2}{f_s^2}\right) \left(\frac{2 f_m}{f_s}\right) = \frac{8\pi^2 f_m^3 A_m^2}{3 f_s^3}
\end{equation}

Since the signal power is $P_s = A_m^2 / 2$, the output Signal-to-Noise Ratio is:
\begin{equation}
\mathrm{SNR}_{\mathrm{DM}} = \frac{P_s}{N_{q,\mathrm{in-band}}} = \frac{A_m^2 / 2}{\frac{8\pi^2 f_m^3 A_m^2}{3 f_s^3}} = \frac{3}{16\pi^2} \left(\frac{f_s}{f_m}\right)^3
\end{equation}
In decibels:
\begin{equation}
\mathrm{SNR}_{\mathrm{DM,dB}} = 10 \log_{10}\left(\frac{3}{16\pi^2}\right) + 30 \log_{10}\left(\frac{f_s}{f_m}\right)
\end{equation}

\noindent\textbf{Crucial Takeaway:} Doubling the oversampling frequency $f_s$ (one octave increase) yields:
\begin{equation}
\Delta \mathrm{SNR} = 30 \log_{10}(2) \approx \mathbf{9.03\,\mathrm{dB / octave}} \quad (\mathbf{30\,\mathrm{dB / decade}})
\end{equation}

\begin{figure}[h!]
\centering
\includegraphics[width=0.88\textwidth]{plots/fig4_dm_snr_vs_sampling_frequency.png}
\caption{Empirical vs. theoretical Delta Modulation SNR scaling with oversampling ratio ($OSR$). The empirical simulation tracks the theoretical $+9\,\mathrm{dB/octave}$ slope with high fidelity.}
\label{fig:dm_snr}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[width=0.88\textwidth]{plots/fig5_sqnr_comparison_pcm_dpcm_dm_adm.png}
\caption{Comprehensive SQNR benchmark comparison: DPCM provides a consistent $+7.5\,\mathrm{dB}$ advantage over standard PCM, while ADM provides robust performance across varying bitrates.}
\label{fig:sqnr_comp}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[width=0.88\textwidth]{plots/fig6_reconstruction_filtering_and_psd.png}
\caption{Frequency-domain power spectral density of DM bitstream and 4th-order Butterworth low-pass reconstruction filter output, confirming out-of-band noise rejection.}
\label{fig:psd_filter}
\end{figure}

\section{Comprehensive Viva-Voce Questions \& Detailed Model Answers}

\begin{enumerate}
    \item \textbf{Why does DPCM provide higher SQNR than standard PCM at the same bit rate?}\\
    \textit{Answer:} Natural information signals possess high autocorrelation ($\rho \approx 0.9$). DPCM uses linear prediction to subtract predictable redundancies, quantizing only the small innovation residual $d[n] = x[n] - \hat{x}[n]$. Because the residual has vastly smaller variance ($\sigma_d^2 \approx \sigma_x^2(1-\rho^2)$), a quantizer with identical bit-depth $n$ uses much smaller step sizes, yielding a Prediction Gain $G_p \approx 6 - 10\,\mathrm{dB}$ higher SQNR.

    \item \textbf{Why is local feedback decoding used inside the DPCM transmitter?}\\
    \textit{Answer:} If the transmitter predictor used the unquantized input $x[n]$, the receiver (which only has access to quantized values) would predict from reconstructed values $\tilde{x}[n]$. Any mismatch would cause quantization errors to accumulate over time. By incorporating the local feedback accumulator $\tilde{x}[n] = \hat{x}[n] + d_q[n]$ at the transmitter, the transmitter and receiver predictors remain locked in identical states, strictly preventing error accumulation.

    \item \textbf{Derive the condition to prevent slope overload in Delta Modulation.}\\
    \textit{Answer:} The maximum slope of input $x(t) = A_m \sin(2\pi f_m t)$ is $|dx/dt|_{\max} = 2\pi f_m A_m$. The maximum tracking slew rate of the DM staircase is $\Delta / T_s = \Delta \cdot f_s$. To track the signal without falling behind, the staircase slew rate must exceed the maximum signal derivative:
    $$\Delta \cdot f_s \ge 2\pi f_m A_m \implies \Delta \ge \frac{2\pi f_m A_m}{f_s}$$

    \item \textbf{Explain granular noise in Delta Modulation and state its power expression.}\\
    \textit{Answer:} Granular noise occurs when the input signal is flat or slow-moving ($|\dot{x}| \ll \Delta \cdot f_s$). The 1-bit quantizer can only step $+ \Delta$ or $- \Delta$, causing the staircase to hunt back and forth around the true level. Assuming the error is uniformly distributed over $[-\Delta, +\Delta]$, the granular noise power is $N_g = (2\Delta)^2 / 12 = \Delta^2 / 3$.

    \item \textbf{How does the Jayant algorithm in ADM detect slope overload vs. granular noise?}\\
    \textit{Answer:} By monitoring the output bitstream history:
    \begin{itemize}
        \item Two consecutive identical bits ($b[n] = b[n-1]$) signify that the signal is rising or falling steeply and the staircase is lagging $\implies$ step size expands: $\Delta[n] = \min(\Delta[n-1] \cdot K_e, \Delta_{\max})$.
        \item Two alternating bits ($b[n] \ne b[n-1]$) signify that the staircase is hunting above and below a flat signal $\implies$ step size contracts: $\Delta[n] = \max(\Delta[n-1] \cdot K_c, \Delta_{\min})$.
    \end{itemize}

    \item \textbf{Why does DM require an oversampling ratio $f_s \gg 2 f_m$?}\\
    \textit{Answer:} Because DM transmits only 1 bit per sample. To capture complex waveform shapes with fine resolution and avoid slope overload without needing huge step sizes, the sampling rate must be $20\times$ to $100\times$ the Nyquist rate. High oversampling spreads quantization noise over a wide frequency band, allowing an analog low-pass filter to eliminate the out-of-band noise.

    \item \textbf{What is the SNR scaling rate of Linear DM with oversampling frequency?}\\
    \textit{Answer:} Output SNR scales with the third power of sampling frequency: $\mathrm{SNR} \propto (f_s / f_m)^3$. In decibels, this equals $+30 \log_{10}(f_s)$, which corresponds to $\mathbf{9.03\,\mathrm{dB / octave}}$ (or $30\,\mathrm{dB / decade}$) of oversampling.

    \item \textbf{What is Continuously Variable Slope Delta Modulation (CVSD)?}\\
    \textit{Answer:} CVSD is an analog/digital implementation of ADM widely used in military communications (MIL-STD-188-113) and Bluetooth voice (SCO). It monitors a 3- or 4-bit shift register of transmitted bits. If the bits are all 1s or all 0s (run-length $\ge 3$), a syllabic low-pass filter charges, continuously expanding the integrator step size.

    \item \textbf{What is the transmission bandwidth of a DM system?}\\
    \textit{Answer:} In DM, $n = 1$ bit/sample, so the transmission bit rate is $R_b = f_s$ bits/second. The minimum transmission channel bandwidth (Nyquist criterion) is $B_{\min} = R_b / 2 = f_s / 2\,\mathrm{Hz}$.

    \item \textbf{Compare DPCM and ADM in terms of circuit complexity and error robustness.}\\
    \textit{Answer:} DPCM requires a multi-bit ADC, digital multiplier/adders for the linear predictor, and word framing, making it moderately complex. DM/ADM requires only a single analog comparator, a 1-bit D-flip-flop, and a simple RC or digital accumulator, making it extremely low-cost and compact. Additionally, DM is immune to bit-framing synchronization errors since every bit is an independent 1-bit delta step.
\end{enumerate}

\section{Conclusions \& Summary}
\begin{itemize}
    \item \textbf{Redundancy Reduction:} DPCM successfully exploits the high adjacent-sample correlation ($\rho \approx 0.90$) of physical signals via linear prediction, achieving $\approx 7.2\,\mathrm{dB}$ of Prediction Gain.
    \item \textbf{Linear DM Trade-off:} Linear DM is strictly constrained by the mutual exclusivity of slope overload ($\Delta < \frac{2\pi f_m A_m}{f_s}$) and granular noise ($N_g = \frac{\Delta^2}{3}$).
    \item \textbf{ADM Supremacy:} The Jayant ADM algorithm dynamically adapts $\Delta[n]$, eliminating slope overload during steep ramps while preserving low granular noise on plateaus.
    \item \textbf{Oversampling Fidelity:} Linear DM achieves $+9\,\mathrm{dB/octave}$ SNR scaling with sampling frequency when paired with a low-pass reconstruction filter.
\end{itemize}

\vspace{5mm}
\noindent\rule{\linewidth}{0.6pt}
\begin{center}
\small \textbf{Software-Based Digital Communication Laboratory (EC593 / EC592) \quad $\vert$ \quad Academic Record}\\
\textit{Master Engineering Study Guide compiled for Apurba Maity --- September 2026}
\end{center}

\end{document}
'''

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(tex_content)

print(f"LaTeX file written to {tex_path}")

cmd = ["pdflatex", "-interaction=nonstopmode", "-output-directory=" + exp_dir, tex_path]
print("Running pdflatex (Pass 1)...")
res1 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace")
if res1.returncode != 0:
    print("Pass 1 warning/log snippet:")
    print("\n".join(res1.stdout.splitlines()[-25:]))
print("Running pdflatex (Pass 2)...")
res2 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace")
if res2.returncode == 0:
    print(f"SUCCESS! Master PDF compiled at: {pdf_path}")
else:
    print("Pass 2 log snippet:")
    print("\n".join(res2.stdout.splitlines()[-25:]))

# Cleanup temporary artifacts per Rule 28
for ext in [".aux", ".log", ".out"]:
    aux_file = os.path.join(exp_dir, "Digital_Comm_Exp5_Study_Guide" + ext)
    if os.path.exists(aux_file):
        os.remove(aux_file)
        print(f"Cleaned temporary artifact: {aux_file}")
