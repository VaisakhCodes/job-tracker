import spacy
from typing import List, Dict

# Load once at module level — not on every request
nlp = spacy.load("en_core_web_sm")

# Tech skills that matter to hiring managers
TECH_KEYWORDS = {
    # Languages
    "python", "javascript", "java", "typescript", "go", "rust", "c++", "c#",
    "ruby", "php", "swift", "kotlin", "scala", "r",
    # Frameworks
    "django", "flask", "fastapi", "react", "vue", "angular", "spring",
    "express", "nextjs", "nuxt", "rails",
    # Databases
    "mysql", "postgresql", "mongodb", "redis", "sqlite", "elasticsearch",
    "dynamodb", "cassandra",
    # DevOps & Cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "jenkins",
    "git", "github", "gitlab", "ci/cd", "linux",
    # ML & Data
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "nlp", "machine learning", "deep learning", "llm", "langchain",
    # Concepts
    "rest", "api", "graphql", "microservices", "agile", "scrum",
    "sql", "nosql", "oop", "tdd", "mvc",
}

def extract_keywords(text: str) -> List[str]:
    """Extract tech keywords from a job description using spaCy + keyword matching."""
    doc = nlp(text.lower())
    found = set()

    # Method 1: Direct keyword match against our tech list
    for keyword in TECH_KEYWORDS:
        if keyword in text.lower():
            found.add(keyword)

    # Method 2: spaCy noun chunks — catches multi-word terms like "machine learning"
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower().strip()
        if chunk_text in TECH_KEYWORDS:
            found.add(chunk_text)

    # Method 3: Named entities — catches product names, technologies
    for ent in doc.ents:
        if ent.label_ in ("ORG", "PRODUCT") and ent.text.lower() in TECH_KEYWORDS:
            found.add(ent.text.lower())

    return sorted(list(found))


def extract_requirements(text: str) -> Dict:
    """Extract structured requirements from a job description."""
    doc = nlp(text.lower())
    keywords = extract_keywords(text)

    # Look for experience requirements
    experience_years = None
    for token in doc:
        if token.like_num and token.nbor(1).text in ("year", "years"):
            try:
                experience_years = int(token.text)
            except ValueError:
                pass

    # Detect seniority level
    level = "junior"
    text_lower = text.lower()
    if any(w in text_lower for w in ["senior", "sr.", "lead", "principal", "staff"]):
        level = "senior"
    elif any(w in text_lower for w in ["mid", "intermediate", "2-4 years", "3-5 years"]):
        level = "mid"

    return {
        "keywords": keywords,
        "experience_years": experience_years,
        "level": level,
        "keyword_count": len(keywords)
    }