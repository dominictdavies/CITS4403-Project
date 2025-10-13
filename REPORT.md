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

> ![all_scenarios_infected](/Users/leonce/Desktop/CITS4403-Project/outputs/all_scenarios_infected.png)
> ![all_scenarios_susceptible](/Users/leonce/Desktop/CITS4403-Project/outputs/all_scenarios_susceptible.png)

------

## **4. Results**

The experiments reveal consistent and interpretable trends across all scenarios. Each intervention affects either the *speed* or the *extent* of infection spread, and their combined effects demonstrate how behavioural factors interact to shape epidemic outcomes.

1. In the **baseline** scenario, infections grow rapidly after a short delay. The number of infected agents increases almost exponentially before stabilising as all susceptible individuals are infected. This logistic-shaped curve confirms the expected behaviour of uncontrolled transmission in a closed system.

2. Introducing **social distancing** slows the infection process. Reduced contact radius lowers the rate of encounters, flattening the infection curve and extending the time to reach saturation. Though the final infection count remains high, the slower progression effectively illustrates the “flatten the curve” phenomenon.

3. Enhancing **hygiene** reduces transmission probability while maintaining normal mobility. The resulting curve remains lower throughout, indicating fewer successful transmissions. Hygiene primarily diminishes infection *intensity* rather than infection *speed*.

4. The **50% vaccination** scenario exhibits a significant decline in both infection rate and total infections. Approximately half of the population remains uninfected, representing a simplified manifestation of herd immunity that limits outbreak growth.

5. When both interventions are combined, the epidemic is smallest and most stable. The **combined scenario** produces the flattest curve, with minimal growth and early plateau. This confirms that layered strategies outperform single interventions in controlling spread.

6. To validate correctness, a **real-time visualisation** built with *Pygame* was used. In this interface, agents appear as coloured dots—red for infected, yellow for susceptible, and blue for vaccinated. Observations show infection only occurs upon close contact and that boundary reflections behave properly.

> ![image-20251009004922833](/Users/leonce/Library/Application Support/typora-user-images/image-20251009004922833.png)

The visual behaviour aligns with data results: dense infection clusters emerge in the baseline, while spread remains contained under combined measures. This consistency between visual and statistical outcomes reinforces the accuracy of model logic.

------

### **4.7 Summary of Trends**

| Scenario       | Infection Peak | Speed of Spread | Final Susceptible | Key Observation       |
| -------------- | -------------- | --------------- | ----------------- | --------------------- |
| Baseline       | Very high      | Fast            | ~0                | Complete outbreak     |
| Distancing     | Medium-high    | Slower          | ~20               | Flattened curve       |
| Hygiene        | Medium         | Moderate        | ~30               | Reduced transmission  |
| 50% Vaccinated | Low            | Slower          | ~45               | Partial herd immunity |
| Combined       | Very low       | Slowest         | ~60               | Strongest suppression |

------

## **5. Discussion**

### **5.1 Model Evaluation**

The model demonstrates coherent internal logic and consistent sensitivity across its parameters. Variations in geometry or infection probability produce predictable and interpretable effects: lower contact radius or reduced probability flatten infection curves, while their combination yields the strongest suppression.

The design is compact yet modular. With fewer than 200 lines of code, the implementation provides a transparent mapping between parameters and emergent outcomes. The use of ContinuousSpace avoids lattice artefacts, and the RandomActivation scheduler ensures fairness in agent updates.

The reproducibility of results, achieved through fixed seeds and data exports, allows transparent verification and replication by others.

------

### **5.2 Sensitivity Analysis**

Three groups of parameters govern system dynamics:

1. **Geometric parameters** – including `collision_radius`, `distancing_factor`, and population density (`N / area`), determine encounter frequency.
2. **Probabilistic parameters** – `infection_prob`, `hygiene_factor`, and `vaccinated_effect`, control infection likelihood per contact.
3. **Initial conditions** – such as `initial_infected` and `vaccinated_rate`, influence early acceleration and final outbreak size.

Simulation results show consistent qualitative behaviour: lowering either contact frequency or infection probability suppresses infection curves, and combining both maximises the mitigation effect.

------

### **5.3 Validity and Limitations**

Despite its simplicity, the model has several limitations that constrain realism:

1. **Single-radius approximation:** using one radius for both collision and infection simplifies computation but ignores variation in proximity and exposure time.
2. **Absence of recovery:** infected agents remain permanently infected, inflating final counts relative to realistic epidemics.
3. **Homogeneous agents:** identical movement speeds and behaviours omit variability in compliance or susceptibility.
4. **Discrete-time simulation:** fixed time steps standardise exposure duration, limiting fine-grained temporal analysis.

These limitations are deliberate trade-offs to prioritise transparency and computational efficiency over biological detail.

------

### **5.4 Extensibility**

The modular architecture allows straightforward extensions:

1. Introduce recovery and immunity states (`RECOVERED`, `REMOVED`).
2. Assign heterogeneous speeds or compliance levels.
3. Separate `bounce_radius` from `contact_radius` for finer physical realism.
4. Add social clustering or barriers to represent environmental structure.
5. Record contact networks for statistical or epidemiological analysis.

Such additions could increase realism while preserving interpretability and educational value.

**Note on Code Maintenance:**
 A subsequent pull request introduced automated code formatting using *Black* and *isort* via *pre-commit*. This ensures consistent style and import order across all Python files without altering functionality.

------

## **6. Conclusion**

A continuous-space agent-based model was developed to simulate infection spread under different behavioural interventions. The results demonstrate that social distancing primarily slows the rate of transmission, hygiene reduces overall infections, vaccination limits both scale and duration, and their combination produces the strongest suppression effect.

The inclusion of visualisation and reproducible experiments highlights how simple, individual-level rules can produce complex, emergent epidemic dynamics. The project’s modular structure and clear outputs make it a strong foundation for future work on recovery processes, networked populations, and adaptive behaviours.

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
  │   ├─ all_scenarios_susceptible.png
  │   └─ scenario CSVs
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

------

## **Appendix B. Figure Captions**

**Figure 1:** Infected vs Time (five intervention scenarios)

**Figure 2:** Susceptible vs Time (comparison of all scenarios)

**Figure 3:** Pygame visualisation snapshot showing movement and infection spread
