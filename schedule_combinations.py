from datetime import datetime
from itertools import product
from datetime import timedelta

def time_to_dt(time_str):
    return datetime.strptime(time_str, '%H:%M')

def expand_days(day_str):
    return list(day_str)  # 'MWF' -> ['M', 'W', 'F']

def has_overlap(classes):
    for i in range(len(classes)):
        for j in range(i + 1, len(classes)):
            days1 = set(expand_days(classes[i]['day']))
            days2 = set(expand_days(classes[j]['day']))
            if days1 & days2:
                begtime1 = time_to_dt(classes[i]['begtime'])
                endtime1 = time_to_dt(classes[i]['endtime'])
                begtime2 = time_to_dt(classes[j]['begtime'])
                endtime2 = time_to_dt(classes[j]['endtime'])
                if begtime1 < endtime2 and begtime2 < endtime1:
                    return True
    return False

def has_conflict_or_insufficient_gap(classes, min_gap_minutes=1):
    min_gap = timedelta(minutes=min_gap_minutes)

    # Check all pairs of classes
    for i in range(len(classes)):
        for j in range(i + 1, len(classes)):
            days1 = set(expand_days(classes[i]['day']))
            days2 = set(expand_days(classes[j]['day']))

            common_days = days1 & days2
            if common_days:
                beg1 = time_to_dt(classes[i]['begtime'])
                end1 = time_to_dt(classes[i]['endtime'])
                beg2 = time_to_dt(classes[j]['begtime'])
                end2 = time_to_dt(classes[j]['endtime'])

                # Determine temporal relationship
                if beg1 < end2 and beg2 < end1:
                    # Overlapping classes
                    return True
                elif end1 <= beg2:
                    # Gap between end1 -> beg2
                    gap = beg2 - end1
                    if gap < min_gap:
                        return True
                elif end2 <= beg1:
                    # Gap between end2 -> beg1
                    gap = beg1 - end2
                    if gap < min_gap:
                        return True

    return False

# THIS IS THE METHOD USED BY run_all.py
# CREATES ALL POSSIBLE SCHEDULES AND CHECKS FOR OVERLAPS
def generate_valid_schedules(classes, min_gap_minutes):
    """Return a list of valid schedule combos (each a tuple of class dicts)."""
    all_combinations = list(product(*classes))
    valid_schedules = [combo for combo in all_combinations
            if not has_conflict_or_insufficient_gap(combo, min_gap_minutes)]

    with open('valid_schedules.txt', 'w') as file:
        i = 1
        for schedule in valid_schedules:
            file.write("Schedule " + str(i) + ":\n")
            for cls in schedule:
                file.write(f"{cls['day']} - {cls['name']} from {cls['begtime']} to {cls['endtime']}\n")
            file.write("\n")
            i += 1

    print("Valid schedules have been written to 'valid_schedules.txt'.")

    return valid_schedules
