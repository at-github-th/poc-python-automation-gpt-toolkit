# Python Automation Toolkit (GPT-assisted)

Small, practical CLI with three commands:

- `parse-logs <file>` — extract WARN/ERROR lines
- `csv-to-summary <in.csv> <out.csv>` — group by `category` and count
- `summarize <text>` — GPT summary if `OPENAI_API_KEY` is set; fallback otherwise

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env  # optionally add OPENAI_API_KEY

# Examples:
python cli.py parse_logs example.log
python cli.py csv_to_summary examples/in.csv out.csv
echo "This is a long paragraph to summarize." | python cli.py summarize
```
