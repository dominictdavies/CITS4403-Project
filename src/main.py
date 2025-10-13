"""Entry point for running the InfectionModel simulation."""

from src.model import InfectionModel
from src.visualisation import run_simulation

if __name__ == "__main__":
    model = InfectionModel()
    run_simulation(model, fps=60)
