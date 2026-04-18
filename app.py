import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from final_score import calculate_score
from database import create_table, login_user, add_user

# -------- INIT --------
create_table()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -------- LOGIN PAGE --------
def login():
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        result = login_user(user, pwd)

        if result:
            st.session_state.logged_in = True
            st.session_state["username"] = user
            st.session_state["role"] = result[0]   # 🔥 IMPORTANT
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")


# -------- MAIN APP --------
def main_app():
    role = st.session_state.get("role")

    page = st.sidebar.radio("Navigation", ["Checker", "Dashboard", "Admin Panel"])

    # HEADER
    col1, col2 = st.columns([8, 2])

    with col1:
        st.title("💡 Code Plagiarism Detection Tool")

    with col2:
        if st.button("Logout 🔓"):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()

    # ================= CHECKER =================
    if page == "Checker":

        file1 = st.file_uploader("Upload File 1", type=["py", "c", "cpp", "java"])
        file2 = st.file_uploader("Upload File 2", type=["py", "c", "cpp", "java"])

        if st.button("Check Plagiarism"):

            if file1 and file2:
                code1 = file1.read().decode()
                code2 = file2.read().decode()

                lex, ngram, sem, final = calculate_score(code1, code2)

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

                # RESULTS
                st.subheader("Results")

                c1, c2, c3 = st.columns(3)
                c1.metric("Lexical", f"{int(lex*100)}%")
                c2.metric("N-Gram", f"{int(ngram*100)}%")
                c3.metric("Semantic", f"{int(sem*100)}%")

                st.metric("Final Score", f"{int(final*100)}%")
                st.progress(final)

                # GRAPH
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=["Lexical", "N-Gram", "Semantic", "Final"],
                    y=[lex, ngram, sem, final]
                ))

                st.plotly_chart(fig)

                # VERDICT
                if final < 0.3:
                    st.success("Low Plagiarism")
                elif final < 0.6:
                    st.warning("Medium Plagiarism")
                else:
                    st.error("High Plagiarism")

            else:
                st.warning("Upload both files")

    # ================= DASHBOARD =================
    elif page == "Dashboard":

        st.title("Dashboard")

        import sqlite3
        conn = sqlite3.connect("plagiarism_new.db")

        df = pd.read_sql_query("SELECT * FROM results", conn)

        if df.empty:
            st.warning("No data yet")
        else:
            st.metric("Total Checks", len(df))
            st.metric("Average Score", f"{df['final'].mean():.2f}")

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=["Low", "Medium", "High"],
                y=[
                    len(df[df["final"] <= 0.3]),
                    len(df[(df["final"] > 0.3) & (df["final"] <= 0.6)]),
                    len(df[df["final"] > 0.6])
                ]
            ))

            st.plotly_chart(fig)
            st.dataframe(df.tail(10))

        conn.close()

    # ================= ADMIN PANEL =================
    elif page == "Admin Panel":

        if role != "admin":
            st.error("Access Denied")
            return

        st.title("Admin Panel")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Create Student"):
            if new_user and new_pass:
                success = add_user(new_user, new_pass, "student")

                if success:
                    st.success("Student Created")
                else:
                    st.error("User already exists")
            else:
                st.warning("Fill all fields")


# -------- ROUTING --------
if not st.session_state.logged_in:
    login()
else:
    main_app()