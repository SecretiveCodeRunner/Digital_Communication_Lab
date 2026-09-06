import os
import subprocess

exp_dir = "/home/apurba/Projects/Digital_Communication_Lab/Experiment_06_Digital_Line_Coding_and_PSD"
tex_path = os.path.join(exp_dir, "Digital_Comm_Exp6_Study_Guide.tex")
pdf_path = os.path.join(exp_dir, "Digital_Comm_Exp6_Study_Guide.pdf")

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
{\LARGE \textbf{Experiment 6: Digital Line Coding Schemes \& Power Spectral Density (PSD) Analysis}}\\[2mm]
{\large \textbf{Comprehensive Theoretical, Mathematical \& Practical Study Guide}}\\[2.5mm]
\rule{\linewidth}{1.0pt}\\[2mm]
\small \textbf{Student Name:} Apurba Maity \quad \textbf{University Roll No.:} 34900324001 \quad \textbf{Semester:} 5th Sem ECE
\end{center}

\vspace{3mm}

\section{Introduction, Role in Baseband Transmission \& Design Criteria}
In digital communications, the binary output from a source encoder or PCM quantizer consists of an abstract sequence of discrete bits $\{b_n\} \in \{0, 1\}$. To transmit this information over a physical guided medium (such as twisted-pair copper telephone lines, coaxial cables, or backplane printed circuit board traces) without modulation onto a high-frequency carrier, the bits must be mapped directly into a continuous-time electrical voltage waveform $s(t)$. This process is termed \textbf{Digital Line Coding} or \textbf{Baseband Pulse Formatting}.

\subsection{The Six Fundamental Engineering Criteria for Line Code Selection}
The design and selection of a line code involves balancing six mutually interacting physical and architectural requirements:

\begin{enumerate}
    \item \textbf{DC Component Minimization ($S(0) = 0$):} Most long-distance transmission channels (such as telephone lines, Ethernet transformers, and capacitive repeaters) are AC-coupled. A non-zero DC voltage component causes continuous charge buildup across coupling capacitors and magnetic core saturation in transformers, resulting in \textbf{baseline wandering} and decision threshold slicing errors. A superior line code must have strictly zero energy at zero frequency ($f = 0$).
    \item \textbf{Self-Synchronization (Clock Extraction):} The receiver must reconstruct an exact, jitter-free bit sampling clock ($f = R_b$) directly from the incoming signal. The line code must guarantee sufficient transitions, even during prolonged sequences of identical bits (long runs of 0s or 1s).
    \item \textbf{Bandwidth Efficiency \& Spectral Compactness:} The power spectrum must be concentrated within a narrow bandwidth to prevent inter-symbol interference (ISI) in bandlimited channels and minimize cross-talk into adjacent cable pairs.
    \item \textbf{Error Detection Capability:} Physical-layer mechanisms that allow the receiver to recognize transmission bit errors (such as bipolar code violations or invalid state transitions) without adding parity or framing overhead.
    \item \textbf{Noise Immunity \& Bit Error Rate (BER):} The minimum Euclidean distance $d_{\min}$ between physical signaling states dictates immunity against additive white Gaussian noise (AWGN). Polar signaling ($d_{\min} = 2V$) provides a $3\,\mathrm{dB}$ power advantage over unipolar signaling ($d_{\min} = V$).
    \item \textbf{Transparency \& Implementation Cost:} The protocol must accept arbitrary user bit patterns without restriction, and the required transmitter/receiver hardware must be economically viable.
\end{enumerate}

\section{Mathematical Theory: Power Spectral Density of Random Pulse Trains}

