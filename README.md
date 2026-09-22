# 🔎 Mini Search Engine

A lightweight search engine built with **Python and Flask** that searches across a collection of local documents using **TF-IDF, semantic search, and hybrid ranking**.

The project combines traditional information retrieval with semantic similarity to provide both exact keyword matching and meaning-based document retrieval through a clean web interface.

---

## ✨ Features

### 🔎 Keyword Search

Uses **TF-IDF-based ranking** to find documents containing terms related to the user's query.

* Term Frequency (TF)
* Inverse Document Frequency (IDF)
* TF-IDF scoring
* Normalized term frequency
* Query normalization
* Punctuation handling
* Relevant text snippets

### 🧠 Semantic Search

Uses **Sentence Transformers** to convert the query and documents into semantic embeddings.

The system then uses **cosine similarity** to measure how closely each document matches the meaning of the query.

This allows the search engine to retrieve conceptually related documents even when the exact query words are not present.

The semantic search pipeline uses:

- Sentence Transformers for embeddings
- scikit-learn for cosine similarity
- PyTorch as the underlying deep-learning framework

### 🔀 Hybrid Search

Combines:

* Keyword relevance
* Semantic similarity

to produce a combined ranking of documents.

### ✍️ Spelling Correction

The search engine can detect possible spelling mistakes and provide alternative queries.

Example:

```text
macine → machine
```

### 💡 Live Search Suggestions

Suggestions are generated while the user types using the indexed vocabulary.

### 🕘 Search History

The web application keeps track of previous searches and allows users to:

* Re-run previous searches
* Clear search history

### 📊 Search Statistics

Each search displays:

* Search time
* Number of documents searched
* Number of query terms

### 📱 Responsive Interface

The Flask interface is designed to work across desktop and smaller screen sizes.

---

| Technology | Purpose |
|---|---|
| Python | Core programming and search algorithms |
| Flask | Web application |
| HTML | Page structure |
| CSS | User interface |
| JavaScript | Live search suggestions |
| TF-IDF | Keyword-based information retrieval |
| Sentence Transformers | Semantic embeddings |
| scikit-learn | Cosine similarity |
| PyTorch | Deep-learning backend |
| JSON | Evaluation query data |

## 🧠 How It Works

The search engine follows a multi-stage retrieval process.

```text
                User Query
                    │
                    ▼
             Query Processing
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   Keyword Search       Semantic Search
      (TF-IDF)          (Similarity)
          │                   │
          └─────────┬─────────┘
                    ▼
              Hybrid Search
                    │
                    ▼
            Ranked Documents
                    │
                    ▼
              Web Interface
```

### 1. Document Collection

The search engine loads text files from the `documents/` directory.

The current dataset contains **15 documents** covering topics such as:

* Artificial Intelligence
* Algorithms
* Computer Vision
* Cybersecurity
* Databases
* Data Structures
* Deep Learning
* Generative AI
* IoT
* Networking
* NLP
* Operating Systems
* Programming
* Python
* Robotics

### 2. Text Processing

Documents and queries are processed before searching.

The processing includes:

* Converting text into normalized terms
* Removing punctuation
* Normalizing related word forms
* Preparing terms for indexing and retrieval

### 3. Keyword Retrieval

The keyword search uses TF-IDF to determine how relevant a document is to a query.

A higher TF-IDF score indicates stronger keyword relevance.

### 4. Semantic Retrieval

Semantic search looks beyond exact word matching and retrieves documents based on conceptual similarity.

This allows related documents to appear even when the exact query terms are not strongly represented.

### 5. Hybrid Ranking

Hybrid search combines keyword and semantic signals to provide a more comprehensive ranking.

This allows the system to benefit from both:

**Exact matching + Meaning-based matching**

---

## 📂 Project Structure

```text
MiniSearchEngine/
│
├── app.py
├── hybrid_search.py
├── index.py
├── main.py
├── search_engine.py
├── semantic_search.py
│
├── documents/
│   ├── ai.txt
│   ├── algorithms.txt
│   ├── computer_vision.txt
│   ├── cybersecurity.txt
│   ├── database.txt
│   ├── data_structures.txt
│   ├── deep_learning.txt
│   ├── generative_ai.txt
│   ├── iot.txt
│   ├── networking.txt
│   ├── nlp.txt
│   ├── operating_system.txt
│   ├── programming.txt
│   ├── python.txt
│   └── robotics.txt
│
├── evaluation/
│   ├── evaluate.py
│   └── queries.json
│
├── tests/
│   └── test_search.py
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
└── .vscode/
    └── settings.json
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd MiniSearchEngine
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

### Windows

```powershell
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install flask
```

If additional dependencies are used by the semantic-search implementation, install them according to the project's environment requirements.

---

## ▶️ Running the Application

Start the Flask application with:

```bash
python app.py
```

The application will start locally.

Open the local Flask address shown in the terminal in your browser.

---

## 🔍 Example Queries

Try searches such as:

```text
python
machine learning
computer vision
database
robotics
artificial intelligence
```

You can also test spelling correction:

```text
macine
```

The system can suggest:

```text
machine
```

---

## 🧪 Testing

The project includes automated tests in the `tests/` directory.

Run:

```bash
python -m pytest
```

The `evaluation/` directory also contains:

```text
evaluate.py
queries.json
```

which can be used to evaluate search behaviour against predefined queries.

---

## 📈 Evaluation

The project evaluates search behaviour across different query types, including:

* Exact keyword queries
* Multi-word queries
* Spelling errors
* Queries with no direct keyword matches
* Semantically related queries

This helps compare how traditional keyword retrieval and semantic retrieval behave under different search conditions.

---

## 🎯 Project Goals

The main goals of this project are to understand and implement fundamental concepts in information retrieval and modern search systems.

Key concepts explored include:

* Text preprocessing
* Inverted indexing
* TF-IDF
* Document ranking
* Semantic similarity
* Hybrid retrieval
* Search suggestions
* Spelling correction
* Search evaluation
* Flask-based application development

---

## 🔮 Future Improvements

Possible future improvements include:

* Persistent search history
* Improved ranking algorithms
* Larger document collections
* Better semantic embeddings
* Advanced query understanding
* Search filters
* Document upload functionality
* Performance optimization
* Cloud deployment
* Improved evaluation metrics

---

## 📌 Current Status

**Project status: Completed core implementation**

The current version includes:

* ✅ Keyword search
* ✅ TF-IDF ranking
* ✅ Semantic search
* ✅ Hybrid search
* ✅ Spelling correction
* ✅ Live suggestions
* ✅ Search history
* ✅ Search statistics
* ✅ Responsive web interface
* ✅ Automated tests
* ✅ Search evaluation framework

---

## 👩‍💻 Author

**Sudheeksha**

CSE — Artificial Intelligence & Machine Learning

---

## 📄 License

This project is intended for educational and portfolio purposes.
