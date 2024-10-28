import os
import sys
import readline  # Use readline directly for tab completion

# Define builtins dictionary
builtins = {}

def echo_command(args):
    print(" ".join(args))

def clear(cmd):
    if "clear" in cmd or "cls" in cmd:
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For macOS and Linux
        else:
            os.system('clear')

def type_builtin(args):
    if not args:
        print("type: missing operand")
        return

    command = args[0]
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)

    for directory in path_dirs:
        potential_path = os.path.join(directory, command)
        if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
            print(f"{command} is {potential_path}")
            return

    print(f"{command}: not found")

def cd_command(args):
    if not args:
        print("cd: missing operand")
        return

    try:
        os.chdir(args[0])
    except FileNotFoundError:
        print(f"cd: {args[0]}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {args[0]}: Not a directory")
    except PermissionError:
        print(f"cd: {args[0]}: Permission denied")

def ls_command(args):
    directory = args[0] if args else '.'
    try:
        for item in os.listdir(directory):
            print(item)
    except FileNotFoundError:
        print(f"ls: cannot access '{directory}': No such file or directory")
    except NotADirectoryError:
        print(f"ls: cannot access '{directory}': Not a directory")
    except PermissionError:
        print(f"ls: cannot access '{directory}': Permission denied")

def cd_completer(text, state):
    # Get the current directory
    current_dir = os.getcwd()
    # List all directories in the current directory
    directories = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    # Filter directories based on the text entered so far
    matches = [d for d in directories if d.startswith(text)]
    # Return the match for the current state
    return matches[state] if state < len(matches) else None

# Add commands to builtins
builtins['echo'] = echo_command
builtins['exit'] = lambda args: sys.exit(0)
builtins['type'] = type_builtin
builtins['clear'] = lambda args: clear("clear")
builtins['cd'] = cd_command
builtins['ls'] = ls_command

# Enable tab completion using readline
readline.set_completer(cd_completer)
readline.parse_and_bind("tab: complete")

# Example usage
def main():
    sys.stdout.flush()

    while True:
        # Split command into parts
        input_line = input("$ ").strip().split()
        if not input_line:
            continue
        
        # Extract the command and arguments
        cmd, *args = input_line

        # Check if the command is a built-in
        if cmd in builtins:
            builtins[cmd](args)
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()

