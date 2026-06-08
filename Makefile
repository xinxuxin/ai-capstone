.PHONY: setup lint format test sample-panel sample-analysis dashboard clean

setup:
	uv sync

lint:
	uv run ruff check src tests scripts

format:
	uv run ruff format src tests scripts

test:
	uv run pytest tests

sample-panel:
	uv run python scripts/bootstrap_from_samples.py

sample-analysis:
	uv run python scripts/run_baseline_analysis.py --panel data/processed/analytic_panel.csv

dashboard:
	uv run streamlit run src/ai_impact_research/dashboard/app.py

clean:
	rm -rf data/processed/*.csv .pytest_cache .ruff_cache .mypy_cache
