import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

def generate_weekly_rota(names, start_date, num_weeks):
    rota = []
    current_date = start_date

    for i in range(num_weeks):
        person = names[i % len(names)]
        week_end = current_date + timedelta(days=6)

        rota.append({
            "Week Start": current_date.strftime("%Y-%m-%d"),
            "Week End": week_end.strftime("%Y-%m-%d"),
            "Assigned Person": person
        })

        current_date += timedelta(days=7)

    return pd.DataFrame(rota)

st.title("📅 Weekly On-Call Rota Generator")

names_input = st.text_input("Enter names (comma separated)")
start_date = st.date_input("Week beginning date")
num_weeks = st.number_input("Number of weeks", min_value=1, value=4)

if st.button("Generate Rota"):
    names = [n.strip() for n in names_input.split(",") if n.strip()]
    
    if not names:
        st.error("Please enter at least one name")
    else:
        df = generate_weekly_rota(names, start_date, num_weeks)

        st.dataframe(df)

        # Excel download
        file_name = "rota.xlsx"
        df.to_excel(file_name, index=False)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Download Excel",
                f,
                file_name=file_name
            )
