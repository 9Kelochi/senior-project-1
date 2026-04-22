import json
import os
import pandas as pd

EXPT_NAME = "2026-04-20_exp_0"
BASE_DIR = "expt-logs"
INPUT_PATH = os.path.join(BASE_DIR, EXPT_NAME, "agent-logs-compact.json")
OUTPUT_PATH = "./linear-probes/data/Roleplaying/phi4_rollouts.csv"

rows = []


with open(INPUT_PATH, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        row = json.loads(line)

        rows.append({
            "scenario": row.get("interaction.system_prompt", ""),
            "question": (
                f"Summarization: {row.get('interaction.prompt.Summarization', '')}\n\n"
                f"{row.get('interaction.prompt.All Info', '')}\n\n"
                f"Memory: {row.get('interaction.prompt.Memory', '')}\n\n"
                f"Phase: {row.get('interaction.prompt.Phase', '')}. Return your output."
            ),
            "answer_prefix": "",
            "phi4_rollout": row.get("interaction.full_response", ""),
            "llm_eval_gt": 0 if row.get("player.identity") == "Impostor" else 1,
        })

df = pd.DataFrame(rows)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"Saved {len(df)} rows to {OUTPUT_PATH}")
print(df.head())