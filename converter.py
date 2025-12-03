import re

def convert_schedule_text(schedule_text):
    lines = schedule_text.splitlines()
    return convert_schedule_lynes(lines)

# THIS IS THE METHOD USED BY run_all.py
# CONVERT EACH LINE TO A DICTIONARY
def convert_schedule_lynes(lines):
    output = []
    for line in lines:
        match = re.match(r"(\w+) - (.+?) from (\d{1,2}:\d{2}) to (\d{1,2}:\d{2})", line)
        if match:
            days, name, begtime, endtime = match.groups()
            output.append({
                'days': days,
                'name': name.strip(),
                'begtime': begtime,
                'endtime': endtime
            })
    return output


