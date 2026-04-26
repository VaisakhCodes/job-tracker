from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
from nlp.extractor import extract_keywords


def calculate_fit_score(jd_text: str, resume_text: str) -> Dict:
    """
    Compare job description against resume using TF-IDF cosine similarity.
    Returns a fit score (0-100) and keyword analysis.
    """
    if not jd_text or not resume_text:
        return {"fit_score": 0, "matched": [], "missing": []}

    # TF-IDF vectorise both texts
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),   # captures both single words and pairs like "machine learning"
        max_features=1000
    )

    try:
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        fit_score = round(float(similarity) * 100, 1)
    except Exception:
        fit_score = 0.0

    # Keyword gap analysis
    jd_keywords = set(extract_keywords(jd_text))
    resume_keywords = set(extract_keywords(resume_text))

    matched = sorted(list(jd_keywords & resume_keywords))
    missing = sorted(list(jd_keywords - resume_keywords))

    return {
        "fit_score": fit_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "extracted_skills": sorted(list(jd_keywords)),
        "match_count": len(matched),
        "total_jd_keywords": len(jd_keywords)
    }