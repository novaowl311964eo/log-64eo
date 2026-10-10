#!/usr/bin/env python3
"""
Simple log parsing helper: counts log levels and prints parsed lines.
"""
import argparse, re, sys
from collections import Counter

LOG_RE = re.compile(r'\[(?P<ts>.*?)\]\s+(?P<level>[A-Z]+):\s+(?P<msg>.*)')

def parse_line(line):
    m = LOG_RE.match(line)
    if m:
        return m.groupdict()
    return None

def parse_file(fp):
    for line in fp:
        parsed = parse_line(line.rstrip('\n'))
        if parsed:
            yield parsed

def main(argv=None):
    parser = argparse.ArgumentParser(description='Parse and summarize log files')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Log file (default: stdin)')
    args = parser.parse_args(argv)
    levels = Counter()
    for entry in parse_file(args.file):
        levels[entry['level']] += 1
    print("Log level counts:")
    for level, count in levels.most_common():
        print(f"{level}: {count}")
    return 0

if __name__ == '__main__':
    sys.exit(main())