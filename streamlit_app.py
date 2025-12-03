import streamlit as st
from schedule_combinations import generate_valid_schedules
from converter import convert_schedule_lynes
from visualizer import vysualize

import io
import zipfile

def create_zip(png_files):
    """
    png_files: list of tuples (filename, bytes_data)
    returns: bytes of the ZIP archive
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for filename, data in png_files:
            z.writestr(filename, data)
    return zip_buffer.getvalue()

st.write("Welcome to the Schedule Combination Generator!")

with st.form("input_of_courses", clear_on_submit=False, enter_to_submit=True):
    # PART 1: TAKING USER INPUT
    st.write("FORM")
    st.markdown("Enter a list of classes in the following format (use the 24-hour time format):")
    st.markdown("DATA_ENG, MWF, 09:30, 10:50")
    st.markdown("DATA_ENG, MWF, 08:00, 8:50")
    st.markdown("COMP_SCI 212-0, TR, 14:30, 15:45")
    st.markdown("COMP_SCI 212-0, TR, 15:30, 16:45")
    st.markdown("PSYH 123, M, 07:00, 07:30")
    user_cls = st.text_area("Please put one class section on each line (empty lines are acceptable), or copy and paste the above example:")
    user_gap = st.number_input("What is minimum gap (number of minutes) between classes? (Think: Passing period time)",
                    min_value=0, max_value=240, step=1)
    twenty_four_hrs_format = st.checkbox("Use the 12-hour time format (not working yet / useless button):")

    # PART 2: PARSING AND WHEN SUBMITTING FORM
    submitted_01 = st.form_submit_button(label="SUBMIT")

if submitted_01:
    st.write("Generating schedule now...")

    # ----- PARSE -----
    parsed_flat = []
    for line in user_cls.split("\n"):
        if not line.strip():
            continue
        name, day, beg, end = [x.strip() for x in line.split(",")]
        parsed_flat.append({
            "name": name,
            "day": day,
            "begtime": beg,
            "endtime": end,
        })

    # ----- GROUP -----
    from collections import defaultdict

    grouped = defaultdict(list)
    for c in parsed_flat:
        grouped[c["name"]].append(c)

    classes_for_scheduler = list(grouped.values())

    # ----- RUN SCHEDULER -----
    valid = generate_valid_schedules(classes_for_scheduler, user_gap)
    png_lyst = []

    for i, schedule in enumerate(valid, start=1):
        st.write(f"### Schedule {i}")

        # Convert to converter-friendly text
        text_lines = [
            f"{c['day']} - {c['name']} from {c['begtime']} to {c['endtime']}"
            for c in schedule
        ]

        converted = convert_schedule_lynes(text_lines)

        # Get the Matplotlib figure from vysualize()
        fig = vysualize(converted)

        # Show figure
        st.pyplot(fig)

        # Turn figure into PNG bytes
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        png_bytes = buf.getvalue()

        # Add to list for ZIP
        png_lyst.append((f"schedule_{i}.png", png_bytes))

        # Individual download button
        st.download_button(
            label=f"Download Schedule {i} as PNG",
            data=png_bytes,
            file_name=f"schedule_{i}.png",
            mime="image/png"
        )

    # ----- ZIP EXPORT -----
    if png_lyst:
        zip_bytes = create_zip(png_lyst)

        st.download_button(
            label="⬇️ Download ALL Schedules (ZIP)",
            data=zip_bytes,
            file_name="all_schedules.zip",
            mime="application/zip"
        )

