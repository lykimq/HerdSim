"""Lama and di Bernardo 2024: the target step, the herder rule, and the paper's assumptions."""

from __future__ import annotations

import numpy as np
import pytest

from sim.methods.lama.dynamics import (
    choose_targets,
    herder_velocities,
    noise_step,
    target_velocities,
)
from sim.plugins.dogs import lama_herders
from sim.plugins.sheep import lama as lama_sheep
from tests.helpers import gather_config, make_state, make_world

CONFIG = gather_config(n=20, d=2)
BETA, LAMBDA = CONFIG["repulsion_strength"], CONFIG["repulsion_radius"]
XI, V_H = CONFIG["sensing_radius"], CONFIG["herder_speed"]


def _reference_push(targets, herders, cfg):
    """Eq. 1 one target at a time: beta (lambda - d) away from every herder within lambda."""
    out = np.zeros_like(targets)
    for a, t in enumerate(targets):
        for h in herders:
            d = np.linalg.norm(t - h)
            if d <= cfg["repulsion_radius"]:
                out[a] += cfg["repulsion_strength"] * (cfg["repulsion_radius"] - d) * (t - h) / d
    return out


def test_vectorised_push_matches_the_per_target_reference():
    rng = np.random.default_rng(3)
    targets = rng.uniform(-6.0, 6.0, size=(50, 2))
    herders = rng.uniform(-6.0, 6.0, size=(5, 2))
    np.testing.assert_allclose(
        target_velocities(targets, herders, CONFIG), _reference_push(targets, herders, CONFIG)
    )


def test_push_points_away_from_the_herder_falls_linearly_and_adds():
    target = np.array([[0.0, 0.0]])
    one = target_velocities(target, np.array([[-1.0, 0.0]]), CONFIG)[0]
    np.testing.assert_allclose(one, [BETA * (LAMBDA - 1.0), 0.0])  # away from a herder at -x
    at_contact = target_velocities(target, np.array([[-1e-9, 0.0]]), CONFIG)[0]
    assert np.linalg.norm(at_contact) == pytest.approx(BETA * LAMBDA, rel=1e-6)  # v_T
    beyond = target_velocities(target, np.array([[-LAMBDA - 0.01, 0.0]]), CONFIG)[0]
    np.testing.assert_allclose(beyond, [0.0, 0.0])
    two = target_velocities(target, np.array([[-1.0, 0.0], [0.0, -1.0]]), CONFIG)[0]
    np.testing.assert_allclose(two, [BETA * (LAMBDA - 1.0), BETA * (LAMBDA - 1.0)])  # sum


def test_noise_has_variance_two_d_dt_per_coordinate():
    steps = noise_step(np.random.default_rng(0), 200_000, CONFIG)
    expected = 2.0 * CONFIG["target_diffusion"] * CONFIG["dt"]
    assert steps.var(axis=0) == pytest.approx([expected, expected], rel=0.02)
    assert steps.mean(axis=0) == pytest.approx([0.0, 0.0], abs=3e-3)


def test_herder_chases_the_farthest_sensed_target_and_ignores_the_unseen():
    targets = np.array([[3.0, 0.0], [6.0, 0.0], [XI + 5.0, 0.0]])  # the last is out of sight
    choice = choose_targets(targets, np.array([[0.0, 0.0]]), CONFIG)
    assert choice.target.tolist() == [1]


def test_a_target_closer_to_a_sensed_neighbour_is_left_to_that_neighbour():
    targets = np.array([[8.0, 0.0]])  # 2 from herder 1, 8 from herder 0, both sense it
    herders = np.array([[0.0, 0.0], [10.0, 0.0]])
    assert choose_targets(targets, herders, CONFIG).target.tolist() == [-1, 0]
    far_apart = np.array([[0.0, 0.0], [0.0, XI + 1.0]])  # herders do not sense each other
    both = choose_targets(np.array([[0.0, 5.0]]), far_apart, CONFIG).target
    assert both.tolist() == [0, 0]


