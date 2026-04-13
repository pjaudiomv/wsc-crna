#!/usr/bin/env python3
"""Parse CarolinaRegion2026GroupCarTally.csv and print the JS AREAS array."""

import csv
import sys
from collections import defaultdict

CSV_PATH = "CarolinaRegion2026GroupCarTally.csv"
MOTION_COLS = [7, 9, 11, 13, 15]  # columns for Motion 1–5 votes


def main():
    # area_name -> { motion_index -> {y, n, a} }
    areas = defaultdict(lambda: {i: {"y": 0, "n": 0, "a": 0} for i in range(5)})
    area_groups = defaultdict(set)

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            area = row[6].strip()
            group = row[5].strip()
            if not area:
                continue
            area_groups[area].add(group)
            for mi, col in enumerate(MOTION_COLS):
                vote = row[col].strip().lower()
                if vote == "yes":
                    areas[area][mi]["y"] += 1
                elif vote == "no":
                    areas[area][mi]["n"] += 1
                elif vote == "abstain":
                    areas[area][mi]["a"] += 1

    # Sort areas alphabetically
    sorted_areas = sorted(areas.keys())

    # Find longest name for alignment
    max_name = max(len(a) for a in sorted_areas)

    lines = ["// motions array: index 0 = Motion 1 … 4 = Motion 5 → { y, n, ab }"]
    lines.append("const AREAS = [")
    for area in sorted_areas:
        g = len(area_groups[area])
        motions = areas[area]
        m_parts = []
        for i in range(5):
            m = motions[i]
            m_parts.append(f"{{y:{m['y']},n:{m['n']},a:{m['a']}}}")
        m_str = ",".join(m_parts)
        padded = f"'{area}'"
        lines.append(f"  {{ name:{padded:<{max_name + 2}}, g:{g:<3}, m:[{m_str}] }},")
    lines.append("];")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
