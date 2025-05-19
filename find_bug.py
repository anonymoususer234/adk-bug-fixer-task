from datasets import load_dataset

def count_changed_lines_from_patch(patch):
    if not patch:
        return 0
    lines = patch.split('\n')
    count = 0
    for line in lines:
        if line.startswith('+') and not line.startswith('+++'):
            count += 1
        elif line.startswith('-') and not line.startswith('---'):
            count += 1
    return count

try:
    dataset = load_dataset("princeton-nlp/SWE-bench_lite", split="test")
    print(f"Loaded dataset with {len(dataset)} instances")
    
    python_files = dataset.filter(lambda x: x['file_path'].endswith('.py') and 'test' not in x['file_path'].lower())
    print(f"Found {len(python_files)} Python files (excluding test files)")
    
    simple_changes = python_files.filter(lambda x: count_changed_lines_from_patch(x['patch']) == 1)
    print(f"Found {len(simple_changes)} instances with single-line changes")
    
    print("\nTop 10 candidate bugs with single-line changes:")
    for i, item in enumerate(simple_changes.select(range(min(10, len(simple_changes))))):
        print(f"\n{i+1}. Instance ID: {item['instance_id']}")
        print(f"   Repository: {item['repo']}")
        print(f"   File: {item['file_path']}")
        print(f"   Problem: {item['problem_statement']}")
        print(f"   Patch:\n{item['patch']}")

except Exception as e:
    print(f"Error loading dataset: {e}")