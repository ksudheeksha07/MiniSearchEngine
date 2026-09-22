import json
import sys
from pathlib import Path

# Allow Python to import files from the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import search_engine
import hybrid_search


# ---------------------------------------
# LOAD EVALUATION DATASET
# ---------------------------------------

evaluation_file = (
    Path(__file__).resolve().parent
    / "queries.json"
)

with open(
    evaluation_file,
    "r",
    encoding="utf-8"
) as file:

    evaluation_data = json.load(file)


# ---------------------------------------
# PRECISION@5
# ---------------------------------------

def precision_at_k(
    retrieved_documents,
    relevant_documents,
    k=5
):

    retrieved = retrieved_documents[:k]

    if not retrieved:
        return 0.0

    relevant_count = sum(
        1
        for document in retrieved
        if document in relevant_documents
    )

    return relevant_count / len(retrieved)


# ---------------------------------------
# RECALL@5
# ---------------------------------------

def recall_at_k(
    retrieved_documents,
    relevant_documents,
    k=5
):

    if not relevant_documents:
        return 0.0

    retrieved = retrieved_documents[:k]

    relevant_count = sum(
        1
        for document in retrieved
        if document in relevant_documents
    )

    return relevant_count / len(
        relevant_documents
    )


# ---------------------------------------
# F1@5
# ---------------------------------------

def f1_score(
    precision,
    recall
):

    if precision + recall == 0:
        return 0.0

    return (
        2
        * precision
        * recall
        / (precision + recall)
    )


# ---------------------------------------
# TEST ONE WEIGHT CONFIGURATION
# ---------------------------------------

def evaluate_weights(
    keyword_weight,
    semantic_weight
):

    precision_scores = []
    recall_scores = []
    f1_scores = []

    for item in evaluation_data:

        query = item["query"]

        relevant_documents = set(
            item["relevant_documents"]
        )

        results = hybrid_search.hybrid_search(
            query,
            keyword_weight=keyword_weight,
            semantic_weight=semantic_weight,
            limit=5
        )

        retrieved_documents = [
            result["filename"]
            for result in results
        ]

        precision = precision_at_k(
            retrieved_documents,
            relevant_documents
        )

        recall = recall_at_k(
            retrieved_documents,
            relevant_documents
        )

        f1 = f1_score(
            precision,
            recall
        )

        precision_scores.append(
            precision
        )

        recall_scores.append(
            recall
        )

        f1_scores.append(
            f1
        )

    return {
        "precision@5":
            sum(precision_scores)
            / len(precision_scores),

        "recall@5":
            sum(recall_scores)
            / len(recall_scores),

        "f1@5":
            sum(f1_scores)
            / len(f1_scores)
    }


# ---------------------------------------
# MAIN
# ---------------------------------------

if __name__ == "__main__":

    weight_configurations = [
        (0.7, 0.3),
        (0.5, 0.5),
        (0.3, 0.7)
    ]

    print()
    print("=" * 75)
    print("HYBRID SEARCH WEIGHT EXPERIMENT")
    print("=" * 75)

    print()
    print(
        f"Evaluation queries: "
        f"{len(evaluation_data)}"
    )

    print(
        f"Documents available: "
        f"{len(search_engine.document_files)}"
    )

    print()
    print(
        "Testing keyword/semantic weight combinations..."
    )

    print()
    print(
        "Weights        Precision@5   "
        "Recall@5   F1@5"
    )

    print("-" * 55)

    for keyword_weight, semantic_weight in (
        weight_configurations
    ):

        metrics = evaluate_weights(
            keyword_weight,
            semantic_weight
        )

        print(
            f"{keyword_weight:.1f} / "
            f"{semantic_weight:.1f}"
            f"{'':<10}"
            f"{metrics['precision@5']:<14.3f}"
            f"{metrics['recall@5']:<11.3f}"
            f"{metrics['f1@5']:.3f}"
        )

    print()
    print("=" * 75)
    print("EXPERIMENT COMPLETE")
    print("=" * 75)