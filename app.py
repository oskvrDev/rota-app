import streamlit as st
from datetime import datetime, timedelta
import pandas as pd


# -----------------------------
# ROTATION LOGIC
# -----------------------------
def generate_monthly_rota(names, start_date, months):
    rota = []
    n = len(names)

    current_date = datetime.combine(start_date, datetime.min.time())

    for month in range(months):

        primaries = names[month % n:] + names[:month % n]

        if n >= 2:
            secondaries = [primaries[-1]] + primaries[:-1]
        else:
            secondaries = primaries[:]

        for week in range(4):
            primary = primaries[week % n]
            secondary = secondaries[week % n]

            if n > 1 and primary == secondary:
                secondary = names[(names.index(primary) + 1) % n]

            week_start = current_date
            week_end = current_date + timedelta(days=7)

            rota.append({
                "Week Start": week_start.strftime("%Y-%m-%d"),
                "Week End": week_end.strftime("%Y-%m-%d"),
                "Primary": primary,
                "Secondary": secondary
            })

            current_date += timedelta(days=7)

    return pd.DataFrame(rota)


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("📅 Out-of-Hours Rota Generator")

names_input = st.text_input(
    "Enter names (1–4 people), comma separated",
    placeholder="Adam, Michael P, Michael M, Oskar"
)

start_date = st.date_input("Week beginning date")
months = st.number_input("Number of months", min_value=1, value=1)


# -----------------------------
# EXCEL EXPORT (STYLED)
# -----------------------------
def export_excel(df, file_name="out_of_hours_rota.xlsx"):

    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Rota")

        workbook = writer.book
        worksheet = writer.sheets["Rota"]

        # -----------------------------
        # FORMATS (your colour scheme)
        # -----------------------------
        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#F4B183",   # peach header
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        })

        cell_format = workbook.add_format({
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        })

        alt_row_format = workbook.add_format({
            "bg_color": "#D9E1F2",   # light blue stripe
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        })

        # -----------------------------
        # HEADER FORMAT
        # -----------------------------
        for col_num, value in enumerate(df.columns):
            worksheet.write(0, col_num, value, header_format)

        # -----------------------------
        # COLUMN WIDTHS
        # -----------------------------
        worksheet.set_column("A:B", 18)
        worksheet.set_column("C:D", 20)

        # -----------------------------
        # STRIPED ROWS
        # -----------------------------
        for row in range(len(df)):
            fmt = alt_row_format if row % 2 == 0 else cell_format

            for col in range(len(df.columns)):
                worksheet.write(row + 1, col, df.iloc[row, col], fmt)

        worksheet.freeze_panes(1, 0)

    return file_name


# -----------------------------
# BUTTON ACTION
# -----------------------------
if st.button("Generate Rota"):
    names = [n.strip() for n in names_input.split(",") if n.strip()]

    if len(names) == 0:
        st.error("Please enter at least one name.")
    elif len(names) > 4:
        st.error("This version supports up to 4 people.")
    else:
        df = generate_monthly_rota(names, start_date, months)

        st.dataframe(df)

        file_path = export_excel(df)

        with open(file_path, "rb") as f:
            st.download_button(
                "📥 Download Excel",
                f,
                file_name="out_of_hours_rota.xlsx"
            )
