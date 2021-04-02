import inspect
import os

colors = {
    "red" : (255,0,0),
    "green" : (0,255,0),
    "blue" : (0,0,255),
    "grey" : (204,204,204),
    "hot pink" : (255,105,180)
}

def colored(*text, color="grey") -> str:
    """
    Colorize a tuple of strings based on the given color
 
    *text: str
        String(s) to colorize
    color: str OR tuple
        String with the color name OR Tuple with the RGB color code
    """
    if type(color) == str:
        try:
            color = colors[color]
        except KeyError:
            color = colors["grey"]
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(color[0], color[1], color[2], " ".join(map(str,text)))

def log_msg(*msg, color="grey") -> str:
    """
    Logs a message with a given color. Also logs the file and the line number of the logged message

    *msg: str
        String(s) to log
    color: str OR tuple
        String with the color name OR Tuple with the RGB color code
    """
    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    file_line_info = f"{os.path.basename(i.filename)}:{i.lineno}"
    file_line_info = f"{file_line_info:<30}\t| "
    print(colored(file_line_info, *msg, color=color)) 

if __name__ == "__main__":    
    log_msg("test1", color="hot pink")
    log_msg("test2","extra arg" ,color="green")
    log_msg("test3", color="red")
    log_msg("test4", color="")