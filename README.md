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

## Additional sources

Opportunity Scout also searches the official Stack Exchange API across
selected enthusiast communities. A combined scout is available with:

```bash
opportunity-scout-all
```

Marketplace competition checks use official eBay and Etsy APIs:

```bash
opportunity-scout-marketplace ebay "replacement knob"
opportunity-scout-marketplace etsy "replacement knob"
```

These marketplace checks examine public active listings, titles, URLs,
prices, and aggregate result counts. They do not access private orders,
sales records, customer data, messages, or shop-management functions.

## Credentials and privacy

API credentials are loaded from a local `.env` file that is excluded
from Git. Real credentials and generated data are never committed.
The `.env.example` file documents the required variable names without
containing any secrets.

Reddit access is intentionally disabled unless explicit API and
commercial-use permission is obtained from Reddit.
