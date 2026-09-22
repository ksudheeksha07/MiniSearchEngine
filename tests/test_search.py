import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from search_engine import find_documents


# -------------------------------
# TEST 1: BASIC SEARCH
# -------------------------------

def test_basic_search():

    query = "python"

    expected_documents = {
        "python.txt",
        "programming.txt"
    }

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# TEST 2: NO RESULTS
# -------------------------------

def test_no_results():

    query = "quantum"

    expected_documents = set()

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# TEST 3: DATABASE SEARCH
# -------------------------------

def test_database_search():

    query = "database"

    expected_documents = {
        "database.txt"
    }

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# TEST 4: CYBERSECURITY SEARCH
# -------------------------------

def test_cybersecurity_search():

    query = "cybersecurity"

    expected_documents = {
        "cybersecurity.txt"
    }

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# TEST 5: OPERATING SYSTEM SEARCH
# -------------------------------

def test_operating_system_search():

    query = "operating system"

    expected_documents = {
        "operating_system.txt"
    }

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# TEST 6: CASE-INSENSITIVE SEARCH
# -------------------------------

def test_case_insensitive_search():

    query = "PYTHON"

    expected_documents = {
        "python.txt",
        "programming.txt"
    }

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# TEST 7: PUNCTUATION SEARCH
# -------------------------------

def test_punctuation_search():

    query = "python!!!"

    expected_documents = {
        "python.txt",
        "programming.txt"
    }

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# TEST 8: WORD NORMALIZATION
# -------------------------------

def test_word_normalization():

    query = "connection"

    expected_documents = {
        "networking.txt"
    }

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# TEST 9: MULTI-WORD SEARCH
# -------------------------------

def test_multi_word_search():

    query = "machine learning"

    expected_documents = {
        "python.txt",
        "ai.txt"
    }

    actual_documents = find_documents(query)

    print("Testing:", query)
    print("Expected:", expected_documents)
    print("Actual:", actual_documents)

    assert actual_documents == expected_documents

    print("PASS")


# -------------------------------
# RUN ALL TESTS
# -------------------------------

test_basic_search()
test_no_results()
test_database_search()
test_cybersecurity_search()
test_operating_system_search()
test_case_insensitive_search()
test_punctuation_search()
test_word_normalization()
test_multi_word_search()