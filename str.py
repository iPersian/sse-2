import time
import statistics
import re
import regex
from pyparsing import Word, alphas, OneOrMore, ParseException
import nltk
import spacy
import os
import csv

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nlp = spacy.load("en_core_web_sm")
RUNS = 1

text_sample = (
    "Measuring energy consumption in joules is the path to successful computing. "
    "All algorithms use power differently. "
    "The goal is to analyze, optimize, and save energy. "
    "EnergyBridge helps us understand the application of energy in joules. "
    "Sorting algorithms, regex operations, and others can be profiled for energy. "
    "Running experiments multiple times yields statistically valid energy measurements. "
) * 1000

def test_re():
    pattern = r"\b\w{5}\b"
    re.findall(pattern, text_sample)

def test_regex():
    pattern = r"\b\w{5}\b"
    regex.findall(pattern, text_sample)

def test_pyparsing():
    grammar = OneOrMore(Word(alphas))
    try:
        grammar.parseString(text_sample)
    except ParseException:
        pass

def test_nltk_tokenization():
    from nltk.tokenize import word_tokenize
    word_tokenize(text_sample)

def test_spacy_tokenization():
    nlp(text_sample)

def run_test_n_times(test_func, num_runs=RUNS):
    times_list = []
    for run in range(RUNS):
        start_time = time.perf_counter()
        test_func()
        elapsed_time = time.perf_counter() - start_time
        times_list.append(elapsed_time)
    avg_time = statistics.mean(times_list)
    return avg_time

def print_stats(lib_name, avg_time):
    print(f"{lib_name:20s} | time: {avg_time:.5f}s")

def get_next_filename(prefix="string", ext=".csv"):
    i = 1
    while os.path.exists(f"{prefix}{i}{ext}"):
        i += 1
    return f"{prefix}{i}{ext}"

def main():
    results = []
    
    avg_time = run_test_n_times(test_re)
    print_stats("re (built-in)", avg_time)
    results.append({"Library": "re (built-in)", "Time (s)": f"{avg_time:.5f}"})
    
    avg_time = run_test_n_times(test_regex)
    print_stats("regex", avg_time)
    results.append({"Library": "regex", "Time (s)": f"{avg_time:.5f}"})
    
    avg_time = run_test_n_times(test_pyparsing)
    print_stats("pyparsing", avg_time)
    results.append({"Library": "pyparsing", "Time (s)": f"{avg_time:.5f}"})
    
    avg_time = run_test_n_times(test_nltk_tokenization)
    print_stats("NLTK tokenization", avg_time)
    results.append({"Library": "NLTK tokenization", "Time (s)": f"{avg_time:.5f}"})
    
    avg_time = run_test_n_times(test_spacy_tokenization)
    print_stats("spaCy tokenization", avg_time)
    results.append({"Library": "spaCy tokenization", "Time (s)": f"{avg_time:.5f}"})
    
    filename = get_next_filename()
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["Library", "Time (s)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"\nResults saved in {filename}")

if __name__ == "__main__":
    main()