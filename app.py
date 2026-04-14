import streamlit as st
from datetime import timedelta
import pandas as pd


def generate_monthly_rota(names, start_date, months):
    rota = []
    current_date = start_date

    for month in range(months):
        # Primary order (rotate each month for fairness over time)
        primaries = names[month % len(names):] + names[:month % len(names)]

        # Secondary = rotated version (shift right by 1)
        secondaries = [primaries[-1]] + primaries[:-1]

        for week in range(4):  # 4-week cycle
            week_start = current_date
            week_end = current_date + timedelta(days=6)

            rota.append({
                "Week Start": week_start.strftime("%Y-%m-%d"),
                "Week End": week_end.strftime("%Y-%m-%d"),
                "Primary": primaries[week % len(primaries)],
                "Secondary": secondaries[week % len(secondaries)]
            })

            current_date += timedelta(days=7)

    return pd.DataFrame(rota)


# UI
st.title("📅 Monthly On-Call Rota (4-Week Cycle)")

names_input = st.text_input(
    "Enter 4 names (comma separated)",
    placeholder="Adam, Michael P, Michael M, Oskar"
)

start_date = st.date_input("Week beginning date (start of cycle)")
months = st.number_input("Number of months", min_value=1, value=3)

if st.button("Generate Rota"):
    names = [n.strip() for n in names_input.split(",") if n.strip()]

    if len(names) != 4:
        st.error("This version requires exactly 4 people.")
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
