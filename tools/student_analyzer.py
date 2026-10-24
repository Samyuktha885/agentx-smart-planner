
"""Analyze student performance from the challenge CSV dataset."""

import csv

from tools.data_query import _path
from tools import Tool


class StudentAnalyzer(Tool):
    name = "student_analyzer"
    description = (
        "Analyze scores.csv to calculate a student's average score "
        "and identify weaker subjects. Arguments: student_id."
    )
    args_doc = '{"student_id": "S1"}'

    def execute(self, student_id="S1", **kwargs):
        try:
            with open(_path("scores.csv"), newline="", encoding="utf-8-sig") as file:
                rows = list(csv.DictReader(file))

            if not rows:
                return {"error": "scores.csv contains no records."}

            columns = rows[0].keys()
            id_column = next(
                (c for c in columns if c.lower().strip() in
                 ("student_id", "student", "studentid", "id")),
                None,
            )

            if not id_column:
                return {
                    "error": "Could not identify the student ID column.",
                    "available_columns": list(columns),
                }

            student_rows = [
                row for row in rows
                if row.get(id_column, "").strip().lower()
                == str(student_id).strip().lower()
            ]

            if not student_rows:
                return {"error": f"No records found for student {student_id}."}

            score_columns = [
                c for c in columns
                if c != id_column and any(
                    word in c.lower()
                    for word in ("score", "mark", "math", "science",
                                 "english", "topic", "subject")
                )
            ]

            scores = {}
            for row in student_rows:
                for column in score_columns:
                    try:
                        value = float(row[column])
                        scores.setdefault(column, []).append(value)
                    except (ValueError, TypeError):
                        continue

            if not scores:
                return {
                    "error": "No numeric score columns detected.",
                    "available_columns": list(columns),
                }

            results = {
                subject: round(sum(values) / len(values), 2)
                for subject, values in scores.items() if values
            }

            return {
                "student_id": student_id,
                "subject_averages": results,
                "overall_average": round(
                    sum(results.values()) / len(results), 2
                ),
                "weakest_subjects": sorted(
                    results, key=results.get
                )[:min(3, len(results))],
            }

        except FileNotFoundError:
            return {"error": "scores.csv was not found in the data folder."}
