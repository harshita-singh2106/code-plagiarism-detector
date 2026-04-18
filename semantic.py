import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------- NORMALIZATION --------
def normalize_code(code):
    # remove comments
    code = re.sub(r'//.*|/\*[\s\S]*?\*/|#.*', '', code)

    # remove extra spaces
    code = re.sub(r'\s+', ' ', code)

    return code.strip()


# -------- LEXICAL SIMILARITY --------
def lexical_similarity(code1, code2):
    tokens1 = code1.split()
    tokens2 = code2.split()

    set1 = set(tokens1)
    set2 = set(tokens2)

    if not set1 or not set2:
        return 0

    return len(set1 & set2) / len(set1 | set2)


# -------- N-GRAM SIMILARITY --------
def ngram_similarity(code1, code2, n=3):
    def get_ngrams(tokens, n):
        return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

    tokens1 = code1.split()
    tokens2 = code2.split()

    ngrams1 = set(get_ngrams(tokens1, n))
    ngrams2 = set(get_ngrams(tokens2, n))

    if not ngrams1 or not ngrams2:
        return 0

    return len(ngrams1 & ngrams2) / len(ngrams1 | ngrams2)


# -------- SEMANTIC SIMILARITY (TF-IDF) --------
def semantic_similarity(code1, code2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([code1, code2])

    sim = cosine_similarity(vectors[0], vectors[1])[0][0]
    return sim


# -------- FINAL SCORE --------
def calculate_score(code1, code2):
    code1 = normalize_code(code1)
    code2 = normalize_code(code2)

    lex = lexical_similarity(code1, code2)
    ngram = ngram_similarity(code1, code2)
    sem = semantic_similarity(code1, code2)

    # weighted score
    final = (0.3 * lex) + (0.3 * ngram) + (0.4 * sem)

    return lex, ngram, sem, final