from src.model import InfectionModel
from src.visualisation import run_simulation


if __name__ == "__main__":
    model = InfectionModel(
        N=10,
        width=50,
        height=50,
        speed=1.0,
        collision_radius=1.0,  # bounce only (small)
        contact_radius=6.0,  # infection proximity (large)
        infection_prob=0.5,
        initial_infected=2,
        seed=42,
    )

    run_simulation(model)
