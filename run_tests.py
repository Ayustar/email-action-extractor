from pathlib import Path
from week2_tool import summarise_email

RUNS = 2

for path in sorted(Path("fresh_email").glob("*.txt")):
    text = path.read_text(encoding="utf-8")
    print("=" * 60)
    print(path.name)
    for run in range(1, RUNS + 1):
        print(f"--- Run {run} ---")
        result = summarise_email(text)
        if result is None:
            print("No summary produced.")
            continue
        print("Summary:", result.summary)
        if not result.action_items:
            print("(no action items)")
        for item in result.action_items:
            print("-", item.task, "| deadline:", item.deadline, "| condition:", item.condition)