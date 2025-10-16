# CITS4403-Project: Continuous-Space Infection Simulation

## Overview
A continuous-space agent-based infection model (ABM) built with **Mesa 3.3.0** and a live visualiser using **Pygame 2.6.1**.  
Agents move in a 2D plane, collide, and transmit infection probabilistically. The current model includes **vaccination** and **recovery** (SIRV-style dynamics).  
We provide a **Jupyter notebook** for batch experiments and a **real-time visualisation** for demonstrations.

---

## 1) Setup

```bash
cd CITS4403-Project
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
````

*(Optional – formatting on commit)*

```bash
pip install pre-commit
pre-commit install
```

---

## 2) How to Run

### A. Live visualisation (Pygame)

```bash
python -m src.main
```

A window opens:

* 🟨 Susceptible
* 🟥 Infected
* ⬜ Recovered
* 🟦 Vaccinated

Wait for no infected to remain in the simulation, or close the window to end.

### B. Batch experiments (Notebook)

```bash
jupyter lab notebooks/overview.ipynb
```

Run all cells to generate the figures present in `outputs/`.
The current vaccination-comparison plots in `outputs/` are:

* `0_vaccinated.png`
* `20_vaccinated.png`
* `60_vaccinated.png`
* `65_vaccinated.png`

For 0%, 20%, 60%, and 65% vaccination rates respectively.

---

## 3) Parameters

The following parameters are passed into the model from `src/main.py`:

* `num_people`, `initial_infected`, `vaccinated_rate`, `vaccinated_effect`, `recovered_effect`

More parameters may be adjusted by using the config types from `utils/config.py`:

* `width`, `height`, `speed`, `collision_radius`
* `contact_radius`, `frame_infection_prob`, `frame_recover_prob`
* `seed`

---

## 4) Project Layout

```
notebooks/
  overview.ipynb
outputs/
  0_vaccinated.png
  20_vaccinated.png
  60_vaccinated.png
  65_vaccinated.png
src/
  __init__.py
  agents.py
  model.py
  main.py
  visualisation.py
utils/
  __init__.py
  config.py
README.md
REPORT.md
requirements.txt
```

---

## 5) Example Outputs

The four PNGs under `outputs/` compare infection trajectories at different vaccination rates (0%, 20%, 60%, 65%).
Use the Pygame visualiser for live demonstrations and screenshots.
