import sys
import os
print(f"Current working directory: {os.getcwd()}")
print(f"Python sys.path: {sys.path}")
print("-" * 30)

print("Attempting to import 'my_agent_code.agent_logic' directly...")
try:
    from my_agent_code import agent_logic
    print("SUCCESS: 'my_agent_code.agent_logic' module imported.")

    if hasattr(agent_logic, 'agent'):
        print(f"SUCCESS: Found 'agent' attribute in 'agent_logic' module. Agent name: {agent_logic.agent.name}")
    else:
        print("ERROR: 'agent_logic' module was imported, but it does NOT have an 'agent' attribute defined at its top level.")

except ImportError as e:
    print(f"ERROR: Could not import 'my_agent_code.agent_logic'. ImportError: {e}")
    print("This suggests a problem with the package structure or __init__.py.")
except Exception as e:
    print(f"An unexpected error occurred during direct import test: {e}")

print("-" * 30)
print("Attempting to import 'my_agent_code' as a package and access 'agent' attribute (relies on __init__.py)...")
try:
    import my_agent_code
    print("SUCCESS: 'my_agent_code' package imported.")

    if hasattr(my_agent_code, 'agent'):
        print(f"SUCCESS: Found 'agent' attribute on 'my_agent_code' package. Agent name: {my_agent_code.agent.name}")
        print("--- The following print statements should be from agent_logic.py if loaded via __init__.py ---")
    else:
        print("ERROR: 'my_agent_code' package was imported, but it does NOT have an 'agent' attribute made available through its __init__.py.")

except ImportError as e:
    print(f"ERROR: Could not import 'my_agent_code' as a package. ImportError: {e}")
except AttributeError as e:
    print(f"ERROR: Imported 'my_agent_code' package, but got AttributeError: {e}. This means 'agent' isn't an attribute of the package.")
except Exception as e:
    print(f"An unexpected error occurred during package import test: {e}") 