import streamlit as st
import subprocess
import time

from db import (
    create_table,
    check_user,
    add_default_user,
    get_all_results,
    get_results,
    save_result
)

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Code Plagiarism Detection Tool", layout="centered")

# ---------- DB SETUP ----------
create_table()
add_default_user()

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- LOGIN ----------
if not st.session_state.logged_in:

    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = check_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[0]
            st.session_state.role = user[2]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Page", "Dashboard"])

# ==================================================
# ================= UPLOAD PAGE ====================
# ==================================================
if page == "Upload Page" and st.session_state.role == "Student":

    st.title("Code Plagiarism Detection Tool")
    st.write(f"Logged in as: {st.session_state.role}")

    file1 = st.file_uploader("Upload Code File 1 (.py)", type=["py"], key="u1")
    file2 = st.file_uploader("Upload Code File 2 (.py)", type=["py"], key="u2")

    if st.button("Check Plagiarism"):

        if file1 and file2:

            with open("data/code1.py", "wb") as f:
                f.write(file1.read())

            with open("data/code2.py", "wb") as f:
                f.write(file2.read())

            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            result = subprocess.check_output(
                ["python", "final_score.py"],
                universal_newlines=True
            )

            st.subheader("Raw Output")
            st.text(result)

            # ---------- PARSE ----------
            lexical = structural = semantic = final_score = 0.0

            for line in result.splitlines():
                if line.startswith("Lexical Score"):
                    lexical = float(line.split(":")[1])
                elif line.startswith("Structural Score"):
                    structural = float(line.split(":")[1])
                elif line.startswith("Semantic Score"):
                    semantic = float(line.split(":")[1])
                elif line.startswith("Final Plagiarism Score"):
                    final_score = float(line.split(":")[1])

            percent = int(final_score * 100)

            # ---------- DISPLAY ----------
            st.subheader("Similarity Scores")

            c1, c2, c3 = st.columns(3)
            c1.metric("Lexical", f"{int(lexical * 100)}%")
            c2.metric("Structural", f"{int(structural * 100)}%")
            c3.metric("Semantic", f"{int(semantic * 100)}%")

            st.metric("Overall Plagiarism", f"{percent}%")
            st.progress(final_score)

            # ---------- VERDICT ----------
            if percent < 30:
                verdict = "Low"
                st.success("Low Plagiarism 🟢")
            elif percent < 60:
                verdict = "Medium"
                st.warning("Medium Plagiarism 🟡")
            else:
                verdict = "High"
                st.error("High Plagiarism 🔴")

            # ---------- SAVE ----------
            save_result(
                st.session_state.username,
                file1.name,
                file2.name,
                percent,
                verdict
            )

        else:
            st.warning("Please upload both files.")

# ==================================================
# ================= DASHBOARD =======================
# ==================================================
elif page == "Dashboard":

    # ---------- FACULTY ----------
    if st.session_state.role == "Faculty":

        st.title("📊 Faculty Dashboard")

        # ✅ Upload for faculty also
        st.subheader("Upload Code")

        f1 = st.file_uploader("Upload File 1", type=["py"], key="f1")
        f2 = st.file_uploader("Upload File 2", type=["py"], key="f2")

        if st.button("Check Plagiarism (Faculty)"):
            if f1 and f2:

                with open("data/code1.py", "wb") as f:
                    f.write(f1.read())

                with open("data/code2.py", "wb") as f:
                    f.write(f2.read())

                result = subprocess.check_output(
                    ["python", "final_score.py"],
                    universal_newlines=True
                )

                st.text(result)
            else:
                st.warning("Upload both files")

        # ---------- RESULTS ----------
        results = get_all_results()

        if results:
            st.metric("Total Reports", len(results))

            for row in results:
                st.markdown("---")
                st.write(f"👤 User: {row[1]}")
                st.write(f"📄 File1: {row[2]}")
                st.write(f"📄 File2: {row[3]}")
                st.write(f"📊 Score: {row[4]}%")
                st.write(f"⚠️ Verdict: {row[5]}")
        else:
            st.warning("No results yet")

    # ---------- STUDENT ----------
    else:
        st.title("📊 Your Dashboard")

        results = get_results(st.session_state.username)

        if results:
            for row in results:
                st.markdown("---")
                st.write(f"📄 File1: {row[2]}")
                st.write(f"📄 File2: {row[3]}")
                st.write(f"📊 Score: {row[4]}%")
                st.write(f"⚠️ Verdict: {row[5]}")
        else:
            st.info("No results yet")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Code Plagiarism Detection Tool | B.Tech Final Year Project")