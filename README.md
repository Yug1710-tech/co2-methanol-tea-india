
<div align="center">

# 🧪 CO₂-to-Green Methanol
## 🇮🇳 India-Specific Techno-Economic Assessment

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](tests/)

**Thermodynamic Analysis & Techno-Economic Assessment of CO₂ Hydrogenation to Green Methanol**  
*100,000 t/yr Plant | Dahej SEZ, Gujarat, India*

[🚀 Quick Start](#quick-start) · [📊 Results](#key-results) · [📁 Data](data/) · [📖 Citation](#citation)

</div>

---

## 🎯 What Is This?

This repository contains the **complete simulation framework** 🔬 for a bottom-up techno-economic study that asks one critical question:

> *Can India produce green methanol from captured CO₂ and renewable hydrogen at a cost that makes business sense?*

**The answer: Yes — but only with the right policy support.** ⚡

At current hydrogen prices ($3.50/kg), the project loses money 💸. But if India hits its **National Green Hydrogen Mission target** of $1.00/kg hydrogen by 2030, green methanol becomes **cheaper than imported fossil methanol** — and permanently locks away **1.3 tonnes of CO₂ for every tonne produced** 🌱.

### 👥 For Different Readers

| If you are... | Start here | Why |
|--------------|-----------|-----|
| 🔧 **Chemical Engineer** | [`src/equilibrium.py`](src/equilibrium.py) | Rigorous thermodynamic solver with NIST Shomate data |
| 🏛️ **Policy Maker** | [`data/ists_scenarios.csv`](data/ists_scenarios.csv) | ISTS waiver impact quantified in dollars |
| 💰 **Investor / Banker** | [`src/economics.py`](src/economics.py) | NPV, IRR, DSCR — bankability metrics |
| 📈 **Data Scientist** | [`src/montecarlo.py`](src/montecarlo.py) | 10,000-trial uncertainty quantification |
| 🔍 **Reviewer** | [`tests/test_all.py`](tests/test_all.py) | 20+ validation tests against literature |
| 🎓 **Student** | This README | Everything explained step by step |

---

## 📊 Key Results

### 💡 The Bottom Line

| Scenario | Cost per Tonne | Project Viable? |
|----------|---------------|-----------------|
| Today (no policy help) | **$1,127/t** | ❌ No — loses $108M |
| With ISTS transmission waiver | **$752/t** | ✅ Yes — earns $211M |
| At NGHM 2030 hydrogen target | **$502/t** | ✅ Strongly yes — earns $424M |
| Fossil methanol (imported) | ~$346/t | Baseline comparison |
| Marine fuel premium | ~$1,000/t | Target market today |

### 🏆 The Headline Number

**Breakeven hydrogen price for commodity methanol: $0.37/kg**

India's NGHM target: $1.00/kg by 2030.  
**Headroom: $0.63/kg below target.** This is not marginal — it is robust 💪.

### 🇮🇳 Why This Matters for India

- India imports **88%** of its methanol, mostly from the Middle East 🌍
- The Dahej-Hazira corridor has **9.57 million tonnes/year** of capturable CO₂ within 100 km 🏭
- The ISTS (inter-state transmission) waiver alone **restores project bankability** — DSCR jumps from 0.38 → 3.43 📈
- Green methanol is **carbon-negative**: **−1.304 t CO₂ per tonne produced** (solar power) ☀️

### ⚔️ Green Methanol vs. Green Ammonia

| Factor | 🧪 Green Methanol | 🌿 Green Ammonia | Winner |
|--------|------------------|------------------|--------|
| Carbon intensity | **−1.304 t CO₂/t** | +0.143 t CO₂/t | 🧪 |
| Marine fuel market | **Established (60+ vessels)** | Speculative | 🧪 |
| Port infrastructure | Standard terminal ($2M) | Cryogenic ($15M) | 🧪 |
| Safety | Flammable (Class 3) | **Toxic (Class 2.3)** | 🧪 |
| Indian manufacturing | **Full domestic capability** | 80% import-dependent | 🧪 |

> **Policy implication:** 🏛️ NGHM Phase II should explicitly include methanol synthesis subsidies, not just ammonia.

---

## 🚀 Quick Start

### ⚡ Install (2 minutes)

```bash
git clone https://github.com/YOUR-USERNAME/co2-methanol-tea-india.git
cd co2-methanol-tea-india
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

### ▶️ Run the Solvers

```bash
# Thermodynamic equilibrium at 250°C, 50 bar
python -m src.equilibrium

# Coupled adiabatic reactor (temperature rise + equilibrium)
python -m src.adiabatic

# Full economic model
python -m src.economics

# Monte Carlo uncertainty (10,000 trials)
python -m src.montecarlo
```

### 📈 Generate Figures

```bash
python src/fig1_keq.py        # Equilibrium constants vs temperature
python src/fig2_contour.py     # CO₂ conversion contour map
python src/fig6_tornado.py     # Sensitivity analysis
python src/fig8_montecarlo.py  # NPV probability distribution
python src/fig9_recycle.py     # Recycle ratio optimization
```

All figures save to `figures/` as **PNG (300 DPI)** and **PDF**.

---

## 📁 Repository Structure

```
co2-methanol-tea-india/
|
├── 📂 data/                          # All paper data as CSV
│   ├── shomate_coefficients.csv          # Table 1: NIST thermodynamic data
│   ├── equipment_costs.csv               # Table 8: Capital cost breakdown
│   ├── opex_breakdown.csv                # Table 9: Operating costs
│   ├── stream_table.csv                  # Table 6: Process streams
│   ├── validation_points.csv             # Table 2: Literature validation
│   ├── ists_scenarios.csv                # Table 17: Policy scenarios
│   ├── monte_carlo_distributions.csv     # Table 15: Input distributions
│   ├── carbon_intensity.csv              # Table 13: Carbon balance
│   ├── methanol_vs_ammonia.csv           # Table 19: Strategic comparison
│   └── capex_summary.csv                 # Capital cost roll-up
|
├── 📂 src/                           # Core Python solvers
│   ├── __init__.py
│   ├── equilibrium.py             # Thermodynamic model (Newton-Raphson)
│   ├── adiabatic.py               # Coupled reactor solver
│   ├── economics.py               # Cost estimation & profitability
│   ├── montecarlo.py              # Uncertainty quantification
│   ├── utils.py                   # Helpers
│   ├── fig1_keq.py                # Figure scripts
│   ├── fig2_contour.py
│   ├── fig6_tornado.py
│   ├── fig8_montecarlo.py
│   └── fig9_recycle.py
|
├── 📂 tests/                       # Validation tests
│   ├── __init__.py
│   └── test_all.py                # 20+ tests against paper & literature
|
├── 📂 figures/                     # Generated output
|
├── 📂 .github/workflows/           # CI/CD
│   └── tests.yml                  # Automated testing on every push
|
├── .gitignore
├── LICENSE                         # MIT License
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── setup.py                        # Package installation
```

---

## 🔬 The Science: How It Works

### ⚗️ Reaction Chemistry

CO₂ captured from industrial sources reacts with green hydrogen over a copper catalyst:

```
CO2 + 3H2  ->  CH3OH + H2O        # main reaction (releases heat)
CO2 + H2   ->  CO + H2O           # side reaction (absorbs heat)
```

**The problem:** The main reaction likes **low temperature** ❄️, but the side reaction (RWGS) accelerates as temperature rises 🔥. In a real adiabatic reactor, the heat released pushes temperature up — **slashing methanol selectivity from 66% → 50%**. This is a **central finding** of this work 🎯.

### 📐 Thermodynamic Model

- Uses **NIST Shomate equations** for heat capacity, enthalpy, and entropy
- Solves two coupled nonlinear equations via **Newton-Raphson** (converges in 5–7 iterations)
- Validated against **4 independent literature sources** with **2.3% mean deviation** ✅

### 🏭 Reactor Design

| Parameter | Value |
|-----------|-------|
| Type | Vertical adiabatic fixed-bed |
| Catalyst | Cu/ZnO/Al₂O₃ (BASF S3-85) |
| Operating | 250°C inlet → 268°C outlet, 50 bar |
| Modules | 6 parallel reactors |
| Capacity | **100,000 tonnes/year** |

### ♻️ Heat Integration

A **feed-effluent heat exchanger** recovers **900 kW** of waste heat, eliminating all external heating for feed preheating. Payback: **1.3 years** 💰.

### 💵 Economics

| Item | Cost |
|------|------|
| Total Capital Investment | **$55.2 million** |
| Annual OPEX | **$106.2 million** |
| Hydrogen share of OPEX | **82.3%** 🔴 |
| Levelised Cost of Methanol | **$1,127/tonne** |

With ISTS waiver: **LCOM drops to $752/tonne** 🟢.

### 🎲 Uncertainty Analysis

10,000 Monte Carlo trials reveal:
- **29% chance** of positive NPV at baseline
- Hydrogen price is the **dominant risk factor** (Spearman ρ = −0.64) 🔴
- Capital cost uncertainty is almost irrelevant (ρ = −0.18) ⚪

> **💡 Takeaway:** Secure long-term hydrogen supply contracts, not construction guarantees.

---

## 📊 Data

Every number in the paper is available as a **machine-readable CSV** in `data/`:

| File | What It Contains |
|------|-----------------|
| `shomate_coefficients.csv` | A–E coefficients for 6 species |
| `equipment_costs.csv` | 11 equipment items with India location factors |
| `opex_breakdown.csv` | 6 cost categories, H₂ dominates at 82.3% |
| `stream_table.csv` | 11 process streams, mass flows, T, P, phase |
| `validation_points.csv` | 4 literature data points for verification |
| `ists_scenarios.csv` | 4 policy scenarios with dollar impacts |
| `monte_carlo_distributions.csv` | 7 input distributions with parameters |
| `carbon_intensity.csv` | Solar vs grid electricity carbon balance |
| `methanol_vs_ammonia.csv` | 16-criterion strategic comparison |
| `capex_summary.csv` | Roll-up from equipment to total investment |

---

## 🖼️ Figures

### What We Provide

| Script | Output | What It Shows |
|--------|--------|---------------|
| `fig1_keq.py` | Fig 1 | Equilibrium constants vs temperature |
| `fig2_contour.py` | Fig 2 | CO₂ conversion across T–P space |
| `fig6_tornado.py` | Fig 6 | Which parameters most affect economics |
| `fig8_montecarlo.py` | Fig 8 | NPV probability distribution |
| `fig9_recycle.py` | Fig 9 | How recycle ratio affects profit |

### 🎨 About Our Figures

> **Transparency note:** The publication-quality figures in the manuscript were generated using **AI-assisted visualization tools** (Figure Labs, SciFig) for final polish, using **exact numerical data** from the solvers in this repository. The underlying data and all numerical results are **fully reproducible** from the Python code provided here.
>
> The matplotlib scripts in `src/` generate verification plots that match the same data. Researchers who prefer open-source workflows can reproduce all trends independently.

---

## ✅ Testing

```bash
python -m pytest tests/ -v
```

Tests validate:
- ✅ Thermodynamic properties against NIST data
- ✅ Equilibrium conversions against 4 literature sources (Portha, Graaf, Pérez-Fortes)
- ✅ Adiabatic outlet temperature and selectivity penalty
- ✅ Economic calculations (CRF, LCOM, NPV, breakeven)
- ✅ Monte Carlo reproducibility and statistical properties

---

## 📖 Citation

```bibtex
@article{soni2026greenmethanol,
  title={Thermodynamic Analysis and Techno-Economic Assessment of 
         CO2 Hydrogenation to Green Methanol: An India-Specific 
         Study with Policy Implications},
  author={Soni, Yug},
  year={2026}
}
```

```bibtex
@software{soni2026co2methanolcode,
  author = {Soni, Yug},
  title = {CO2-to-Green Methanol: India-Specific TEA},
  url = {https://github.com/YOUR-USERNAME/co2-methanol-tea-india},
  year = {2026},
  version = {1.0.0}
}
```

---

## 📧 Contact

**Yug Soni**  
Department of Chemical Engineering  
Sardar Vallabhbhai National Institute of Technology (SVNIT), Surat, India  
📧 U23CH077@ched.svnit.ac.in

---

<div align="center">

⭐ **Star this repository if you find it useful!**


</div>
```
