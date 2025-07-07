import math
import json
import sys

def load_config(path='config.json'):
    """Load configuration JSON from a file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file {path} not found. Exiting.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Config file {path} is not valid JSON. Exiting.")
        sys.exit(1)

def build_allowed_functions(config):
    """Build dict of allowed math functions from config."""
    return {name: getattr(math, name) for name in config.get("allowed_functions", [])}

def print_welcome_message(config):
    """Print welcome and instructions from config."""
    print(config.get("welcome_message", "Welcome!"))
    for line in config.get("instructions", []):
        print(line)
    print()

def evaluate_expression(expr, allowed_functions):
    """Evaluate the user expression safely."""
    try:
        return eval(expr, {"__builtins__": None}, {"math": math, **allowed_functions})
    except ZeroDivisionError:
        return "❌ Error: Division by zero is not allowed."
    except ValueError as ve:
        return f"❌ Value Error: {ve}"
    except SyntaxError:
        return "❌ Syntax Error: Please enter a valid mathematical expression."
    except NameError:
        return "❌ Name Error: Use only allowed functions and variables (like math.sqrt)."
    except Exception as e:
        return f"❌ Unexpected Error: {e}"

def main_loop(config):
    """Main input loop."""
    allowed_functions = build_allowed_functions(config)
    exit_command = config.get("exit_command", "exit")

    print_welcome_message(config)

    while True:
        user_input = input("Enter your expression: ").strip()
        if user_input.lower() == exit_command:
            print("Thanks for using the calculator!")
            break

        result = evaluate_expression(user_input, allowed_functions)
        print(f"Result: {result}\n")

if __name__ == '__main__':
    # Optionally allow passing the config file path via the command line
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    config = load_config(config_path)
    main_loop(config)
