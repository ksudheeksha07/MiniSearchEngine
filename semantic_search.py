from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# DOCUMENT FOLDER
# -------------------------------

documents_folder = (
    Path(__file__).resolve().parent / "documents"
)


# -------------------------------
# LOAD EMBEDDING MODEL
# -------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -------------------------------
# LOAD DOCUMENTS
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
# CREATE DOCUMENT EMBEDDINGS
# -------------------------------

document_embeddings = model.encode(
    documents,
    convert_to_numpy=True
)


# -------------------------------
# SEMANTIC SEARCH
# -------------------------------

def semantic_search(query, limit=5):

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