
"""Analyze student scores grouped by topic."""

import csv
from collections import defaultdict

from tools import Tool
from tools.data_query import _path


class StudentAnalyzer(Tool):
    name = "student_analyzer"
    description = (
        "Analyze student performance by topic. "
        "Arguments: student_id (for example S1)."
    )
    args_doc = '{"student_id": "S1"}'

    def execute(self, student_id="S1", **kwargs):
        try:
            with open(
                _path("scores.csv"),
                newline="",
                encoding="utf-8-sig",
            ) as file:
                reader = csv.DictReader(file)
                headers = {
                    name.strip().lower(): name for name in (reader.fieldnames or [])
                }

                if not all(key in headers for key in ("student", "topic", "score")):
                    return {
                        "error": "Expected CSV columns: Student, Topic, Score."
                    }

                scores = defaultdict(list)

                for row in reader:
                    if row[headers["student"]].strip().lower() != str(student_id).strip().lower():
                        continue

                    topic = row[headers["topic"]].strip()
                    try:
                        score = float(row[headers["score"]])
                    except (ValueError, TypeError):
                        continue

                    if topic:
                        scores[topic].append(score)

            if not scores:
                return {
                    "error": f"No valid scores found for student {student_id}."
                }

            averages = {
                topic: round(sum(values) / len(values), 2)
                for topic, values in scores.items()
            }

            return {
                "student": student_id,
                "topic_averages": averages,
                "overall_average": round(
                    sum(averages.values()) / len(averages), 2
                ),
                "weakest_topics": sorted(
                    averages, key=averages.get
                )[:min(3, len(averages))],
            }

        except FileNotFoundError:
            return {"error": "scores.csv was not found in the data folder."}
