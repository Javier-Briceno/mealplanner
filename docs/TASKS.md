# MVP Backlog

## T1 – CLI Skeleton (2h)
- Args: --days, --meals-per-day, --format, --out
- Help/usage with examples
**Accept:** `python mealplanner.py --days 3 --meals-per-day 2 --format csv --out outputs/plan.csv` creates file

## T2 – Core Logic (2h)
- Validate ranges, defaults, simple rules
**Accept:** invalid args -> exit!=0 + helpful message

## T3 – Output Writers (2h)
- CSV/MD writers; folder auto-create
**Accept:** schema stable; MD table readable

## T4 – Error Cases + Tests (2h)
- Empty ingredients, unknown diet, bad path
**Accept:** 6 pytest cases pass

## T5 – README + Demo (1h)
- Install steps, examples, GIF
**Accept:** teammate can run in <5 min
