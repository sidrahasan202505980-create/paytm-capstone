"""
build_readme.py
One-time helper: assembles README.md from the captured run transcripts.
Not part of the graded deliverables list itself -- just a tool to avoid
manual copy-paste errors when documenting real run output.
"""

FENCE = chr(96) * 3  # builds a triple-backtick fence without writing literal backticks


def read_transcript(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


advisory = read_transcript("transcript_advisory_agent.txt")
disclosure = read_transcript("transcript_extract_disclosure.txt")
debate = read_transcript("transcript_debate.txt")
dcf = read_transcript("transcript_dfc_calculator.txt")

lines = []
lines.append("# ai_advisory_blockchain -- Part 3 Notes")
lines.append("")
lines.append("## MOCK_LLM Mode")
lines.append("")
lines.append("MOCK_LLM was left **unset** (the default) for this entire submission.")
lines.append("Every script below ran in the fully deterministic, rule-based mock mode,")
lines.append("with no signup, no API key, and no network call to any LLM provider.")
lines.append("The optional MOCK_LLM=0 extension (real LLM calls via Groq's free tier)")
lines.append("was **not** attempted for this submission, so there are no free-tier")
lines.append("usage notes to report.")
lines.append("")
lines.append("## How to reproduce these transcripts")
lines.append("")
lines.append("From inside the ai_advisory_blockchain folder, run:")
lines.append("")
lines.append(FENCE)
lines.append("python advisory_agent.py")
lines.append("python extract_disclosure.py")
lines.append("python debate.py")
lines.append("python dfc_calculator.py")
lines.append(FENCE)
lines.append("")
lines.append("All four scripts use only the local data files in this folder")
lines.append("(stock_universe.py, investor_profiles.py, disclosure_snippets.py)")
lines.append("and require no external services.")
lines.append("")
lines.append("## Recorded Run Transcript -- advisory_agent.py")
lines.append("")
lines.append(FENCE)
lines.append(advisory)
lines.append(FENCE)
lines.append("")
lines.append("## Recorded Run Transcript -- extract_disclosure.py")
lines.append("")
lines.append(FENCE)
lines.append(disclosure)
lines.append(FENCE)
lines.append("")
lines.append("## Recorded Run Transcript -- debate.py")
lines.append("")
lines.append(FENCE)
lines.append(debate)
lines.append(FENCE)
lines.append("")
lines.append("## Recorded Run Transcript -- dfc_calculator.py (includes DCF sensitivity table)")
lines.append("")
lines.append(FENCE)
lines.append(dcf)
lines.append(FENCE)
lines.append("")

readme_content = "\n".join(lines)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("README.md has been created successfully in this folder.")
print(f"Total length: {len(readme_content)} characters.")