\subsection{The Wiener-Khinchin Theorem for Cyclostationary Processes}
A random baseband pulse train is expressed as:
\begin{equation}
s(t) = \sum_{n=-\infty}^{\infty} a_n g(t - n T_b)
\end{equation}
where $\{a_n\}$ is a wide-sense stationary discrete random sequence with statistical autocorrelation $R(k) = E[a_n a_{n-k}]$, $g(t)$ is the basic pulse shape with Fourier transform $G(f) = \int_{-\infty}^{\infty} g(t) e^{-j 2\pi f t} \, dt$, and $T_b = 1 / R_b$ is the bit duration.

Because the statistical autocorrelation of $s(t)$ is periodic in $t$ with period $T_b$, $s(t)$ is a \textbf{cyclostationary random process}. To obtain the stationary Power Spectral Density $S(f)$, we compute the time-average autocorrelation function $\bar{R}_s(\tau)$ over one bit interval $T_b$:
\begin{equation}
\bar{R}_s(\tau) = \frac{1}{T_b} \int_{-T_b/2}^{T_b/2} R_s(t + \tau, t) \, dt = \frac{1}{T_b} \sum_{k=-\infty}^{\infty} R(k) \left[ g(\tau) * g(-\tau) * \delta(\tau - k T_b) \right]
\end{equation}

Applying the Fourier transform to $\bar{R}_s(\tau)$ yields the celebrated \textbf{Wiener-Khinchin Baseband Spectral Formula}:
\begin{equation}
\mathbf{S(f) = \frac{1}{T_b} |G(f)|^2 \sum_{k=-\infty}^{\infty} R(k) e^{-j 2\pi k f T_b}}
\end{equation}

Separating the symbol sequence into its mean $\mu_a = E[a_n]$ and autocovariance $C(k) = R(k) - \mu_a^2$:
\begin{equation}
S(f) = \underbrace{\frac{1}{T_b} |G(f)|^2 \sum_{k=-\infty}^{\infty} C(k) e^{-j 2\pi k f T_b}}_{S_c(f) \text{ (Continuous Spectrum)}} + \underbrace{\frac{\mu_a^2}{T_b^2} \sum_{m=-\infty}^{\infty} \left|G\left(\frac{m}{T_b}\right)\right|^2 \delta\left(f - \frac{m}{T_b}\right)}_{S_d(f) \text{ (Discrete Spectral Lines)}}
\end{equation}

\subsection{Step-by-Step Derivations for Core Line Codes}

\subsubsection{1. Polar Non-Return-to-Zero (Polar NRZ)}
\begin{itemize}
    \item Mapping: Bit 1 $\to +V$, Bit 0 $\to -V$, with equal probability $P(1) = P(0) = 0.5$.
    \item Pulse shape: $g(t) = \mathrm{rect}\left(\frac{t - T_b/2}{T_b}\right) \implies |G(f)|^2 = V^2 T_b^2 \,\mathrm{sinc}^2(f T_b)$.
    \item Mean: $\mu_a = 0.5(+V) + 0.5(-V) = 0$.
    \item Autocorrelation:
    \begin{align}
    R(0) &= E[a_n^2] = 0.5(+V)^2 + 0.5(-V)^2 = V^2 \\
    R(k) &= E[a_n] E[a_{n-k}] = 0 \quad (\text{for } k \ne 0)
    \end{align}
    \item Power Spectral Density:
    \begin{equation}
    \mathbf{S_{\mathrm{Polar\,NRZ}}(f) = V^2 T_b \,\mathrm{sinc}^2(f T_b)}
    \end{equation}
    \item \textit{Observations:} Completely continuous spectrum, zero discrete DC line, first spectral null at $f = R_b$.
\end{itemize}

