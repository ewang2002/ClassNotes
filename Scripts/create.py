import os 
import sys
import datetime
from typing import List, Tuple

CLASSES = {
    'CSE105': {
        'full': True,
        'schedule': ['M', 'W'],
        'class': 'CSE 105'
    },
    'CSE101': {
        'full': True,
        'schedule': ['M', 'W', 'F'],
        'class': 'CSE 101'
    },
    'MATH103B': {
        'full': True,
        'schedule': ['M', 'Tu', 'W', 'F'],
        'class': 'Math 103B'
    }
}

DAY_OF_WEEK = ['M', 'Tu', 'W', 'Th', 'F', 'Sa', "Su"]
TEMPLATE_FILE = "template.txt"
LEC_TEMPLATE = "{lec}"
DATE_TEMPLATE = "{date}"
CLASS_TEMPLATE = "{class}"
PREAMBLE_TEMPLATE = "{preamble}"

def validate_template() -> Tuple[str, bool]:
    """
    Validates the template tex file.
    """
    with open(TEMPLATE_FILE, 'r') as template:
        content = template.read()
        return content, LEC_TEMPLATE in content \
            and DATE_TEMPLATE in content \
            and CLASS_TEMPLATE in content \
            and PREAMBLE_TEMPLATE in content

def get_last_lec_num(c: str) -> int:
    """
    Returns the last lecture number for a given class.
    """
    dir = get_path(c)
    # check if dir exists
    if not os.path.isdir(dir):
        return -1
    # get all files in dir
    files = [int(file.replace(".tex", "").replace("Lec", "")) for file in os.listdir(dir) if file.endswith(".tex")]
    return (0 if len(files) == 0 else max(files)) + 1

def get_path(c: str) -> str:
    """
    Returns the path to the given lecture.
    """
    return os.path.join("..", "PendingClasses", c, "LectureNotes") if CLASSES[c]['full'] else os.path.join("..", "PendingClasses", c)

make_today = len(sys.argv) > 1 and sys.argv[1].lower() in ["today", "t"]
template, is_valid = validate_template()
if not is_valid:
    print("Template file is not valid!")
    exit(1)

num_added = 0
next_date = datetime.date.today() if make_today else datetime.datetime.now() + datetime.timedelta(days=1)
for k in CLASSES:
    if DAY_OF_WEEK[next_date.weekday()] not in CLASSES[k]['schedule']:
        continue 
    last_lec_num = get_last_lec_num(k)
    preamble = "../../../preamble.tex" if CLASSES[k]['full'] else "../../preamble.tex"
    date = next_date.strftime("%A, %B %d, %Y")
    new_file = template.replace(LEC_TEMPLATE, "Lecture " + str(last_lec_num)) \
        .replace(DATE_TEMPLATE, date) \
        .replace(CLASS_TEMPLATE, CLASSES[k]['class']) \
        .replace(PREAMBLE_TEMPLATE, preamble)

    with open(os.path.join(get_path(k), f"Lec{last_lec_num}.tex"), 'w') as f:
        f.write(new_file)
    
    print(f"Created {CLASSES[k]['class']} - {date}")
    num_added += 1

print(f"Added {num_added} lectures.")
input("Press enter to exit...")