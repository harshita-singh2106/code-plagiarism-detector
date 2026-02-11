import streamlit as st
import subprocess
import time

st.set_page_config(page_title="Code Plagiarism Detection Tool", layout="centered")

st.title("Code Plagiarism Detection Tool")
st.write(
    "Upload two Python files to check plagiarism using "
    "Lexical, Structural, and Semantic analysis."
)

# File upload
file1 = st.file_uploader("Upload Code File 1 (.py)", type=["py"])
file2 = st.file_uploader("Upload Code File 2 (.py)", type=["py"])

if st.button("Check Plagiarism"):
    if file1 and file2:
        # Save uploaded files
        with open("data/code1.py", "wb") as f:
            f.write(file1.read())

        with open("data/code2.py", "wb") as f:
            f.write(file2.read())

        # Progress bar
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        # Run backend
        result = subprocess.check_output(
            ["python", "final_score.py"],
            universal_newlines=True
        )

        st.subheader("Raw Output")
        st.text(result)

        # ---------- SAFE PARSING ----------
        lexical = structural = semantic = final_score = 0.0
        lexical_reason = structural_reason = semantic_reason = ""

        for line in result.splitlines():
            if line.startswith("Lexical Score"):
                lexical = float(line.split(":")[1])
            elif line.startswith("Lexical Reason"):
                lexical_reason = line.split(":", 1)[1]
            elif line.startswith("Structural Score"):
                structural = float(line.split(":")[1])
            elif line.startswith("Structural Reason"):
                structural_reason = line.split(":", 1)[1]
            elif line.startswith("Semantic Score"):
                semantic = float(line.split(":")[1])
            elif line.startswith("Semantic Reason"):
                semantic_reason = line.split(":", 1)[1]
            elif line.startswith("Final Plagiarism Score"):
                final_score = float(line.split(":")[1])

        percent = int(final_score * 100)

        # ---------- METRICS ----------
        st.subheader("Similarity Scores")
        c1, c2, c3 = st.columns(3)
        c1.metric("Lexical Similarity", f"{int(lexical * 100)}%")
        c2.metric("Structural Similarity", f"{int(structural * 100)}%")
        c3.metric("Semantic Similarity", f"{int(semantic * 100)}%")

        st.subheader("Final Plagiarism Percentage")
        st.metric("Overall Plagiarism", f"{percent}%")
        st.progress(final_score)

        # ---------- VERDICT ----------
        if percent < 30:
            st.success("Low Plagiarism 🟢")
            st.info("The programs are mostly original with minimal similarity.")
        elif percent < 60:
            st.warning("Medium Plagiarism 🟡")
            st.info("The programs share partial similarity in structure or logic.")
        else:
            st.error("High Plagiarism 🔴")
            st.info("The programs are highly similar and likely plagiarized.")

        # ---------- EXPLANATION ----------
        st.subheader("Explanation")
        st.write("🔹 **Lexical Analysis:**", lexical_reason)
        st.write("🔹 **Structural Analysis:**", structural_reason)
        st.write("🔹 **Semantic Analysis:**", semantic_reason)

        st.button("Check Another Pair")

    else:
        st.warning("Please upload both Python files.")

st.markdown("---")
st.caption("Code Plagiarism Detection Tool | B.Tech Final Year Project")
