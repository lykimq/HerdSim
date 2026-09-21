# Goal 2: scaling protocols (RQ grids under scaling/results/).
# From repo root: make -C scaling help   or   make scaling-help

.PHONY: help scaling-help scaling-test scaling-pilot scaling-pilot-state \
	scaling-analyse scaling-scout scaling-factor-sweep

ROOT := $(abspath $(CURDIR)/..)
UV ?= uv
export PYTHONPATH := $(ROOT):$(ROOT)/platform:$(ROOT)/scaling$(if $(PYTHONPATH),:$(PYTHONPATH),)

SCALING_PROTOCOL_DIR ?= configs/protocols
PHASE1_PILOT_PROTOCOL ?= $(SCALING_PROTOCOL_DIR)/phase1_pilot.yaml
PHASE1_SCOUT_PROTOCOL ?= $(SCALING_PROTOCOL_DIR)/phase1_scout.yaml
PHASE2_STATE_PROTOCOL ?= $(SCALING_PROTOCOL_DIR)/phase2_pilot_state.yaml
PHASE5_SWEEP_PROTOCOL ?= $(SCALING_PROTOCOL_DIR)/phase5_factor_sweep.yaml

SCALING_OUT ?= results/phase1/pilot
STATE_OUT ?= results/phase2/pilot_state
SCOUT_OUT ?= results/phase1/scout
SWEEP_OUT ?= results/phase5/factor_sweep

WORKERS ?= 1
SCALING_MAX_TICKS ?=
PACKAGE ?= A
TRIALS ?= $(SCALING_OUT)/trials.csv
OUT ?= $(SCALING_OUT)/packages/$(shell echo $(PACKAGE) | tr A-Z a-z)

SCALING_METHOD ?=
SCALING_LAYOUT ?=
SCALING_N ?=
SCALING_D ?=
SCALING_SEEDS ?=

SCALING_MAX_TICKS_FLAG = $(if $(SCALING_MAX_TICKS),--max-ticks $(SCALING_MAX_TICKS),)
SCALING_OVERRIDE_FLAGS = \
	$(if $(SCALING_METHOD),--methods $(SCALING_METHOD),) \
	$(if $(SCALING_LAYOUT),--layouts $(SCALING_LAYOUT),) \
	$(if $(SCALING_N),--n $(SCALING_N),) \
	$(if $(SCALING_D),--d $(SCALING_D),) \
	$(if $(SCALING_SEEDS),--seeds $(SCALING_SEEDS),)

.DEFAULT_GOAL := help

help scaling-help:
	@echo "HerdSim scaling -- RQ protocols"
	@echo ""
	@echo "What this is:"
	@echo "  Batch simulations that ask: for flock size N sheep and D dogs,"
	@echo "  how often does herding succeed? Writes under scaling/results/."
	@echo "  Interrupted runs resume if you keep manifest.jsonl and"
	@echo "  re-run the same target."
	@echo ""
	@echo "Targets (grids match scaling/configs/protocols/*.yaml):"
	@echo "  help                 Show this help"
	@echo "  scaling-test          Pytest for the scaling runner and analysis code"
	@echo ""
	@echo "  scaling-pilot         Small smoke grid (~150 trials)."
	@echo "                       Output: scaling/results/phase1/pilot/"
	@echo "  scaling-scout         Denser Phase-1 map (~1440 trials)."
	@echo "                       Output: scaling/results/phase1/scout/"
	@echo "  scaling-pilot-state   Four X0 layouts (~600 trials)."
	@echo "                       Output: scaling/results/phase2/pilot_state/"
	@echo "  scaling-factor-sweep  Observation-mode sweep (~360 trials)."
	@echo "                       Output: scaling/results/phase5/factor_sweep/"
	@echo "  scaling-analyse       Re-run analysis on an existing trials.csv"
	@echo ""
	@echo "Variables: WORKERS, SCALING_MAX_TICKS, PACKAGE, TRIALS, OUT"
	@echo "Example:   make scaling-pilot WORKERS=4"
	@echo "Docs:      scaling/results/README.md"
	@echo "Platform:  make -C ../platform help"

scaling-test:
	cd $(ROOT) && $(UV) run pytest tests/backend/correctness/test_scaling_stack.py -q

scaling-pilot:
	@mkdir -p $(SCALING_OUT)
	cd $(ROOT) && $(UV) run scaling/scripts/run_grid.py \
		--protocol $(CURDIR)/$(PHASE1_PILOT_PROTOCOL) \
		--output $(CURDIR)/$(SCALING_OUT) \
		--workers $(WORKERS) \
		$(SCALING_MAX_TICKS_FLAG) \
		$(SCALING_OVERRIDE_FLAGS)
	$(MAKE) scaling-analyse \
		PACKAGE=A TRIALS=$(SCALING_OUT)/trials.csv OUT=$(SCALING_OUT)/packages/a

scaling-pilot-state:
	@mkdir -p $(STATE_OUT)
	cd $(ROOT) && $(UV) run scaling/scripts/run_grid.py \
		--protocol $(CURDIR)/$(PHASE2_STATE_PROTOCOL) \
		--output $(CURDIR)/$(STATE_OUT) \
		--workers $(WORKERS) \
		$(SCALING_MAX_TICKS_FLAG) \
		$(SCALING_OVERRIDE_FLAGS)
	$(MAKE) scaling-analyse \
		PACKAGE=B TRIALS=$(STATE_OUT)/trials.csv OUT=$(STATE_OUT)/packages/b

scaling-analyse:
	cd $(ROOT) && $(UV) run scaling/scripts/analyse.py \
		--package $(PACKAGE) \
		--trials $(CURDIR)/$(TRIALS) \
		--output $(CURDIR)/$(OUT)

scaling-scout:
	@echo "NOTE: scaling-scout is long-running (many N x D x seeds cells)."
	@echo "Output: $(SCOUT_OUT)  protocol=$(PHASE1_SCOUT_PROTOCOL)"
	@mkdir -p $(SCOUT_OUT)
	cd $(ROOT) && $(UV) run scaling/scripts/run_grid.py \
		--protocol $(CURDIR)/$(PHASE1_SCOUT_PROTOCOL) \
		--output $(CURDIR)/$(SCOUT_OUT) \
		--workers $(WORKERS) \
		$(SCALING_MAX_TICKS_FLAG) \
		$(SCALING_OVERRIDE_FLAGS)
	$(MAKE) scaling-analyse \
		PACKAGE=A TRIALS=$(SCOUT_OUT)/trials.csv OUT=$(SCOUT_OUT)/packages/a
	$(MAKE) scaling-analyse \
		PACKAGE=F TRIALS=$(SCOUT_OUT)/trials.csv OUT=$(SCOUT_OUT)/packages/f

scaling-factor-sweep:
	@mkdir -p $(SWEEP_OUT)
	cd $(ROOT) && $(UV) run scaling/scripts/run_factor_sweep.py \
		--protocol $(CURDIR)/$(PHASE5_SWEEP_PROTOCOL) \
		--output $(CURDIR)/$(SWEEP_OUT) \
		--workers $(WORKERS)
	$(MAKE) scaling-analyse \
		PACKAGE=E TRIALS=$(SWEEP_OUT)/trials.csv OUT=$(SWEEP_OUT)/packages/e