def test_a_chasing_herder_aims_beyond_its_target_at_most_at_v_h():
    target = np.array([[6.0, 0.0]])
    herder = np.array([[0.0, 0.0]])
    v, choice = herder_velocities(target, herder, goal_radius=4.0, config=CONFIG)
    assert choice.target.tolist() == [0]
    assert np.linalg.norm(v[0]) == pytest.approx(V_H)  # alpha x 7.25 is above v_H: saturated
    assert v[0, 0] > 0.0 and v[0, 1] == pytest.approx(0.0)
    near = np.array([[6.0 + CONFIG["chase_offset"] - 0.1, 0.0]])  # 0.1 short of the chase point
    v_near, _ = herder_velocities(target, near, goal_radius=4.0, config=CONFIG)
    np.testing.assert_allclose(v_near[0], [CONFIG["herder_gain"] * 0.1, 0.0])


def test_an_idle_herder_returns_to_the_origin_and_stops_inside_the_goal():
    no_targets = np.zeros((0, 2))
    outside = np.array([[0.0, 9.0]])
    v, _ = herder_velocities(no_targets, outside, goal_radius=4.0, config=CONFIG)
    np.testing.assert_allclose(v[0], [0.0, -V_H])
    inside = np.array([[0.0, 3.0]])
    v_in, _ = herder_velocities(no_targets, inside, goal_radius=4.0, config=CONFIG)
    np.testing.assert_allclose(v_in[0], [0.0, 0.0])


def test_positions_are_measured_from_the_goal_centre():
    """The paper's origin is the goal centre: a target at the goal centre is the nearest, and a
    herder with nothing to chase walks toward the goal, wherever the goal lies in the field."""
    world = make_world(width=200.0, height=200.0, goal_center=(150.0, 150.0), goal_radius=5.0)
    state = make_state([[150.0, 150.0], [150.0, 158.0]], [[150.0, 150.0 + 3.0]], world=world)
    moved = lama_herders.step(state, CONFIG)
    assert moved.metadata["herder_target"].tolist() == [1]  # the farther from the goal centre
    idle = make_state(np.zeros((0, 2)), [[150.0, 170.0]], world=world)
    back = lama_herders.step(idle, CONFIG)
    assert back.shepherd_positions[0, 1] < 170.0 and back.shepherd_positions[0, 0] == 150.0


def test_targets_step_is_push_plus_noise_and_stores_the_displacement_rate():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=4.0)
    state = make_state([[1.0, 0.0]], [[0.0, 0.0]], world=world)
    quiet = {**CONFIG, "target_diffusion": 0.0}
    moved = lama_sheep.step(state, quiet)
    push = BETA * (LAMBDA - 1.0)
    np.testing.assert_allclose(moved.sheep_positions[0], [1.0 + quiet["dt"] * push, 0.0])
    np.testing.assert_allclose(moved.sheep_velocities[0], [push, 0.0])


def test_slower_herders_than_targets_are_refused():
    with pytest.raises(ValueError, match="herder_speed must exceed"):
        gather_config(params={"herder_speed": BETA * LAMBDA})
    gather_config(params={"herder_speed": BETA * LAMBDA + 0.01})


def test_herders_decide_on_the_targets_at_the_start_of_the_tick():
    """The paper integrates both sides from the state at t: after the target step the herders
    choose and aim with the targets' positions from before it, not the moved ones."""
    world = make_world(goal_center=(0.0, 0.0), goal_radius=4.0)
    start = np.array([[6.0, 0.0], [0.0, 7.0]])  # the second is farther: chosen at the start
    state = make_state(start, [[3.0, 3.0]], world=world)
    moved = lama_sheep.step(state, CONFIG)
    moved = moved.copy_with(sheep_positions=np.array([[9.0, 0.0], [0.0, 7.0]]))  # now the first
    after = lama_herders.step(moved, CONFIG)
    assert after.metadata["herder_target"].tolist() == [1]
    aim = start[1] + CONFIG["chase_offset"] * start[1] / np.linalg.norm(start[1])
    expected = (aim - [3.0, 3.0]) / np.linalg.norm(aim - [3.0, 3.0]) * V_H
    np.testing.assert_allclose(after.shepherd_velocities[0], expected)
