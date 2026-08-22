# Experiment 4: Uniform Quantization and Pulse Code Modulation (PCM)
**Department of Electronics and Communication Engineering**  
**Cooch Behar Government Engineering College**  
**Student Name:** Apurba Maity | **Roll Number:** `34900324001` | **Subject:** EC593 Software-Based Digital Communication Lab  

---

## 1. Overview
This directory contains the Python simulation, publication figures, Jupyter Notebook report, and presentation & study guide PDFs for **Experiment 4: Uniform Quantization and PCM**.

---

## 2. Directory Structure & Key Files

```
Experiment_04_Uniform_Quantization_and_PCM/
├── experiment_04.py                      # Python simulation & validation script (generates all 4 figures)
├── Experiment_04_Lab_Report.ipynb        # Academic Jupyter Notebook with code & theory
├── VIDEO_PRESENTATION_SCRIPT.md          # Scene-by-scene presentation narration & viva Q&A
├── Experiment_04_Presentation_Script.pdf # Compiled presentation script PDF
├── Experiment_04_Presentation_Script.tex # LaTeX source for presentation script
├── Digital_Comm_Exp4_Study_Guide.pdf     # 8-page comprehensive study guide PDF
├── Digital_Comm_Exp4_Study_Guide.tex     # LaTeX source for study guide
├── index.html                            # Interactive PCM Web Studio
├── build_notebook.py                     # Jupyter notebook generator script
├── plots/                                # Publication-quality 300 DPI figures
│   ├── exp4_original_vs_quantized_waveforms.png
│   ├── exp4_quantizer_staircase_characteristics.png
│   ├── exp4_quantization_error_and_pdf.png
│   └── exp4_sqnr_vs_bit_resolution.png
└── README.md
```

---

## 3. How to Run

```bash
# 1. Run Python simulation & regenerate all figures
python3 experiment_04.py

# 2. Compile LaTeX PDFs (if edited)
pdflatex -interaction=nonstopmode Experiment_04_Presentation_Script.tex
pdflatex -interaction=nonstopmode Digital_Comm_Exp4_Study_Guide.tex
rm -f *.aux *.log *.out

# 3. Open Jupyter Notebook
jupyter notebook Experiment_04_Lab_Report.ipynb
```
