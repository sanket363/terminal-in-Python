# colorscheme.py

# Define color escape codes for different colors in the scheme.
class Colors:
    ROSEWATER = "\033[38;2;242;213;207m"
    FLAMINGO = "\033[38;2;238;190;190m"
    PINK = "\033[38;2;244;184;228m"
    MAUVE = "\033[38;2;202;158;230m"
    RED = "\033[38;2;231;130;132m"
    MAROON = "\033[38;2;234;153;156m"
    PEACH = "\033[38;2;239;159;118m"
    YELLOW = "\033[38;2;229;200;144m"
    GREEN = "\033[38;2;166;209;137m"
    TEAL = "\033[38;2;129;200;190m"
    SKY = "\033[38;2;153;209;219m"
    SAPPHIRE = "\033[38;2;133;193;220m"
    BLUE = "\033[38;2;140;170;238m"
    LAVENDER = "\033[38;2;186;187;241m"
    RESET = "\033[0m"

def colorize(text, color):
    return f"{color}{text}{Colors.RESET}"
