import streamlit as st
from datetime import timedelta
import pandas as pd


def generate_monthly_rota(names, start_date, months):
    rota = []
    current_date = start_date
    n = len(names)

    for month in range(months):
        # Rotate primaries each month
        primaries = names[month % n:] + names[:month % n]

        # Secondary logic depends on number of people
        if n >= 2:
            secondaries = [primaries[-1]] + primaries[:-1]
        else:
            secondaries = primaries[:]  # only 1 person

        for week in range(4):
            primary = primaries[week % n]

            # Try to avoid same person as secondary
            secondary = secondaries[week % n]

            if n > 1 and secondary == primary:
                # pick next person if possible
                secondary = names[(names.index(primary) + 1) % n]

            week_start = current_date
            week_end = current_date + timedelta(days=6)

            rota.append({
                "Week Start": week_start.strftime("%Y-%m-%d"),
                "Week End": week_end.strftime("%Y-%m-%d"),
                "Primary": primary,
                "Secondary": secondary
            })

            current_date += timedelta(days=7)

    return pd.DataFrame(rota)


# UI
st.title("📅 Monthly On-Call Rota (Flexible Team Size)")

names_input = st.text_input(
    "Enter names (1–4 people)",
    placeholder="Adam, Michael P, Michael M, Oskar"
)

start_date = st.date_input("Week beginning date")
months = st.number_input("Number of months", min_value=1, value=3)

if st.button("Generate Rota"):
    names = [n.strip() for n in names_input.split(",") if n.strip()]

    if len(names) == 0:
        st.error("Please enter at least one name.")
    elif len(names) > 4:
        st.error("This version supports up to 4 people.")
    else:
        df = generate_monthly_rota(names, start_date, months)

        st.dataframe(df)

        # Export
        file_name = "monthly_rota.xlsx"
        df.to_excel(file_name, index=False)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Download Excel",
                f,
                file_name=file_name
            )
