# Area: scaling protocols. Orchestration lives in
# scaling/scripts/campaign.py (services.scaling.campaign).
# From repo root: make -C scaling help

.PHONY: help scaling-help scaling-test scaling-analyse \
	scaling-pilot scaling-scout scaling-claim-plan scaling-claim-reseed \
	scaling-t1-plan scaling-t1 \
	scaling-pilot-state scaling-phase2-scout \
	scaling-phase2-claim-plan scaling-phase2-claim-reseed \
	scaling-transfer-size-scout scaling-transfer-size-claim-plan \
	scaling-transfer-size-claim-reseed \
	scaling-transfer-structure-scout scaling-transfer-structure-claim-plan \
	scaling-transfer-structure-claim-reseed \
	scaling-factor-sweep \
	scaling-phase5-obs-claim-plan scaling-phase5-obs-claim-reseed \
	scaling-phase5-range-scout scaling-phase5-range-claim-plan \
	scaling-phase5-range-claim-reseed \
	scaling-phase5-comm-scout scaling-phase5-comm-claim-plan \
	scaling-phase5-comm-claim-reseed

ROOT := $(abspath $(CURDIR)/..)
UV ?= uv
export PYTHONPATH := $(ROOT):$(ROOT)/platform:$(ROOT)/scaling$(if $(PYTHONPATH),:$(PYTHONPATH),)

# Default pool size for this host (Ultra 7 165H, 22 threads). Override down on
# smaller machines: make scaling-scout WORKERS=4
WORKERS ?= 16
PACKAGE ?= A
TRANSFER_METHOD ?= kubo
PROTOCOL ?=
TRIALS ?=
OUT ?=
SCALING_MAX_TICKS ?=
SCALING_METHOD ?=
SCALING_LAYOUT ?=
SCALING_N ?=
SCALING_D ?=
SCALING_SEEDS ?=

CAMPAIGN = cd $(ROOT) && $(UV) run scaling/scripts/campaign.py

CAMPAIGN_FLAGS = --workers $(WORKERS) \
	$(if $(SCALING_MAX_TICKS),--max-ticks $(SCALING_MAX_TICKS),) \
	$(if $(SCALING_METHOD),--methods $(SCALING_METHOD),) \
	$(if $(SCALING_LAYOUT),--layouts $(SCALING_LAYOUT),) \
	$(if $(SCALING_N),--n $(SCALING_N),) \
	$(if $(SCALING_D),--d $(SCALING_D),) \
	$(if $(SCALING_SEEDS),--seeds $(SCALING_SEEDS),)

.DEFAULT_GOAL := help

help scaling-help:
	@$(CAMPAIGN) help
	@echo "Make aliases (same verbs; PROTOCOL id under configs/protocols/):"
	@echo "  scaling-test"
	@echo "  scaling-pilot | scaling-scout | scaling-claim-plan | scaling-claim-reseed"
	@echo "  scaling-t1-plan | scaling-t1"
	@echo "  scaling-pilot-state | scaling-phase2-scout | scaling-phase2-claim-*"
	@echo "  scaling-transfer-*-scout|claim-*   TRANSFER_METHOD=kubo|fat"
	@echo "  scaling-factor-sweep | scaling-phase5-*-scout|claim-*"
	@echo "  scaling-analyse PROTOCOL=... PACKAGE=A [TRIALS=...]"
	@echo "Default WORKERS=$(WORKERS) on this Makefile (override as needed)."
	@echo "Example: make scaling-scout"
	@echo "         make scaling-transfer-size-scout TRANSFER_METHOD=fat WORKERS=16"

scaling-test:
	cd $(ROOT) && $(UV) run pytest tests/backend/correctness/test_scaling_stack.py -q

scaling-analyse:
	$(CAMPAIGN) analyse --protocol $(PROTOCOL) --package $(PACKAGE) \
		$(if $(TRIALS),--trials $(TRIALS),) \
		$(if $(OUT),--output $(OUT),)

scaling-pilot:
	$(CAMPAIGN) run --protocol phase1_pilot $(CAMPAIGN_FLAGS)

scaling-scout:
	$(CAMPAIGN) run --protocol phase1_scout $(CAMPAIGN_FLAGS)

scaling-claim-plan:
	$(CAMPAIGN) claim-plan --protocol phase1_claim

scaling-claim-reseed:
	$(CAMPAIGN) claim-reseed --protocol phase1_claim $(CAMPAIGN_FLAGS)

scaling-t1-plan:
	$(CAMPAIGN) t1-plan --protocol phase1_t1

scaling-t1:
	$(CAMPAIGN) t1 --protocol phase1_t1 $(CAMPAIGN_FLAGS)

scaling-pilot-state:
	$(CAMPAIGN) run --protocol phase2_pilot_state $(CAMPAIGN_FLAGS)

scaling-phase2-scout:
	$(CAMPAIGN) run --protocol phase2_scout $(CAMPAIGN_FLAGS)

scaling-phase2-claim-plan:
	$(CAMPAIGN) claim-plan --protocol phase2_claim

scaling-phase2-claim-reseed:
	$(CAMPAIGN) claim-reseed --protocol phase2_claim $(CAMPAIGN_FLAGS)

scaling-transfer-size-scout:
	$(CAMPAIGN) run --protocol phase4_$(TRANSFER_METHOD)_size_scout $(CAMPAIGN_FLAGS)

scaling-transfer-size-claim-plan:
	$(CAMPAIGN) claim-plan --protocol phase4_$(TRANSFER_METHOD)_size_claim

scaling-transfer-size-claim-reseed:
	$(CAMPAIGN) claim-reseed --protocol phase4_$(TRANSFER_METHOD)_size_claim $(CAMPAIGN_FLAGS)

scaling-transfer-structure-scout:
	$(CAMPAIGN) run --protocol phase4_$(TRANSFER_METHOD)_structure_scout $(CAMPAIGN_FLAGS)

scaling-transfer-structure-claim-plan:
	$(CAMPAIGN) claim-plan --protocol phase4_$(TRANSFER_METHOD)_structure_claim

scaling-transfer-structure-claim-reseed:
	$(CAMPAIGN) claim-reseed --protocol phase4_$(TRANSFER_METHOD)_structure_claim $(CAMPAIGN_FLAGS)

scaling-factor-sweep:
	$(CAMPAIGN) run --protocol phase5_factor_sweep $(CAMPAIGN_FLAGS)

scaling-phase5-obs-claim-plan:
	$(CAMPAIGN) claim-plan --protocol phase5_obs_claim

scaling-phase5-obs-claim-reseed:
	$(CAMPAIGN) claim-reseed --protocol phase5_obs_claim $(CAMPAIGN_FLAGS)

scaling-phase5-range-scout:
	$(CAMPAIGN) run --protocol phase5_range_scout $(CAMPAIGN_FLAGS)

scaling-phase5-range-claim-plan:
	$(CAMPAIGN) claim-plan --protocol phase5_range_claim

scaling-phase5-range-claim-reseed:
	$(CAMPAIGN) claim-reseed --protocol phase5_range_claim $(CAMPAIGN_FLAGS)

scaling-phase5-comm-scout:
	$(CAMPAIGN) run --protocol phase5_comm_scout $(CAMPAIGN_FLAGS)

scaling-phase5-comm-claim-plan:
	$(CAMPAIGN) claim-plan --protocol phase5_comm_claim

scaling-phase5-comm-claim-reseed:
	$(CAMPAIGN) claim-reseed --protocol phase5_comm_claim $(CAMPAIGN_FLAGS)
