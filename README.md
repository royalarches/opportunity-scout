# Opportunity Scout

Opportunity Scout finds repair discussions that may indicate demand for
small, hard-to-find replacement parts suitable for local 3D printing.

## Current capabilities

- Searches the official iFixit API
- Runs several spare-part searches as a batch
- Removes duplicate results
- Estimates demand, printability, competition, and legal risk
- Ranks opportunities
- Saves results as JSON
- Tests the scraper and ranking logic

## Start a session

```bash
cd ~/Projects/opportunity-scout
source .venv/bin/activate

```
## Search one phrase

    PYTHONPATH=src python -m opportunity_scout.run_ifixit "broken knob"

Results are saved to:

    data/ifixit_opportunities.json

## Run the batch scout

    PYTHONPATH=src python -m opportunity_scout.batch

Results are saved to:

    data/batch_opportunities.json

## Run the tests

    PYTHONPATH=src python -m pytest

## Collection policy

Prefer official APIs. For ordinary public pages, verify robots.txt,
identify the collector, use timeouts, and keep request rates low.
Do not bypass authentication, access controls, or site restrictions.

## Important limitation

The current scores are preliminary filters, not proof of market demand.
Promising results still require marketplace research, legal review,
measurements, prototyping, and customer validation.