\subsubsection{2. Unipolar Non-Return-to-Zero (Unipolar NRZ)}
\begin{itemize}
    \item Mapping: Bit 1 $\to +V$, Bit 0 $\to 0\,\mathrm{V}$, with $P(1) = P(0) = 0.5$.
    \item Mean: $\mu_a = 0.5(V) + 0.5(0) = V / 2$.
    \item Autocorrelation:
    \begin{equation}
    R(0) = 0.5(V^2) + 0 = \frac{V^2}{2}, \qquad R(k) = \mu_a^2 = \frac{V^2}{4} \quad (\text{for } k \ne 0)
    \end{equation}
    \item Covariance: $C(0) = R(0) - \mu_a^2 = \frac{V^2}{4}$, and $C(k) = 0$ for $k \ne 0$.
    \item Power Spectral Density:
    \begin{equation}
    \mathbf{S_{\mathrm{Unipolar\,NRZ}}(f) = \frac{V^2 T_b}{4} \,\mathrm{sinc}^2(f T_b) + \frac{V^2}{4} \delta(f)}
    \end{equation}
    \item \textit{Observations:} Contains a massive discrete DC delta impulse $\frac{V^2}{4} \delta(0)$ that consumes $50\%$ of total transmitted power without carrying any information!
\end{itemize}

\subsubsection{3. Bipolar Alternate Mark Inversion (AMI)}
\begin{itemize}
    \item Mapping: Bit 0 $\to 0\,\mathrm{V}$; Bit 1 $\to$ alternating $+V$ and $-V$.
    \item For equiprobable independent bits:
    \begin{align}
    R(0) &= E[a_n^2] = 0.5(0)^2 + 0.5(V^2) = \frac{V^2}{2} \\
    R(1) &= R(-1) = E[a_n a_{n-1}] = P(a_n = +V, a_{n-1} = -V)(-V^2) + \dots = -\frac{V^2}{4} \\
    R(k) &= 0 \quad (\text{for } |k| \ge 2)
    \end{align}
    \item Summation term:
    \begin{equation}
    \sum_{k=-\infty}^{\infty} R(k) e^{-j 2\pi k f T_b} = \frac{V^2}{2} - \frac{V^2}{4} e^{-j 2\pi f T_b} - \frac{V^2}{4} e^{j 2\pi f T_b} = \frac{V^2}{2} [1 - \cos(2\pi f T_b)] = V^2 \sin^2(\pi f T_b)
    \end{equation}
    \item Power Spectral Density:
    \begin{equation}
    \mathbf{S_{\mathrm{AMI}}(f) = V^2 T_b \,\mathrm{sinc}^2(f T_b) \sin^2(\pi f T_b)}
    \end{equation}
    \item \textit{Observations:} At $f = 0$, $\sin^2(0) = 0 \implies \mathbf{S(0) = 0}$. The DC component is strictly zero. Spectral nulls occur at both $f = 0$ and $f = R_b$, packing energy into a compact lobe around $R_b / 2$.
\end{itemize}

\subsubsection{4. Split-Phase / Manchester (IEEE 802.3 Ethernet)}
\begin{itemize}
    \item Mapping: Bit 1 $\to [+V \text{ for } T_b/2, -V \text{ for } T_b/2]$; Bit 0 $\to [-V \text{ for } T_b/2, +V \text{ for } T_b/2]$.
    \item Basic doublet pulse shape Fourier transform:
    \begin{equation}
    G(f) = \int_0^{T_b/2} V e^{-j 2\pi f t} \, dt - \int_{T_b/2}^{T_b} V e^{-j 2\pi f t} \, dt = j V T_b \,\mathrm{sinc}\left(\frac{f T_b}{2}\right) \sin\left(\frac{\pi f T_b}{2}\right)
    \end{equation}
    \item Power Spectral Density:
    \begin{equation}
    \mathbf{S_{\mathrm{Manchester}}(f) = V^2 T_b \,\mathrm{sinc}^2\left(\frac{f T_b}{2}\right) \sin^2\left(\frac{\pi f T_b}{2}\right)}
    \end{equation}
    \item \textit{Observations:} Strictly zero DC ($S(0) = 0$). Peak power occurs near $0.74 R_b$. The first null is pushed out to $f = 2 R_b$, requiring double the bandwidth of Polar NRZ.
