# **Simulation of Infection Spread Using a Continuous-Space Agent-Based Model**

**Team Members:** Dominic Davies (23431003), Jingwei Luo (23875736)
**Date Submitted:** 13 October 2025

**Libraries**: Python 3.13, Mesa 3.3.0, Matplotlib, Pandas (visualisation branch uses Pygame)

------

## **1. Introduction**

This project presents an agent-based model (ABM) that simulates the spread of an infectious disease within a dynamic population. The model aims to demonstrate how interventions—such as vaccination—affect infection dynamics in a simple but interpretable system.

Unlike traditional SIR models that treat populations as homogeneous, the ABM framework explicitly represents individuals as autonomous agents moving in continuous space. This allows direct modelling of local interactions, stochastic transmission, and spatial clustering, offering more realistic insights into how microscopic contacts produce macroscopic epidemic outcomes.

The system comprises two complementary components: a batch simulation framework that runs experiments and outputs quantitative results, and a real-time visualisation developed using **Pygame**, which provides intuitive validation of model logic and agent behaviour. The project is implemented in **Python 3.13** using **Mesa 3.3.0**, **Matplotlib**, and **Pandas**, designed for clarity, modularity, and reproducibility.

------

## **2. Model Design**

### **2.1 Agent Representation**

Each agent represents a person capable of movement, contact, and infection. Agents possess the following core attributes:

1. **Position** in continuous 2D space (`pos`)
2. **Velocity** (direction and magnitude)
3. **Health state**: `SUSCEPTIBLE`, `INFECTED`, `RECOVERED` or `VACCINATED`

At each simulation step, agents move and check for neighbours within a contact radius. If a susceptible agent encounters an infected one, transmission may occur with a certain probability. Upon crossing the edge of the simulation, the agent wraps around to the opposite side, causing the space to act like a torus. The choice of torus-shaped space leads to behaviour akin to a busy town square with many people trying to move in different directions.

------

### **2.2 Movement and Space**

The model operates within a **ContinuousSpace**, a finite area with wraparound boundaries. Agents maintain constant speed in random directions which emulates movement in a busy environment, such as a building or community area.

Neighbourhood detection uses Mesa’s spatial index, where each agent retrieves neighbours within a **collision radius**. This radius defines a physical collision distance. The infection **contact range** is stored separately, and only slightly larger than the collision radius by default.

------

### **2.3 Infection Process**

During each step:

1. Each agent updates its position based on velocity.
2. If a susceptible agent finds an infected neighbour within `collision_radius`, infection occurs with probability:
    $P_{infect} = infection_prob \times (1 - vaccinated_effect | recovered_effect)$

where:

- `infection_prob` is the base probability of infection per contact,
- `vaccinated_effect` reduces infection risk for vaccinated individuals.
- `recovered_effect` also reduces infection risk for those that have recovered from the infection.

------

### **2.4 Scheduling and Randomness**

The model uses Mesa’s **shuffle_do("step")** function, ensuring agents are updated in random order each step. This prevents systematic bias caused by fixed update sequences.

The simulation terminates when all susceptible agents have been infected. Random seeds are fixed to guarantee reproducibility across runs.

------

### **2.5 Data Collection**

A `DataCollector` tracks model-level variables:

- Number of **Susceptible** agents
- Number of **Infected** agents
- Number of **Recovered** agents
- Number of **Vaccinated** agents

This data is stored as CSV files and plotted to show how infection, susceptibility, and recovery evolves over time.

------

## **3. Parameters and Scenarios**

### **3.1 Model Parameters**

| Parameter             | Symbol  | Description                                        |
| --------------------- | ------- | -------------------------------------------------- |
| Population size       | N       | Total number of agents                             |
| Simulation area       | W × H   | Continuous 2D space                                |
| Agent speed           | v       | Distance moved per step                            |
| Collision radius      | r₍c₎    | Range for physical collision                       |
| Contact radius        | r₍d₎    | Range for infection contact                        |
| Infection probability | p₍inf₎  | Infection probability per frame while in contact   |
| Recovery probability  | p₍rec₎  | Recovery probability per frame while in contact    |
| Vaccination rate      | v₍rate₎ | Fraction initially vaccinated                      |
| Vaccine effect        | v₍veff₎ | Infection reduction for vaccinated                 |
| Recovery effect       | v₍reff₎ | Infection reduction for recovered                  |
| Random seed           | s       | Ensures reproducibility                            |

------

### **3.2 Experimental Scenarios**

| Scenario       | Parameter Change | Interpretation                              |
| -------------- | -----------------| ------------------------------------------- |
| Baseline       | 0% vaccinated    | Infection explosion for comparison          |
| 20% Vaccinated | 20% vaccinated   | Slightly better protection, still explosion |
| 60% Vaccinated | 60% vaccinated   | Just before full herd immunity effect       |
| 65% Vaccinated | 65% vaccinated   | Just after full herd immunity effect        |

> ![60_vaccinated](/Users/leonce/Desktop/CITS4403-Project/outputs/60_vaccinated.png)
> ![65_vaccinated](/Users/leonce/Desktop/CITS4403-Project/outputs/65_vaccinated.png)

------

## **4. Results**

The experiments reveal the trend of *herd immunity* across scenarios with increasing vaccination rates. Each increase in vaccination rate affects the *speed* and *extent* of infection spread, and the arise of herd immunity demonstrates how stopping an epidemic at its critical infection point may shape its overall outcome greatly.

