import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from normalize import normalize_code    
from final_score import calculate_score
from database import login_user
# -------- SESSION INIT --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------- LOGIN PAGE --------
def login():
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(user, pwd):
            st.session_state.logged_in = True
            st.session_state["username"] = user  # important
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")
def main_app():
    #st.write("App Loaded")
    page = st.sidebar.radio("Navigation", ["Checker", "Dashboard"])
    #st.write("Login page visible")

    # ---- HEADER ----
    col1, col2 = st.columns([8, 2])

    with col1:
        st.title("💡 Code Plagiarism Detection Tool")
        st.caption("Supports Python, C, C++, Java")

    with col2:
        if st.button("Logout 🔓"):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()

    # ================= CHECKER =================
    if page == "Checker":

        file1 = st.file_uploader("📂 Upload File 1", type=["py", "c", "cpp", "java"])
        file2 = st.file_uploader("📂 Upload File 2", type=["py", "c", "cpp", "java"])

        if st.button("🚀 Check Plagiarism"):

            if file1 and file2:
                try:
                    code1 = file1.read().decode()
                    code2 = file2.read().decode()

                    # ---- CALCULATE ----
                    lex, ngram, sem, final = calculate_score(code1, code2)

                    # ---- SAVE TO DB ----
                    import sqlite3
                    conn = sqlite3.connect("plagiarism_new.db")
                    c = conn.cursor()

                    c.execute("""
                    CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lexical REAL,
                        ngram REAL,
                        semantic REAL,
                        final REAL
                    )
                    """)

                    c.execute(
                        "INSERT INTO results (lexical, ngram, semantic, final) VALUES (?, ?, ?, ?)",
                        (lex, ngram, sem, final)
                    )

                    conn.commit()
                    conn.close()

                    # ---- RESULTS ----
                    st.subheader("📊 Results")

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Lexical", f"{int(lex * 100)}%")
                    c2.metric("N-Gram", f"{int(ngram * 100)}%")
                    c3.metric("Semantic", f"{int(sem * 100)}%")

                    st.metric("🔥 Final Score", f"{int(final * 100)}%")
                    st.progress(final)

                    # ---- GRAPH ----
                    st.subheader("📊 Similarity Breakdown")

                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=["Lexical", "N-Gram", "Semantic", "Final"],
                        y=[lex, ngram, sem, final],
                        marker_color=["#60a5fa", "#2563eb", "#f87171", "#facc15"]
                    ))

                    fig.update_layout(
                        template="plotly_dark",
                        title="Similarity Breakdown"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.divider()

                    # ---- VERDICT ----
                    if final < 0.3:
                        st.success("✅ Low Plagiarism")
                    elif final < 0.6:
                        st.warning("⚠️ Medium Plagiarism")
                    else:
                        st.error("🚨 High Plagiarism")

                except Exception as e:
                    st.error(f"Error: {e}")

            else:
                st.warning("⚠️ Please upload both files")

    # ================= DASHBOARD =================
    elif page == "Dashboard":

        st.title("📊 Dashboard")

        import sqlite3
        import pandas as pd

        conn = sqlite3.connect("plagiarism_new.db")
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lexical REAL,
            ngram REAL,
            semantic REAL,
            final REAL
        )
        """)

        conn.commit()
        df = pd.read_sql_query("SELECT * FROM results", conn)

        if df.empty:
            st.warning("No data yet. Run some checks first.")
        else:
            total = len(df)
            avg = df["final"].mean()

            high = len(df[df["final"] > 0.6])
            medium = len(df[(df["final"] > 0.3) & (df["final"] <= 0.6)])
            low = len(df[df["final"] <= 0.3])

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Checks", total)
            col2.metric("Avg Score", f"{avg:.2f}")
            col3.metric("High 🚨", high)
            col4.metric("Low ✅", low)

            st.divider()

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=["Low", "Medium", "High"],
                y=[low, medium, high],
                marker_color=["#22c55e", "#facc15", "#ef4444"]
            ))

            fig.update_layout(
                template="plotly_dark",
                title="Plagiarism Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.divider()

            st.subheader("Recent Checks")
            st.dataframe(df.tail(10))

        conn.close()
if not st.session_state.get("logged_in", False):
    login()
else:
    main_app()       