\end{itemize}

\begin{figure}[h!]
\centering
\includegraphics[width=0.92\textwidth]{plots/fig1_line_coding_time_domain_waveforms.png}
\caption{Synchronized time-domain baseband waveforms across 6 line coding formats for the test bitstream $[1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]$.}
\label{fig:waveforms}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[width=0.90\textwidth]{plots/fig2_theoretical_psd_master_comparison.png}
\caption{Master analytical Power Spectral Density comparison: (a) Linear continuous envelopes highlighting DC impulse on Unipolar NRZ, and (b) Semi-logarithmic scale illustrating high-frequency roll-off and exact spectral nulls.}
\label{fig:psd_theory}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[width=0.88\textwidth]{plots/fig3_empirical_vs_theoretical_psd_validation.png}
\caption{Monte Carlo numerical Welch periodogram estimation ($N = 65,536$ random bits) overlaid on closed-form theoretical curves, validating exact mathematical convergence.}
\label{fig:psd_welch}
\end{figure}

\section{Channel Degradation: AC-Coupling \& Baseline Wandering}
When a baseband signal passes through an AC-coupled link (e.g., an isolation transformer or a series DC-blocking capacitor), the channel acts as a first-order high-pass filter with transfer function:
\begin{equation}
H(s) = \frac{s}{s + \frac{1}{R C}}
\end{equation}

When transmitting Unipolar NRZ, a run of consecutive 1s causes the capacitor to charge to $+V$, causing the voltage at the receiver load to decay exponentially toward zero:
\begin{equation}
v_{\mathrm{load}}(t) = V e^{-t / RC}
\end{equation}
When a 0 finally follows the long run of 1s, the load voltage plunges below zero to $-V(1 - e^{-T_{\mathrm{run}}/RC})$. The dynamic baseline wanders uncontrollably, causing the fixed zero-volt decision threshold to misclassify 1s as 0s (slicing errors). 

In contrast, \textbf{Bipolar AMI} and \textbf{Manchester} codes have strictly zero DC content ($\int s(t) dt = 0$), preserving a perfectly stationary baseline through transformers and blocking capacitors without any baseline droop.

\begin{figure}[h!]
\centering
\includegraphics[width=0.90\textwidth]{plots/fig4_baseline_wander_ac_coupling_transient.png}
\caption{Transient AC-coupling response during long runs of identical bits: (a) Unipolar NRZ exhibits catastrophic exponential baseline droop, while (b) Bipolar AMI and (c) Manchester remain perfectly centered.}
\label{fig:baseline_wander}
\end{figure}

\section{Clock Recovery Mechanics \& Eye Diagram Diagnostic Analysis}

\subsection{Bit Timing Clock Extraction}
Receiving digital bitstreams requires an accurate clock signal synchronized to the transmitted bit rate $R_b$. 
\begin{itemize}
    \item Line codes with discrete spectral lines at $f = R_b$ (such as Unipolar RZ) allow direct clock extraction by feeding the signal into a high-$Q$ resonant tank or bandpass filter centered at $f_0 = R_b$.
    \item Codes with continuous zero-mean spectra (such as Polar NRZ or Manchester) must first undergo a non-linear memoryless operation---such as a full-wave rectifier or squaring circuit $y(t) = s^2(t)$---which generates a strong discrete harmonic at $f = R_b$ that is subsequently locked onto by a Phase-Locked Loop (PLL).
\end{itemize}

\begin{figure}[h!]
\centering
\includegraphics[width=0.90\textwidth]{plots/fig5_clock_recovery_spectral_line_extraction.png}
\caption{Simulated clock recovery pipeline: (a) Baseband Unipolar RZ signal, (b) Extracted sinusoidal clock tone via high-$Q$ bandpass filter ($f_0 = R_b$), and (c) Regenerated decision sampling strobes.}
\label{fig:clock_recovery}
\end{figure}