1. In the **baseline** scenario, infections grow rapidly after a short delay. The number of infected agents increases steadily before reaching a maximum and falling again as most susceptible individuals recover. This quadratic curve confirms the expected behaviour of transmission reaching a maximum in a closed system before dropping as people become immune.

    > ![0_vaccinated](/Users/leonce/Desktop/CITS4403-Project/outputs/0_vaccinated.png)

2. Introducing a **vaccination rate** of *20%* slows the infection process. Reduced susceptible people lowers the rate of infectious encounters, slighlty squashing the infection curve and extending the time to reach saturation. Though the final infection count remains high, the slower progression illustrates the “flatten the curve” phenomenon.

    > ![20_vaccinated](/Users/leonce/Desktop/CITS4403-Project/outputs/20_vaccinated.png)

3. Increasing the **vaccination rate** to *60%* reduces transmission probability much more than *20%*. The resulting curve remains even lower throughout, indicating fewer successful transmissions. The general trend of the infection line unexpectedly shows two maximums. This could be caused by the infection beginning in a small area of infection, then finally making it to the rest of the space before running out of new people to spread to. Herd immunity is not quite being reached in this scenario with the number of infected people still soaring.

    > ![60_vaccinated](/Users/leonce/Desktop/CITS4403-Project/outputs/60_vaccinated.png)

4. At a **vaccination rate** of *65%*, the scenario exhibits a significant decline in both infection rate and total infections. The trend of the infection line makes it nowhere near the susceptible line for the first time. Only *22%* of the susceptible population became infected, representing a simplified manifestation of *herd immunity* that greatly limits outbreak growth.

    > ![65_vaccinated](/Users/leonce/Desktop/CITS4403-Project/outputs/65_vaccinated.png)

The visual behaviour aligns with data results: dense infection clusters emerge in the baseline, while spread remains contained under higher vaccination rates. This consistency between visual and statistical outcomes reinforces the accuracy of our model's logic.

## **5. Discussion**

### **5.1 Model Evaluation**

The model demonstrates coherent internal logic and consistent sensitivity across its parameters. Variations in geometry or infection probability produce predictable and interpretable effects: higher vaccination rates flatten infection curves, leading to herd immunity that yields the strongest suppression.

The design is compact yet modular. The implementation provides a transparent mapping between vaccination rate and emergent outcomes. The use of ContinuousSpace avoids lattice artefacts, and the random step function ensures fairness in agent updates.

The reproducibility of results, achieved through fixed seeds, allows transparent verification and replication by others.

------

### **5.2 Sensitivity Analysis**

Three groups of parameters govern system dynamics:

1. **Geometric parameters** – including `collision_radius`, `distancing_factor`, and population density (`N / area`), determine encounter frequency.
2. **Probabilistic parameters** – `infection_prob`, `recovery_prob`, and `vaccinated_effect`, control infection likelihood per contact.
3. **Initial conditions** – `initial_infected` and `vaccinated_rate`, influence early acceleration and final outbreak size.

Simulation results show consistent qualitative behaviour: increasing vaccination rates suppresses infection curves, and herd immunity maximises this mitigation effect.

------

### **5.3 Validity and Limitations**

Despite its simplicity, the model has several limitations that constrain realism:

1. **Homogeneous agents:** identical movement speeds and behaviours omit variability in compliance or susceptibility.
2. **Discrete-time simulation:** fixed time steps standardise exposure duration, limiting fine-grained temporal analysis.
3. **Slow performance with intensive loads:** increasing the number of agents into the thousands immediately brings about slow-downs.

These limitations are deliberate trade-offs to prioritise transparency and computational efficiency over biological detail.

------

### **5.4 Extensibility**

The modular architecture allows straightforward extensions:

1. Assign heterogeneous speeds or compliance levels.
2. Add social clustering or barriers to represent environmental structure.
3. Record contact networks for statistical or epidemiological analysis.

Such additions could increase realism while preserving interpretability and educational value.

**Note on Code Maintenance:**
 A subsequent pull request introduced automated code formatting using *Black* and *isort* via *pre-commit*. This ensures consistent style and import order across all Python files without altering functionality.

------

## **6. Conclusion**

A continuous-space agent-based model was developed to simulate infection spread under different rates of vaccination. The results demonstrate that *herd immunity* slows the rate of transmission the most, which high vaccination rates are able to bring about to produce a strong suppression effect.

The inclusion of visualisation and reproducible experiments highlights how simple, individual-level rules can produce complex, emergent epidemic dynamics. The project’s modular structure and clear outputs make it a strong foundation for future work on networked populations, and adaptive behaviours.

------

## **Appendix A. Reproducibility**

### **A.1 Environment**

Python 3.13

Mesa 3.3.0

Pandas 2.3.3

Matplotlib 3.10

Pygame 2.6.1

### **A.2 File Structure**

```text
CITS4403-Project/
  ├─ src/
  │   ├─ agents.py
  │   ├─ main.py
  │   ├─ model.py
  │   ├─ visualisation.py
  │   └─ __init__.py
  ├─ notebooks/
  │   └─ overview.ipynb
  ├─ outputs/
  │   ├─ all_scenarios_infected.png
  │   └─ all_scenarios_susceptible.png
  ├─ utils/
  │   ├─ config.py
  │   └─ __init__.py
  └─ requirements.txt
```

### **A.3 Execution**

To reproduce results:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/overview.ipynb
```

To run just the infection model:

```bash
python -m src.main
```
