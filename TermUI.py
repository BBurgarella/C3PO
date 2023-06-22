import os
import shutil
import textwrap

OK = '\033[92m'
WARN = '\033[93m'
ERR = '\033[31m'
UNDERLINE = '\033[4m'
ITALIC = '\x1B[3m'
BOLD = '\033[1m'
BLUE = '\033[94m'
ENDC = '\033[0m'

HEADER = '\033[95m' + BOLD
PASS = OK + BOLD
FAIL = ERR + BOLD

OKMSG = BOLD + OK + u'\u2705' + "  "
ERRMSG = BOLD + FAIL + u"\u274C" + "  "
WAITMSG = BOLD + WARN + u'\u231b' + "  "

HELP = WARN
BITALIC = BOLD + ITALIC
BLUEIC = BITALIC + OK
END = ENDC

def print_conversation(conversation):
    os.system('cls' if os.name == 'nt' else 'clear')  # cls pour Windows, clear pour Unix
    system_msg, user_msg, assistant_msg = "", "", ""

    for item in conversation:
        if item['role'] == 'system':
            system_msg = item['content']
        elif item['role'] == 'user':
            user_msg = item['content']
        elif item['role'] == 'assistant':
            assistant_msg = item['content']

    term_size = shutil.get_terminal_size()
    term_width = term_size.columns
    adjusted_width = int(term_width * 0.8)  # Utiliser 80% de la largeur du terminal
    half_width = adjusted_width // 2 - 3  # -3 for padding and '|'

    def print_line(msg, width):
        lines = textwrap.wrap(msg, width)
        for line in lines:
            print(OK +"| " + line + " " * (width - len(line)) + " |"+ END)
        return len(lines)

    print(OK +"+" + "-" * (adjusted_width - 2) + "+"+ END)
    print(OK + "| SYSTEM MESSAGE: "+ END)
    print_line(system_msg, adjusted_width - 4)  # -4 pour tenir compte des espaces de marge et du symbole '|'
    print(OK + "+" + "-" * (adjusted_width - 2) + "+" + END)

    user_lines = textwrap.wrap(user_msg, half_width)
    assistant_lines = textwrap.wrap(assistant_msg, half_width)
    max_lines = max(len(user_lines), len(assistant_lines))

    # Print user and assistant messages side by side
    for i in range(max_lines):
        user_line = user_lines[i] if i < len(user_lines) else ""
        assistant_line = assistant_lines[i] if i < len(assistant_lines) else ""
        print(BLUE + "| " + user_line.ljust(half_width) + ENDC + "| "+ WARN + assistant_line.ljust(half_width) + " |" + ENDC)

    print("+" + "-" * (adjusted_width - 2) + "+")