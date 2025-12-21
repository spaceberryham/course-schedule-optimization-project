from schedule_combinations import generate_valid_schedules
from converter import convert_schedule_lynes
from visualizer import vysualize

# UPDATE THE classes VARIABLE and MIN_GAP_MINUTES constant
classes = [
    [
        {'day': 'MTW', 'name': 'World History H 20', 'begtime': '9:30', 'endtime': '10:50'},
        {'day': 'MWF', 'name': 'World History H 20', 'begtime': '8:30', 'endtime': '8:50'},
        {'day': 'TR', 'name': 'World History H 20', 'begtime': '9:30', 'endtime': '10:50'},
    ],
    [
        {'day': 'MWF', 'name': 'English 21', 'begtime': '11:00', 'endtime': '11:50'},
    ],
    [
        {'day': 'TR', 'name': 'Science 21', 'begtime': '12:30', 'endtime': '13:50'},
    ],
    [
        {'day': 'MW', 'name': 'PSYCH 221-0', 'begtime': '15:30', 'endtime': '16:50'}
    ],

]
MIN_GAP_MINUTES = 1

valid = generate_valid_schedules(classes, MIN_GAP_MINUTES)
print(f"{len(valid)} valid schedules found.")

for i, schedule in enumerate(valid, start=1):
    print(f"\n=== Showing Schedule {i} ===")

    # Convert schedule dicts to the text format that converter expects
    text_lines = [
        f"{c['day']} - {c['name']} from {c['begtime']} to {c['endtime']}"
        for c in schedule
    ]

    converted = convert_schedule_lynes(text_lines)
    vysualize(converted)