# **CITS4403-Project: Continuous-Space Infection Simulation**

### **Overview**

This project implements a continuous-space agent-based infection model (ABM) using **Mesa 3.3.0** and **Pygame 2.6.1**.
Agents move in a 2D environment, interact through collisions, and transmit infection probabilistically.
The model supports interventions such as **social distancing**, **hygiene improvement**, **vaccination**, and **recovery**, forming a simplified **SIRV** dynamic system.

The repository includes both a **batch experiment mode** (for generating CSVs and plots) and a **live visualisation** (for real-time observation of infection spread).

---

## **1. Setup Instructions**

1. Ensure the current working directory is the project root.
2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. (Optional) Enable automatic formatting before each commit:

   ```bash
   pip install pre-commit
   pre-commit install
   ```

---

## **2. Usage Guide**

### **Run the Model (Batch Simulation)**

```bash
python -m src.experiments
```

This will:

* Run multiple infection scenarios (baseline, distancing, hygiene, vaccination, combined).
* Save per-scenario results in `outputs/` as `.csv` files.
* Generate plots:

  * `all_scenarios_infected.png`
  * `all_scenarios_susceptible.png`

---

### **Run Real-Time Visualisation**

```bash
python -m src.main
```

A Pygame window will open showing moving agents:

* 🟥 **Infected**
* 🟨 **Susceptible**
* 🟩 **Recovered**
* 🟦 **Vaccinated**

You can observe the spread and recovery in real time.
Close the window to end the simulation.

---

## **3. Parameters**

| Parameter           | Description                            | Typical Value |
| ------------------- | -------------------------------------- | ------------- |
| `N`                 | Total number of agents                 | 120           |
| `width`, `height`   | Simulation area                        | 100 × 100     |
| `speed`             | Movement speed                         | 1.0           |
| `infection_prob`    | Base probability of infection          | 0.35          |
| `collision_radius`  | Contact range                          | 3.0           |
| `hygiene_factor`    | Transmission modifier (<1 lowers risk) | 1.0 or 0.7    |
| `distancing_factor` | Scales collision radius                | 1.0 or 0.6    |
| `vaccinated_rate`   | Initial vaccinated proportion          | 0.5           |
| `vaccinated_effect` | Risk reduction for vaccinated          | 0.5           |
| `recovery_chance`   | Per-step chance of recovery            | 0.01          |
| `seed`              | Random seed                            | 42            |

All configuration constants are now stored in `utils/config.py` for clarity.

---

## **4. Project Structure**

```
CITS4403-Project/
├─ src/
│  ├─ agents.py              # Agent definitions and health logic
│  ├─ model.py               # InfectionModel implementation
│  ├─ main.py                # Visualisation entry point
│  ├─ experiments.py         # Batch simulation
│  └─ __init__.py
│
├─ notebooks/
│  └─ overview.ipynb         # Updated notebook with herd immunity analysis
│
├─ utils/
│  └─ config.py              # Centralised parameters and constants
│
├─ outputs/                  # Auto-generated results (CSVs and PNGs)
├─ requirements.txt
├─ .pre-commit-config.yaml   # Formatting config (black + isort)
└─ README.md
```

---

## **5. Example Output**

**Plots**

* `outputs/all_scenarios_infected.png`
* `outputs/all_scenarios_susceptible.png`
* `outputs/herd_immunity_comparison.png` 

**CSV Results**

* `outputs/baseline.csv`
* `outputs/distancing.csv`
* `outputs/better_hygiene.csv`
* `outputs/50%_vaccinated.csv`
* `outputs/combined.csv`

---

**Authors:**

* *Dominic Davies (23431003)* 
* *Jingwei Luo (23875736)* 
