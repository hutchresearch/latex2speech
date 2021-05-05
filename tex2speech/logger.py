from collections import defaultdict
import os.path
import configparser
from datetime import datetime

# Usage: call log("my tag", "warning/info/debugging statement")
# To view content with your tag, call view_log("my tag")

CONFIG_FILE = 'logger_config.cfg'

enabled = True
log_timestamps = False
output_file = "console"

initialized = False

logs_dict = defaultdict(list)

def prepend_time(value):
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    return time_str + ' >> ' + value

def log(tag, value):
    global initialized
    global enabled
    if not initialized:
        read_config()
    if enabled:
        if log_timestamps:
            value = prepend_time(value)
        logs_dict[tag].append(value)

def showlog(tag):
    if output_file == 'console':
        for log_item in logs_dict[tag]:
            print(log_item)
    else:
        f = open(output_file, 'w')
        for log_item in logs_dict[tag]:
            f.write(log_item)
        f.close()
        
def clearlog(tag):
    logs_dict[tag] = []

def read_config():
    global enabled
    global log_timestamps
    global output
    global initialized
    cfg_parser = configparser.ConfigParser()
    cfg_parser.readfp(open(CONFIG_FILE, 'r'))
    enabled = (cfg_parser.get('Logger Settings', 'enabled') == 'True')
    log_timestamps = (cfg_parser.get('Logger Settings', 'log_timestamps') == 'True')
    output = cfg_parser.get('Logger Settings', 'output')

    if not enabled:
        print("Notice: Logger is disabled. Debugging statements will not print or output.")

    initialized = True