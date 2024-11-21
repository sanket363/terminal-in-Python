import os
import sys
import readline
import subprocess
import atexit
from colors import Colors, colorize
import stat
import time
import ctypes
from ctypes import wintypes
from prettytable import PrettyTable
try:
    import pwd  # Unix-specific module
    import grp   # Unix-specific module
except ImportError:
    pwd = None
    grp = None

# Define builtins dictionary and aliases
builtins = {}
aliases = {}
history_file = ".custom_shell_history"
directory_stack = []

# Load command history if available
try:
    readline.read_history_file(history_file)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, history_file)

# Basic built-in commands
def echo_command(args):
    print(" ".join(args))

def clear_command(args):
    os.system('cls' if os.name == 'nt' else 'clear')

def pwd_command(args):
    """Print the current working directory."""
    print(os.getcwd())  # Print the full absolute path of the current directory

def pwd_command(args):
    print(os.getcwd())  # Print working directory

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

# def cd_command(args):
#     if not args:
#         print("cd: missing operand")
#         return
#     try:
#         os.chdir(args[0])
#     except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
#         print(f"cd: {args[0]}: {str(e)}")

def cd_command(args):
    # If no arguments are given, change to the home directory
    if not args:
        target_directory = os.environ.get('HOME', os.path.expanduser("~"))  # Use HOME or fallback to default
    else:
        target_directory = args[0]

        # Check if the target directory is '~'
        if target_directory == '~':
            target_directory = os.environ.get('HOME', os.path.expanduser("~"))  # Use HOME or fallback to default

    try:
        os.chdir(target_directory)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        print(f"cd: {target_directory}: {str(e)}")

def get_owner_group_windows(file_path):
    """Get the owner and group of a file on Windows."""
    owner = "N/A"
    group = "N/A"

    # Prepare buffers
    owner_sid = ctypes.POINTER(ctypes.c_void_p)()
    group_sid = ctypes.POINTER(ctypes.c_void_p)()
    sd = ctypes.POINTER(ctypes.c_void_p)()

    # Retrieve owner and group information
    if ctypes.windll.advapi32.GetNamedSecurityInfoW(
        file_path,
        1,  # SE_FILE_OBJECT
        7,  # OWNER_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION
        ctypes.byref(owner_sid),
        ctypes.byref(group_sid),
        None,
        None,
        ctypes.byref(sd)
    ) == 0:  # ERROR_SUCCESS
        owner_name = ctypes.create_unicode_buffer(256)
        owner_domain = ctypes.create_unicode_buffer(256)
        owner_name_size = wintypes.DWORD(256)
        owner_domain_size = wintypes.DWORD(256)
        sid_name_use = wintypes.DWORD()

        if ctypes.windll.advapi32.LookupAccountSidW(
            None,
            owner_sid,
            owner_name,
            ctypes.byref(owner_name_size),
            owner_domain,
            ctypes.byref(owner_domain_size),
            ctypes.byref(sid_name_use)
        ):
            owner = f"{owner_domain.value}\\{owner_name.value}"

        group_name = ctypes.create_unicode_buffer(256)
        group_domain = ctypes.create_unicode_buffer(256)
        group_name_size = wintypes.DWORD(256)
        group_domain_size = wintypes.DWORD(256)

        if ctypes.windll.advapi32.LookupAccountSidW(
            None,
            group_sid,
            group_name,
            ctypes.byref(group_name_size),
            group_domain,
            ctypes.byref(group_domain_size),
            ctypes.byref(sid_name_use)
        ):
            group = f"{group_domain.value}\\{group_name.value}"

    return owner, group

def ls_command(args):
    directory = args[0] if args else '.'
    table = PrettyTable()
    table.field_names = ["Permissions", "Owner", "Group", "Size (Bytes)", "Last Modified", "File Name"]

    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            file_stats = os.stat(item_path)

            # Get permission bits
            permissions = stat.filemode(file_stats.st_mode)

            # Get owner and group names
            if os.name == 'nt':  # Windows
                owner, group = get_owner_group_windows(item_path)
            else:  # Unix-like
                owner = pwd.getpwuid(file_stats.st_uid).pw_name
                group = grp.getgrgid(file_stats.st_gid).gr_name

            # Get file size and last modified time
            size = file_stats.st_size
            last_modified = time.ctime(file_stats.st_mtime)  # Convert to human-readable format

            # Add row to the table
            table.add_row([permissions, owner, group, size, last_modified, item])

        # Print the table
        print(table)

    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        print(f"ls: cannot access '{directory}': {str(e)}")
    except Exception as e:
        print(f"Error retrieving file information: {str(e)}")
