import time
import statistics
import re
import regex
from pyparsing import Word, alphas, OneOrMore, ParseException
import nltk
import spacy

nltk.download('punkt', quiet=True)
nlp = spacy.load("en_core_web_sm")
NUM_RUNS = 30

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
    _ = nlp(text_sample)

def run_test_n_times(test_func, num_runs=NUM_RUNS):
    times = []
    for _ in range(num_runs):
        start = time.perf_counter()
        test_func()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg_time = statistics.mean(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0
    return avg_time, std_dev

def print_stats(lib_name, avg, std):
    print(f"{lib_name:20s} | avg: {avg:.3f}s | std: {std:.3f}s")

def main():
    avg, std = run_test_n_times(test_re)
    print_stats("re (built-in)", avg, std)
    avg, std = run_test_n_times(test_regex)
    print_stats("regex", avg, std)
    avg, std = run_test_n_times(test_pyparsing)
    print_stats("pyparsing", avg, std)
    avg, std = run_test_n_times(test_nltk_tokenization)
    print_stats("NLTK tokenization", avg, std)
    avg, std = run_test_n_times(test_spacy_tokenization)
    print_stats("spaCy tokenization", avg, std)

if __name__ == "__main__":
    main()
