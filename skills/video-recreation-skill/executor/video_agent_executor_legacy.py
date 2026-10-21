#!/usr/bin/env python3
import argparse
from pathlib import Path
from src.executor import validate_job, build_job, build_queue, aggregate_qa

def main():
    p=argparse.ArgumentParser(description="Video Agent Executor V1")
    s=p.add_subparsers(dest="cmd", required=True)
    for c in ("validate","build","queue","qa"):
        x=s.add_parser(c); x.add_argument("job")
    a=p.parse_args(); jp=Path(a.job)
    if a.cmd=="validate": validate_job(jp, verbose=True)
    elif a.cmd=="build": build_job(jp)
    elif a.cmd=="queue": build_queue(jp)
    elif a.cmd=="qa": aggregate_qa(jp)
if __name__=="__main__": main()
