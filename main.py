import math
import json
import sys
import re

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
    allowed = {name: getattr(math, name) for name in config.get("allowed_functions", [])}
    print("✅ Allowed functions:", allowed)
    return allowed


def print_welcome_message(config):
    """Print welcome,, and instructions from config."""
    print(config.get("welcome_message", "Welcome!"))
    for line in config.get("instructions", []):
        print(line)
    print()

def clean_expression(expr):
    # Remove leading zeros from whole numbers (e.g., "02" → "2")
    # Doesn't affect numbers like "0.5" or "100"
    return re.sub(r'\b0+(\d)', r'\1', expr)

def evaluate_expression(expr, allowed):
    """ Evaluate the user expression safely."""
    try:
        expr = clean_expression(expr.strip())
        if '"' in expr or "'" in expr:
            return "❌ It looks like you used quotes  — please enter only numbers and math symbols, no text"


        d = eval(expr, {"__builtins__": None}, {"math": math, **allowed})

        return  d
    except ZeroDivisionError:
        return "❌ Error: Division by zero is not allowed."
    except ValueError as ve:
        return f"❌ Value Error: {ve}"
    except SyntaxError:
        return f"❌ Syntax Error: Please enter a valid mathematical expression."
    except NameError:
        return f"❌NameError:  "

    except Exception as e:
        return f"❌ You typed something I don't recognize — please use only numbers and math symbols like +, -, *, /, or allowed functions like math.sqrt(). No random letters like 'i' or 'x' please!: {e}"

def main_loop(config):
    """Main input loop."""
    allowed = build_allowed_functions(config)
    exit_command = config.get("exit_command", "exit")

    print_welcome_message(config)

    while True:
        user_input = input("Enter your expression: ").strip()
        if user_input.lower() == exit_command:
            print("Thanks for using the calculator!")
            break

        result = evaluate_expression(user_input, allowed)
        print(f"Result: {result}\n")

if __name__ == '__main__':
    # Optionally allow passing the config file path via the command line
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    config = load_config(config_path)
    main_loop(config)
