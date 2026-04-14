import streamlit as st
from datetime import timedelta
import pandas as pd
import random


def generate_fair_rota(names, start_date, num_weeks):
    # Tracking
    last_worked = {name: -10 for name in names}
    total_assignments = {name: 0 for name in names}
    previous_pair = set()

    rota = []
    current_date = start_date

    for week in range(num_weeks):
        # Eligible = didn't work last week
        eligible = [
            n for n in names
            if last_worked[n] < week - 1
        ]

        # If not enough eligible (edge case), relax rule slightly
        if len(eligible) < 2:
            eligible = names[:]

        # Sort by least assignments (fairness)
        eligible.sort(key=lambda n: total_assignments[n])

        # Try to avoid repeating same pair
        chosen = None
        for i in range(len(eligible)):
            for j in range(i + 1, len(eligible)):
                pair = {eligible[i], eligible[j]}
                if pair != previous_pair:
                    chosen = (eligible[i], eligible[j])
                    break
            if chosen:
                break

        # Fallback if unavoidable
        if not chosen:
            chosen = (eligible[0], eligible[1])

        primary, secondary = chosen

        # Update tracking
        last_worked[primary] = week
        last_worked[secondary] = week
        total_assignments[primary] += 1
        total_assignments[secondary] += 1
        previous_pair = set(chosen)

        week_end = current_date + timedelta(days=6)

        rota.append({
            "Week Start": current_date.strftime("%Y-%m-%d"),
            "Week End": week_end.strftime("%Y-%m-%d"),
            "Primary": primary,
            "Secondary": secondary
        })

        current_date += timedelta(days=7)

    return pd.DataFrame(rota)


# UI
st.title("📅 Fair On-Call Rota Generator")

names_input = st.text_input("Enter names (comma separated)")
start_date = st.date_input("Week beginning date")
num_weeks = st.number_input("Number of weeks", min_value=1, value=6)

if st.button("Generate Rota"):
    names = [n.strip() for n in names_input.split(",") if n.strip()]

    if len(names) < 3:
        st.error("You need at least 3 people for this rota to work properly.")
    else:
        df = generate_fair_rota(names, start_date, num_weeks)

        st.dataframe(df)

        # Export to Excel
        file_name = "rota.xlsx"
        df.to_excel(file_name, index=False)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Download Excel",
                f,
                file_name=file_name
            )
