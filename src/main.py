"""Entry point for running the InfectionModel simulation."""

from src.model import InfectionModel
from src.visualisation import run_simulation
from utils.config import PopulationConfig, SimulationConfig

if __name__ == "__main__":
    population = PopulationConfig(
        num_people=128,
        initial_infected=1,
        vaccinated_rate=0.2,
        vaccinated_effect=1.0,
        recovered_effect=1.0,
    )

    config = SimulationConfig(population=population)
    model = InfectionModel(config=config)
    run_simulation(model)
