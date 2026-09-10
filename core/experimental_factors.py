"""Typed experimental factors for HerdSim factor-based experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any


FAILURE_MODES = (
    "none",
    "inactive_after_tick",
    "reduced_speed_after_tick",
    "blind_after_tick",
)

OBSERVATION_MODES = (
    "global",
    "local_positions",
    "bearing_only",
    "noisy_bearing",
    "intermittent",
)

COMMUNICATION_MODES = ("none", "neighbour_broadcast", "global_shared")

GOAL_MODES = ("static", "moving")

INITIAL_LAYOUTS = ("cluster", "split", "wide")


@dataclass
class FlockFactors:
    n_sheep: int | None = None
    initial_layout: str = "cluster"
    initial_spread: float | None = None
    cohesion_scale: float = 1.0
    stubborn_fraction: float = 0.0
    stubborn_response_scale: float = 0.25
    noise_strength: float | None = None


@dataclass
class ShepherdFactors:
    n_shepherds: int | None = None
    speed_scale: float = 1.0
    failure_mode: str = "none"
    failure_tick: int = -1
    sensing_scale: float = 1.0
    v_max: float | None = None
    a_max: float | None = None
    omega_max: float | None = None
    latency: int = 0


@dataclass
class ObservationFactors:
    mode: str = "global"
    sensing_range: float | None = None
    noise_sigma: float = 0.0
    observation_frequency: int = 1
    communication: str = "none"


@dataclass
class EnvironmentFactors:
    goal_mode: str = "static"
    goal_velocity: tuple[float, float] = (0.0, 0.0)
    world_overrides: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelFactors:
    sheep_model: str = "strombom"
    dog_controller: str = "collect_drive"
    scenario: str = "drive_to_goal"
    preset: str = "paper"


@dataclass
class ExperimentalFactors:
    """Sole high-level experiment specification for HerdSim."""

    flock: FlockFactors = field(default_factory=FlockFactors)
    shepherds: ShepherdFactors = field(default_factory=ShepherdFactors)
    observation: ObservationFactors = field(default_factory=ObservationFactors)
    environment: EnvironmentFactors = field(default_factory=EnvironmentFactors)
    model: ModelFactors = field(default_factory=ModelFactors)
    params: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.flock.initial_layout not in INITIAL_LAYOUTS:
            raise ValueError(
                f"Unknown initial_layout '{self.flock.initial_layout}'. "
                f"Use one of {INITIAL_LAYOUTS}."
            )
        if not (0.0 <= float(self.flock.stubborn_fraction) <= 1.0):
            raise ValueError("stubborn_fraction must be in [0, 1].")
        if not (0.0 < float(self.flock.stubborn_response_scale) <= 1.0):
            raise ValueError("stubborn_response_scale must be in (0, 1].")
        if float(self.flock.cohesion_scale) < 0.0:
            raise ValueError("cohesion_scale must be >= 0.")
        if self.shepherds.failure_mode not in FAILURE_MODES:
            raise ValueError(
                f"Unknown failure_mode '{self.shepherds.failure_mode}'. "
                f"Use one of {FAILURE_MODES}."
            )
        if self.observation.mode not in OBSERVATION_MODES:
            raise ValueError(
                f"Unknown observation mode '{self.observation.mode}'. "
                f"Use one of {OBSERVATION_MODES}."
            )
        if self.observation.communication not in COMMUNICATION_MODES:
            raise ValueError(
                f"Unknown communication '{self.observation.communication}'. "
                f"Use one of {COMMUNICATION_MODES}."
            )
        if int(self.observation.observation_frequency) < 1:
            raise ValueError("observation_frequency must be >= 1.")
        if self.environment.goal_mode not in GOAL_MODES:
            raise ValueError(
                f"Unknown goal_mode '{self.environment.goal_mode}'. "
                f"Use one of {GOAL_MODES}."
            )
        if self.flock.n_sheep is not None and int(self.flock.n_sheep) < 1:
            raise ValueError("n_sheep must be >= 1.")
        if self.shepherds.n_shepherds is not None and int(self.shepherds.n_shepherds) < 0:
            raise ValueError("n_shepherds must be >= 0.")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any] | None) -> ExperimentalFactors:
        raw = dict(raw or {})
        flock = _merge_dataclass(FlockFactors, raw.get("flock"), raw)
        shepherds = _merge_dataclass(ShepherdFactors, raw.get("shepherds"), raw)
        observation = _merge_dataclass(ObservationFactors, raw.get("observation"), raw)
        environment = _merge_dataclass(
            EnvironmentFactors, raw.get("environment"), raw
        )
        model = _merge_dataclass(ModelFactors, raw.get("model"), raw)
        # Flat aliases used by API / CLI.
        if "n_sheep" in raw and flock.n_sheep is None:
            flock.n_sheep = int(raw["n_sheep"])
        if "n_shepherds" in raw and shepherds.n_shepherds is None:
            shepherds.n_shepherds = int(raw["n_shepherds"])
        if "sheep_model" in raw:
            model.sheep_model = str(raw["sheep_model"])
        if "dog_controller" in raw:
            model.dog_controller = str(raw["dog_controller"])
        if "scenario" in raw or "scenario_id" in raw:
            model.scenario = str(raw.get("scenario") or raw.get("scenario_id"))
        if "preset" in raw:
            model.preset = str(raw["preset"])
        if "obs_mode" in raw:
            observation.mode = str(raw["obs_mode"])
        if "sensing_range" in raw:
            observation.sensing_range = float(raw["sensing_range"])
        if "noise_sigma" in raw:
            observation.noise_sigma = float(raw["noise_sigma"])
        if "stubborn_fraction" in raw:
            flock.stubborn_fraction = float(raw["stubborn_fraction"])
        if "cohesion_scale" in raw:
            flock.cohesion_scale = float(raw["cohesion_scale"])
        if "failure_mode" in raw:
            shepherds.failure_mode = str(raw["failure_mode"])
        if "failure_tick" in raw:
            shepherds.failure_tick = int(raw["failure_tick"])
        if "communication" in raw:
            observation.communication = str(raw["communication"])
        if "goal_mode" in raw:
            environment.goal_mode = str(raw["goal_mode"])
        params = dict(raw.get("params") or {})
        for key in ("algorithm_params", "params"):
            if isinstance(raw.get(key), dict):
                params.update(raw[key])
        factors = cls(
            flock=flock,
            shepherds=shepherds,
            observation=observation,
            environment=environment,
            model=model,
            params=params,
        )
        factors.validate()
        return factors


def _merge_dataclass(cls: type, nested: Any, flat: dict[str, Any]):
    data = {f.name: getattr(cls(), f.name) for f in fields(cls)}
    if isinstance(nested, dict):
        for key, value in nested.items():
            if key in data:
                data[key] = value
    # Allow flat keys that match dataclass field names.
    for f in fields(cls):
        if f.name in flat and f.name not in ("world_overrides", "params"):
            data[f.name] = flat[f.name]
    if cls is EnvironmentFactors and isinstance(flat.get("world_overrides"), dict):
        data["world_overrides"] = dict(flat["world_overrides"])
    if cls is EnvironmentFactors and "goal_velocity" in flat:
        gv = flat["goal_velocity"]
        data["goal_velocity"] = tuple(gv) if not isinstance(gv, tuple) else gv
    return cls(**data)


# Allowlisted factor keys for factorial grids (flat dotted or short names).
FACTOR_GRID_KEYS = frozenset(
    {
        "n_sheep",
        "n_shepherds",
        "sheep_model",
        "dog_controller",
        "scenario",
        "preset",
        "obs_mode",
        "sensing_range",
        "noise_sigma",
        "observation_frequency",
        "communication",
        "stubborn_fraction",
        "stubborn_response_scale",
        "cohesion_scale",
        "failure_mode",
        "failure_tick",
        "speed_scale",
        "goal_mode",
        "initial_layout",
        "initial_spread",
        "noise_strength",
        "v_max",
        "a_max",
        "omega_max",
        "latency",
    }
)

MAX_FACTOR_GRID_CELLS = 500
