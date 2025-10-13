"""Entry point for running the InfectionModel simulation."""

from src.model import InfectionModel
from src.visualisation import run_simulation
from utils.config import SimulationConfig

if __name__ == "__main__":
    config = SimulationConfig()
    model = InfectionModel(config=config)
    run_simulation(model, fps=60)