\subsection{Eye Diagram Diagnostic Analysis}
An Eye Diagram is constructed by folding the received noisy waveform into overlapping $2 T_b$ segments synchronized to the symbol clock. Key diagnostic parameters include:
\begin{enumerate}
    \item \textbf{Eye Height (Vertical Aperture):} Directly proportional to the noise margin. Maximum opening defines the optimal decision threshold.
    \item \textbf{Eye Width (Horizontal Aperture):} Defines the timing jitter tolerance. A wider horizontal opening allows larger clock phase variations before ISI causes an error.
    \item \textbf{Transition Slope:} Indicates sensitivity to timing jitter. Steeper slopes mean small clock offsets produce large amplitude degradation.
    \item \textbf{Trace Thickness at Extremities:} Quantifies the magnitude of Inter-Symbol Interference (ISI) and additive channel noise.
\end{enumerate}

\begin{figure}[h!]
\centering
\includegraphics[width=0.90\textwidth]{plots/fig6_eye_diagram_and_noise_margin_analysis.png}
\caption{Eye diagram diagnostic comparison under additive channel noise and timing jitter: Left panel shows Polar NRZ with a wide vertical opening ($d_{\min} = 2V$), right panel shows Manchester with dual eye apertures.}
\label{fig:eye_diagram}
\end{figure}

\section{Comprehensive Viva-Voce Questions \& Detailed Model Answers}

