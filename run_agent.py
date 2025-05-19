import asyncio
import os


BUG_FIX_PROMPT_TEMPLATE = """
You are an expert Python programming assistant specialized in fixing single-line bugs.
I will provide you with a problem description, the path to a file, and a snippet of the code from that file containing an error.
Your task is to identify the single incorrect line within the provided code snippet and provide the corrected version of ONLY that line.

Problem Description:
{problem_statement}

File Path:
{file_path}

Buggy Code Snippet (with line numbers from original file):
```python
{code_snippet}
```

Based only on the problem description and the provided code snippet, please identify the line number that needs correction and provide the single corrected line of code.
Do not provide explanations or surrounding code.
If you believe a fix requires changing more than one line, or if you cannot determine a fix from the given information, please state: "MULTI_LINE_FIX_NEEDED_OR_CANNOT_DETERMINE"

Output format:
LINE: <line_number_of_the_buggy_line_in_snippet_or_original_file>
FIX: <the_corrected_line_of_code>
"""

def get_code_snippet_from_local_file(full_file_path: str, target_line_num: int, window: int = 7) -> tuple[str, int]:
    """
    Reads a snippet of code from a local file around a target line.
    Returns the snippet (with original file line numbers prepended) and the starting line number of the snippet.
    Line numbers are 1-based.
    """
    try:
        with open(full_file_path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f.readlines()]

        target_line_idx = target_line_num - 1 
        
        start_idx = max(0, target_line_idx - window)
        end_idx = min(len(lines), target_line_idx + window + 1) 
        
        snippet_with_line_numbers = []
        for i in range(start_idx, end_idx):
            snippet_with_line_numbers.append(f"{i + 1:04d}: {lines[i]}") 
        
        return "\n".join(snippet_with_line_numbers), start_idx + 1
    except FileNotFoundError:
        return f"Error: File not found at {full_file_path}", -1
    except Exception as e:
        return f"Error reading file: {str(e)}", -1

async def main():
    bug_info = {
        "instance_id": "django__django-11049",
        "repo": "django/django",
        "base_commit": "17455e924e243e7a55e8a38f45966d8cbb27c273",
        "file_path_in_repo": "django/db/models/fields/__init__.py",
        "problem_statement": "Correct expected format in invalid DurationField error message. If you enter a duration '14:00' into a duration field, it translates to '00:14:00' which is 14 minutes. The current error message for invalid DurationField says that this should be in [DD] [HH:[MM:]]ss[.uuuuuu] format, but it should be more explicit about how to represent days and negative durations.",
        "approx_buggy_line_in_file": 1589
    }

    local_buggy_file_full_path = "./chosen_buggy_code.py" 

    print(f"Attempting to prepare context for bug: {bug_info['instance_id']}")
    print(f"Using local file copy: {local_buggy_file_full_path}")
    print(f"Targeting approximate buggy line in original file: {bug_info['approx_buggy_line_in_file']}")

    if not os.path.exists(local_buggy_file_full_path):
        print(f"ERROR: The file '{local_buggy_file_full_path}' was not found in your project root.")
        print(f"Please ensure '{local_buggy_file_full_path}' exists and contains the buggy code.")
        return

    code_snippet, snippet_start_line = get_code_snippet_from_local_file(
        local_buggy_file_full_path,
        bug_info["approx_buggy_line_in_file"],
        window=5 
    )

    if "Error:" in code_snippet:
        print(f"Error getting code snippet: {code_snippet}")
        return

    print("\n--- Code Snippet (lines from original file) ---")
    print(code_snippet)
    print(f"(Snippet starts at line {snippet_start_line} of chosen_buggy_code.py)")
    print("--- End of Code Snippet ---")

    message_to_agent = BUG_FIX_PROMPT_TEMPLATE.format(
        problem_statement=bug_info["problem_statement"],
        file_path=bug_info["file_path_in_repo"], 
        code_snippet=code_snippet
    )

    print("\n" + "="*25 + " MESSAGE FOR AGENT (Copy this entire block) " + "="*25)
    print(message_to_agent)
    print("="*90)

    print("\n--- HOW TO RUN YOUR AGENT ---")
    print("1. Make sure your virtual environment is activated")
    print("2. Ensure GOOGLE_API_KEY environment variable is set")
    print("3. Run: adk web my_agent_code")
    print("4. Copy and paste the message above into the agent's input field")

if __name__ == "__main__":
    asyncio.run(main())
