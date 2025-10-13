"""Configuration classes for infection model."""

from dataclasses import dataclass, field


@dataclass
class WorldConfig:
    """Physical environment parameters.

    Attributes:
        width: Width of the simulation environment in pixels.
        height: Height of the simulation environment in pixels.
        speed: Maximum movement speed of people per frame.
        collision_radius: Distance at which people bounce off each other.
    """

    width: int = 1280
    height: int = 1280
    speed: float = 3.0
    collision_radius: float = 10.0

    def __post_init__(self):
        """Validate and clamp values."""
        self.width = max(1, self.width)
        self.height = max(1, self.height)
        self.speed = max(0.0, self.speed)
        self.collision_radius = max(0.0, self.collision_radius)


@dataclass
class DiseaseConfig:
    """Disease transmission and recovery parameters.

    Attributes:
        contact_radius: Distance at which disease transmission can occur.
        frame_infection_prob: Probability of transmission per frame when in contact (0-1).
        frame_recover_prob: Probability of recovery per frame for infected people (0-1).
    """

    contact_radius: float = 20.0
    frame_infection_prob: float = 0.5
    frame_recover_prob: float = 5e-3

    def __post_init__(self):
        """Validate and clamp values."""
        self.contact_radius = max(0.0, self.contact_radius)
        self.frame_infection_prob = max(0.0, min(1.0, self.frame_infection_prob))
        self.frame_recover_prob = max(0.0, min(1.0, self.frame_recover_prob))


@dataclass
class PopulationConfig:
    """Population composition and immunity parameters.

    Attributes:
        num_people: Total number of people in the simulation.
        initial_infected: Number of people infected at the start of simulation.
        vaccinated_rate: Proportion of population vaccinated at initialization (0-1).
        vaccinated_effect: Immunity effect for vaccinated people (0-1, where 1 is full immunity).
        recovered_effect: Immunity effect for recovered people (0-1, where 1 is full immunity).
    """

    num_people: int = 128
    initial_infected: int = 1
    vaccinated_rate: float = 0.2
    vaccinated_effect: float = 1.0
    recovered_effect: float = 1.0

    def __post_init__(self):
        """Validate and clamp values."""
        self.num_people = max(1, self.num_people)
        self.initial_infected = max(0, min(self.num_people, self.initial_infected))
        self.vaccinated_rate = max(0.0, min(1.0, self.vaccinated_rate))
        self.vaccinated_effect = max(0.0, min(1.0, self.vaccinated_effect))
        self.recovered_effect = max(0.0, min(1.0, self.recovered_effect))


@dataclass
class SimulationConfig:
    """Complete configuration for epidemic simulation.

    Attributes:
        world: Physical environment settings.
        disease: Disease transmission and recovery settings.
        population: Population composition and immunity settings.
        seed: Random seed for reproducibility.
    """

    world: WorldConfig = field(default_factory=WorldConfig)
    disease: DiseaseConfig = field(default_factory=DiseaseConfig)
    population: PopulationConfig = field(default_factory=PopulationConfig)
    seed: int = 42