\begin{enumerate}
    \item \textbf{What is the fundamental difference between Return-to-Zero (RZ) and Non-Return-to-Zero (NRZ) line coding?}\\
    \textit{Answer:} In NRZ, a symbol maintains its voltage level for the entire bit duration $T_b$. In RZ, the physical pulse returns to zero volts midway through the bit interval (at $T_b/2$). Consequently, RZ codes guarantee a transition within every active bit interval (facilitating clock extraction), but require twice the transmission bandwidth of their NRZ counterparts because their pulse width is halved ($T_p = T_b / 2$).

    \item \textbf{Why does Unipolar NRZ have poor power efficiency?}\\
    \textit{Answer:} Unipolar NRZ has a non-zero mean $\mu_a = V/2$. As proven by the Wiener-Khinchin theorem, its power spectrum contains a discrete impulse $\frac{V^2}{4}\delta(f)$ at zero frequency. This DC term consumes $50\%$ of the total transmitter power while carrying zero information, making Unipolar NRZ highly power-inefficient.

    \item \textbf{Why does Bipolar AMI eliminate DC content while Polar NRZ does not always do so?}\\
    \textit{Answer:} Polar NRZ only achieves zero DC if the sequence has an exact equal balance of 1s and 0s ($P(1) = P(0) = 0.5$). If the data stream contains an unbalanced sequence (e.g., $90\%$ ones), Polar NRZ develops a substantial DC bias. In contrast, Bipolar AMI alternates the polarity of every successive 1 ($+V, -V, +V, -V$), ensuring that the integral of the waveform approaches zero regardless of the bit statistics.

    \item \textbf{What is an ``AMI Code Violation'', and how is it used for in-service error detection?}\\
    \textit{Answer:} In Bipolar AMI, two consecutive pulses must always alternate in sign. If channel noise flips a 0 to a 1, or drops a bit, two consecutive pulses will appear with the same polarity (e.g., $+V$ followed immediately by $+V$). This is an illegal condition known as a \textbf{Bipolar Violation (BPV)}. The physical receiver detects BPVs immediately without needing frame headers or checksums, providing real-time in-service Bit Error Rate monitoring.

    \item \textbf{What is the primary weakness of Bipolar AMI, and how do practical systems (HDB3, B8ZS) fix it?}\\
    \textit{Answer:} If the input data contains a prolonged sequence of 0s, Bipolar AMI outputs continuous zero volts ($0\,\mathrm{V}$). The receiver clock extraction circuit starves for transitions and loses synchronization. High-density bipolar codes solve this by replacing strings of consecutive zeros with deliberate bipolar violation sequences:
    \begin{itemize}
        \item \textbf{HDB3 (High-Density Bipolar 3):} Replaces any run of 4 consecutive zeros with $000V$ or $B00V$.
        \item \textbf{B8ZS (Bipolar with 8-Zero Substitution):} Replaces 8 consecutive zeros with $000VB0VB$.
    \end{itemize}

    \item \textbf{Explain why Manchester code is extensively used in IEEE 802.3 10BASE-T Ethernet.}\\
    \textit{Answer:} Manchester code guarantees a voltage transition at the exact center of every single bit ($+V \to -V$ for 1, $-V \to +V$ for 0). This provides: (1) Guaranteed clock synchronization regardless of data content; (2) Strictly zero DC component, allowing cheap transformer isolation on twisted-pair Ethernet cables; and (3) Built-in error detection, as any bit interval lacking a mid-bit transition indicates a physical collision or line fault.

    \item \textbf{What is the main penalty incurred when using Manchester coding?}\\
    \textit{Answer:} The main penalty is bandwidth consumption. Because every bit has a forced transition at $T_b / 2$, the fundamental pulse duration is $T_b / 2$. Its first spectral null occurs at $f = 2 R_b$, requiring twice the transmission channel bandwidth of Polar NRZ or Bipolar AMI.

    \item \textbf{What causes Baseline Wandering in baseband transmission systems?}\\
    \textit{Answer:} Baseline wandering is caused by passing a signal with non-zero DC content through an AC-coupled channel (transformers, blocking capacitors, or high-pass repeater filters). The DC component charges the series capacitor, causing the baseline voltage to drift exponentially. This shifts the signal relative to the receiver's fixed decision threshold, causing severe bit slicing errors.

    \item \textbf{How does Differential Manchester differ from Standard Manchester?}\\
    \textit{Answer:} Standard Manchester defines logic 1 and 0 by the direction of the mid-bit transition (falling vs. rising). Differential Manchester defines bits by the \textbf{presence or absence of a transition at the start of the bit interval} (while retaining the mid-bit transition solely for clocking). This makes Differential Manchester completely polarity-insensitive; if the two copper wires of a twisted pair are inadvertently swapped, the data is still decoded correctly.

    \item \textbf{What information does the vertical and horizontal opening of an Eye Diagram convey?}\\
    \textit{Answer:} The vertical eye opening measures the \textbf{Noise Margin} (the maximum peak noise voltage the signal can withstand before a slicing error occurs). The horizontal eye opening measures the \textbf{Timing Jitter Tolerance} (the allowable clock phase uncertainty without causing an Inter-Symbol Interference error).
\end{enumerate}

\section{Conclusions \& Summary}
\begin{itemize}
    \item \textbf{DC Balance:} Line codes with strictly zero DC power ($S(0) = 0$), such as Bipolar AMI and Manchester, are essential for transformer-coupled and AC-isolated transmission links to prevent baseline wander.
    \item \textbf{Synchronization:} Manchester code provides unbeatable clock synchronization through guaranteed mid-bit transitions at the cost of double the bandwidth ($B_{\min} = R_b$).
    \item \textbf{Error Detection:} Bipolar AMI provides zero DC content and in-service error detection via bipolar violations within a compact bandwidth ($B_{\min} = R_b / 2$).
    \item \textbf{Eye Diagram Utility:} Eye diagrams provide an indispensable diagnostic tool for simultaneously visualizing noise margins, timing jitter vulnerability, and ISI degradation in digital communication transceivers.
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
    aux_file = os.path.join(exp_dir, "Digital_Comm_Exp6_Study_Guide" + ext)
    if os.path.exists(aux_file):
        os.remove(aux_file)
        print(f"Cleaned temporary artifact: {aux_file}")
