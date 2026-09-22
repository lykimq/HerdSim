# HerdSim -- root facade.
# Goal 1 (Simulate + UI):  make -C platform help   (or make help)
# Goal 2 (scaling / RQs):  make -C scaling help    (or make scaling-help)

.PHONY: help install dev dev-backend dev-frontend test test-backend test-stress \
	test-frontend lint format typecheck build clean scaling-help \
	scaling-test scaling-pilot scaling-pilot-state scaling-analyse scaling-scout \
	scaling-factor-sweep

UV ?= uv
export PYTHONPATH := $(CURDIR):$(CURDIR)/platform:$(CURDIR)/scaling$(if $(PYTHONPATH),:$(PYTHONPATH),)

help:
	@echo "HerdSim -- two goals, one shared engine"
	@echo ""
	@echo "  Shared engine:  core/ plugins/ methods/ services/shared/ analysis/"
	@echo "  Goal 1 (UI):    platform/   ->  make -C platform help"
	@echo "  Goal 2 (RQs):   scaling/    ->  make -C scaling help"
	@echo ""
	@echo "Common aliases (forwarded):"
	@echo "  make install|dev|test|lint|format|typecheck|build|clean"
	@echo "  make scaling-help|scaling-pilot|scaling-scout|..."

install dev dev-backend dev-frontend test test-backend test-stress \
	test-frontend lint format typecheck build clean:
	@$(MAKE) -C platform $@

scaling-help:
	@$(MAKE) -C scaling help

scaling-test scaling-pilot scaling-pilot-state scaling-analyse scaling-scout scaling-factor-sweep:
	@$(MAKE) -C scaling $@
