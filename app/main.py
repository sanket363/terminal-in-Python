import os
import sys

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

# Add commands to builtins
builtins['echo'] = echo_command
builtins['exit'] = lambda args: sys.exit(0)
builtins['type'] = type_builtin
builtins['clear'] = lambda args: clear("clear")

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
