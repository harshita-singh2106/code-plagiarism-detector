# final_score.py

lexical_score = 0.6
structural_score = 1.0
semantic_score = 0.33

lexical_reason = "Most keywords and identifiers are similar."
structural_reason = "Both programs share the same structural pattern (AST)."
semantic_reason = "Both programs use similar control flow and logic."

final_score = (
    0.3 * lexical_score +
    0.4 * structural_score +
    0.3 * semantic_score
)

print("Lexical Score:", lexical_score)
print("Lexical Reason:", lexical_reason)

print("Structural Score:", structural_score)
print("Structural Reason:", structural_reason)

print("Semantic Score:", semantic_score)
print("Semantic Reason:", semantic_reason)

print("Final Plagiarism Score:", round(final_score, 2))
