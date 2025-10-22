import os, sys, json, re, click, pandas as pd
from dotenv import load_dotenv
load_dotenv()
try:
    from openai import OpenAI
    _OPENAI = OpenAI() if os.getenv("OPENAI_API_KEY") else None
except Exception:
    _OPENAI = None

@click.group()
def cli():
    "GPT-assisted CLI utilities for parsing logs, transforming CSVs, and summarizing text."
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def parse_logs(path):
    pat = re.compile(r'\b(WARN|ERROR)\b')
    out = []
    with open(path,'r',errors='ignore') as f:
        for i,line in enumerate(f,1):
            if pat.search(line):
                out.append({'line': i, 'text': line.strip()})
    click.echo(json.dumps(out, indent=2))

@cli.command()
@click.argument('csv_in', type=click.Path(exists=True))
@click.argument('csv_out', type=click.Path())
def csv_to_summary(csv_in, csv_out):
    df = pd.read_csv(csv_in)
    if 'category' not in df.columns:
        click.echo("CSV must have a 'category' column", err=True); sys.exit(1)
    out = df.groupby('category').size().reset_index(name='count')
    out.to_csv(csv_out, index=False)
    click.echo(f"wrote {csv_out}")

@cli.command()
@click.argument('text', required=False)
def summarize(text):
    if not text:
        text = sys.stdin.read()
    text = text.strip()
    if not text:
        click.echo("No text to summarize."); return
    if _OPENAI:
        try:
            model = os.getenv("MODEL","gpt-4o-mini")
            res = _OPENAI.chat.completions.create(model=model, messages=[
                {"role":"system","content":"Summarize the text concisely for an engineering audience."},
                {"role":"user","content":text}
            ])
            click.echo(res.choices[0].message.content.strip()); return
        except Exception as e:
            click.echo(f"[fallback] OpenAI failed: {e}", err=True)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    click.echo(' '.join(sentences[:3]))

if __name__ == "__main__":
    cli()
