
"""Task planning tool for AgentX Smart Planner."""


class TaskPlanner:
    name = "task_planner"
    description = (
        "Break a user's goal into prioritized, actionable tasks. "
        "Arguments: goal (string), days (integer, optional)."
    )
    args_doc = '{"goal": "string", "days": 7}'

    def execute(self, goal="", days=7, **kwargs):
        if not isinstance(goal, str) or not goal.strip():
            return {"error": "Please provide a goal."}

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 7

        days = max(1, min(days, 90))
        goal = goal.strip()

        tasks = [
            {
                "priority": 1,
                "task": f"Define the desired outcome for: {goal}",
                "day": 1,
            },
            {
                "priority": 2,
                "task": "Identify requirements, resources, and constraints",
                "day": min(2, days),
            },
            {
                "priority": 3,
                "task": "Break the goal into small, measurable milestones",
                "day": min(3, days),
            },
            {
                "priority": 4,
                "task": "Work on the highest-impact milestone",
                "day": min(4, days),
            },
            {
                "priority": 5,
                "task": "Review progress and adjust the remaining plan",
                "day": days,
            },
        ]

        return {
            "goal": goal,
            "duration_days": days,
            "tasks": tasks,
            "note": (
                "This is a generic starter plan. Adapt tasks to the "
                "user's goal and verify any external facts with tools."
            ),
        }