# Extended built-in commands
def export_command(args):
    if len(args) != 1 or '=' not in args[0]:
        print("export: invalid format, use VAR=VALUE")
        return
    var, value = args[0].split('=', 1)
    os.environ[var] = value

def env_command(args):
    for var, value in os.environ.items():
        print(f"{var}={value}")

def help_command(args):
    print("Available commands:")
    for cmd in builtins:
        print(f" - {cmd}")

def alias_command(args):
    if len(args) != 1 or '=' not in args[0]:
        print("alias: invalid format, use NAME=COMMAND")
        return
    name, command = args[0].split('=', 1)
    aliases[name] = command

def pushd_command(args):
    if not args:
        print("pushd: missing directory argument")
        return
    try:
        directory_stack.append(os.getcwd())
        os.chdir(args[0])
        print(os.getcwd())
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        print(f"pushd: {args[0]}: {str(e)}")

def popd_command(args):
    if not directory_stack:
        print("popd: directory stack is empty")
        return
    try:
        os.chdir(directory_stack.pop())
        print(os.getcwd())
    except Exception as e:
        print(f"popd: error: {str(e)}")

def find_command(args):
    directory = args[0] if args else '.'
    pattern = args[1] if len(args) > 1 else ''
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern in file:
                print(os.path.join(root, file))

def history_command(args):
    with open(history_file, 'r') as f:
        for line in f:
            print(line.strip())

def time_command(args):
    if not args:
        print("time: missing command")
        return

    command = " ".join(args)  # Join the arguments to form the command
    start_time = time.time()
    
    # Execute the command
    result = subprocess.run(command, shell=True)  # Set shell=True to allow string commands
    duration = time.time() - start_time
    print(f"Command executed in {duration:.2f} seconds")

def file_completer(text, state):
    options = [f for f in os.listdir('.') if f.startswith(text)]
    return options[state] if state < len(options) else None

readline.set_completer(file_completer)
readline.parse_and_bind("tab: complete")

# Add built-in commands to dictionary
builtins.update({
    'echo': echo_command,
    'pwd': pwd_command,
    'exit': lambda args: sys.exit(0),
    'pwd': pwd_command,
    'type': type_builtin,
    'clear': clear_command,
    'cd': cd_command,
    'ls': ls_command,
    'export': export_command,
    'env': env_command,
    'help': help_command,
    'alias': alias_command,
    'pushd': pushd_command,
    'popd': popd_command,
    'find': find_command,
    'time': time_command,
    'history': history_command,  # Add history command
})

# Tab-completion setup
def general_completer(text, state):
    options = [cmd for cmd in list(builtins.keys()) + list(aliases.keys()) if cmd.startswith(text)]
    return options[state] if state < len(options) else None

readline.set_completer(general_completer)
readline.parse_and_bind("tab: complete")

# Command execution and parsing
def process_aliases(cmd):
    cmd_parts = cmd.split()
    global aliases  # Make sure to access global alias dictionary
    if cmd_parts[0] in aliases:
        return aliases[cmd_parts[0]].split() + cmd_parts[1:]
    return cmd_parts

def execute_command(cmd):
    try:
        cmd_line = " ".join(cmd)
        if '&&' in cmd_line:
            commands = cmd_line.split('&&')
            for command in commands:
                subprocess.run(command.strip().split())
        elif '|' in cmd_line:
            parts = cmd_line.split('|')
            process = subprocess.Popen(parts[0].strip().split(), stdout=subprocess.PIPE)
            for part in parts[1:]:
                process = subprocess.Popen(part.strip().split(), stdin=process.stdout, stdout=subprocess.PIPE)
            output, _ = process.communicate()
            print(output.decode())
        elif '>' in cmd_line:
            cmd, file = cmd_line.split('>')
            with open(file.strip(), 'w') as f:
                subprocess.run(cmd.strip().split(), stdout=f)
        elif cmd_line.endswith("&"):
            cmd_line = cmd_line[:-1].strip()
            subprocess.Popen(cmd_line.split())
        else:
            subprocess.run(cmd_line.split())
    except Exception as e:
        print(f"Error executing command: {str(e)}")

# Command prompt customization
def custom_prompt():
    return colorize(f"{os.getcwd()} $ ", Colors.SAPPHIRE)

# Main loop
def main():
    sys.stdout.flush()
    while True:
        input_line = input(custom_prompt()).strip()
        if not input_line:
            continue
        cmd_parts = process_aliases(input_line)
        cmd, *args = cmd_parts
        if cmd in builtins:
            builtins[cmd](args)
        else:
            execute_command([cmd] + args)

if __name__ == "__main__":
    main()
