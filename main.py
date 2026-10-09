#!/usr/bin/env python3
"""
Simple log parsing helper:
Counts log levels and reports total lines.
"""

import argparse
import re
from datetime import datetime
import sys

LOG_RE = re.compile(r"^\[(?P<ts>[^]]+)\] \[(?P<lvl>[^]]+)\] (?P<msg>.*)$")

def parse_line(line):
    m = LOG_RE.match(line)
    if m:
        ts_str = m.group('ts')
        try:
            ts = datetime.fromisoformat(ts_str)
        except ValueError:
            ts = None
        return ts, m.group('lvl'), m.group('msg')
    return None, None, None

def summary(path):
    counts={}
    earliest=None
    latest=None
    total=0
    with open(path,encoding='utf-8') as f:
        for line in f:
            total+=1
            ts,lvl,msg=parse_line(line.rstrip('\n'))
            if lvl:
                counts[lvl]=counts.get(lvl,0)+1
            if ts:
                if earliest is None or ts<earliest:
                    earliest=ts
                if latest is None or ts>latest:
                    latest=ts
    print(f"