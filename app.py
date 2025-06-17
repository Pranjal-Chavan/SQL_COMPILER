import streamlit as st
import sqlite3
import pandas as pd
import uuid
import os

# 🌟 Create a unique DB path for each user session
if "db_path" not in st.session_state:
    unique_id = str(uuid.uuid4())[:8]
    st.session_state.db_path = f"userdb_{unique_id}.db"

DB_PATH = st.session_state.db_path

st.set_page_config(page_title="Mini SQL Compiler", layout="centered")
st.title("🧠 Mini SQL Compiler")

query = st.text_area("Enter your SQL query below:", height=200)

if st.button("Run Query"):
    if query.strip() == "":
        st.warning("⚠️ Please enter a SQL query.")
    else:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()

                # Execute multiple SQL statements safely
                cursor.executescript(query)

                # Look for last SELECT statement to display result
                selects = [stmt.strip() for stmt in query.split(';') if stmt.strip().lower().startswith("select")]

                if selects:
                    last_select = selects[-1]
                    df = pd.read_sql_query(last_select, conn)

                    st.success("✅ Query executed successfully.")
                    st.dataframe(df)

                    # Download button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("⬇️ Download CSV", csv, "results.csv", "text/csv")

                else:
                    st.success("✅ Query executed (no SELECT result to display).")

        except Exception as e:
            st.error(f"❌ Error: {e}")
