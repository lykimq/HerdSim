# HerdSim -- root facade over shared engine + area Makefiles.
# platform (Simulate + UI):  make -C platform help   (or make help)
# scaling (RQ protocols):    make -C scaling help    (or make scaling-help)

.PHONY: help install dev dev-backend dev-frontend test test-backend test-ci \
	test-stress test-frontend lint format typecheck check build clean scaling-help \
	scaling-test scaling-pilot scaling-pilot-state scaling-analyse scaling-scout \
	scaling-claim-plan scaling-claim-reseed scaling-t1-plan scaling-t1 \
	scaling-factor-sweep

UV ?= uv
export PYTHONPATH := $(CURDIR):$(CURDIR)/platform:$(CURDIR)/scaling$(if $(PYTHONPATH),:$(PYTHONPATH),)

help:
	@echo "HerdSim -- shared engine with area Makefiles"
	@echo ""
	@echo "  Shared engine:  core/ plugins/ methods/ services/shared/ analysis/"
	@echo "  Areas (each owns a Makefile):"
	@echo "    platform/  Simulate + UI     ->  make -C platform help"
	@echo "    scaling/   RQ protocols      ->  make -C scaling help"
	@echo ""
	@echo "Common aliases (forwarded):"
	@echo "  make install|dev|test|test-ci|lint|format|typecheck|check|build|clean"
	@echo "  make scaling-help|scaling-pilot|scaling-scout|scaling-claim-*|scaling-t1*"
	@echo "  Full scaling list: make -C scaling help"
	@echo "  Note: CI uses make test-ci (no stress, no scaling campaigns)."

install dev dev-backend dev-frontend test test-backend test-ci test-stress \
	test-frontend lint format typecheck check build clean:
	@$(MAKE) -C platform $@

scaling-help:
	@$(MAKE) -C scaling help

scaling-test scaling-pilot scaling-pilot-state scaling-analyse scaling-scout \
	scaling-claim-plan scaling-claim-reseed scaling-t1-plan scaling-t1 \
	scaling-factor-sweep:
	@$(MAKE) -C scaling $@
