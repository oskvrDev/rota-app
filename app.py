import streamlit as st
from datetime import timedelta
import pandas as pd


def generate_monthly_rota(names, start_date, months):
    rota = []
    current_date = start_date
    n = len(names)

    for month in range(months):

        # rotate primaries monthly
        primaries = names[month % n:] + names[:month % n]

        # secondary rotation
        if n >= 2:
            secondaries = [primaries[-1]] + primaries[:-1]
        else:
            secondaries = primaries[:]

        for week in range(4):
            primary = primaries[week % n]
            secondary = secondaries[week % n]

            # avoid same person where possible
            if n > 1 and primary == secondary:
                secondary = names[(names.index(primary) + 1) % n]

            rota.append({
                "Week (On-call Night)": current_date.strftime("%Y-%m-%d"),
                "Primary": primary,
                "Secondary": secondary
            })

            # move to next week (7 days later)
            current_date += timedelta(days=7)

    return pd.DataFrame(rota)


# UI
st.title("📅 Out-of-Hours Weekly Rota")

st.write("Each entry represents the **on-call night starting Sunday → Monday morning**.")

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

        file_name = "out_of_hours_rota.xlsx"
        df.to_excel(file_name, index=False)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Download Excel",
                f,
                file_name=file_name
            )
