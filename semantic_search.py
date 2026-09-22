from pathlib import Path
import os

from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# DOCUMENT FOLDER
# -------------------------------

documents_folder = (
    Path(__file__).resolve().parent / "documents"
)


# -------------------------------
# DOCUMENT LIST
# -------------------------------

document_files = [
    file_path.name
    for file_path in documents_folder.glob("*.txt")
]

documents = []
document_names = []


for filename in document_files:

    file_path = documents_folder / filename

    content = file_path.read_text(
        encoding="utf-8"
    )

    documents.append(content)
    document_names.append(filename)


# -------------------------------
# SEMANTIC SEARCH CONFIGURATION
# -------------------------------

# Semantic search is enabled locally.
# On Render, set ENABLE_SEMANTIC_SEARCH=false
# to prevent the large ML model from loading.

ENABLE_SEMANTIC_SEARCH = (
    os.environ.get(
        "ENABLE_SEMANTIC_SEARCH",
        "true"
    ).lower()
    == "true"
)


model = None
document_embeddings = None


# -------------------------------
# LOAD MODEL ONLY WHEN NEEDED
# -------------------------------

def load_model():

    global model
    global document_embeddings

    if model is not None:
        return

    if not ENABLE_SEMANTIC_SEARCH:
        return

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    document_embeddings = model.encode(
        documents,
        convert_to_numpy=True
    )


# -------------------------------
# SEMANTIC SEARCH
# -------------------------------

def semantic_search(query, limit=5):

    load_model()

    if not ENABLE_SEMANTIC_SEARCH:
        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    similarities = cosine_similarity(
        query_embedding,
        document_embeddings
    )[0]

    ranked_indices = similarities.argsort()[::-1]

    results = []

    for index in ranked_indices[:limit]:

        results.append({
            "filename": document_names[index],
            "similarity": round(
                float(similarities[index]),
                3
            )
        })

    return results


# -------------------------------
# TEST
# -------------------------------

if __name__ == "__main__":

    results = semantic_search(
        "machines that learn from examples"
    )

    for result in results:

        print(
            result["filename"],
            result["similarity"]
        )