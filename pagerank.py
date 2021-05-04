import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    num_links = len(links)
    if num_links == 0: num_links = len(corpus)
    probability = damping_factor / num_links
    pd = dict.fromkeys(corpus, (1 - damping_factor) / len(corpus))
    for link in links:
        pd[link] += probability

    return pd


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    def normalize(v):
        return (v / n)

    pages = list(corpus.keys())
    visits = dict.fromkeys(pages, 0)
    page = random.choice(pages)
    visits[page] += 1
    for i in range(n - 1):
        tm = transition_model(corpus, page, damping_factor)
        weights = list(tm.values())
        pages = list(tm.keys())
        page = random.choices(pages, weights=weights, k=1)[0]
        visits[page] += 1

    visits = {k: normalize(v) for k,v in visits.items()}
    print(sum(visits.values()))
    return visits


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    def summation_for(page_r):
        total = 0
        for page_i in corpus:
            if page_r in corpus[page_i]:
                total += pagerank[page_i] / len(corpus[page_i])
            if not corpus[page_i]:
                total += pagerank[page_i] / N
        return total


    def max_accuracy_reached():
        for page in pagerank:
            if newrank[page] - pagerank[page] > 0.001:
                return False
        return True


    N = len(corpus)
    pagerank = dict.fromkeys(corpus, 1 / N)
    newrank = dict()
    while True:
        for page_r in pagerank:
            newrank[page_r] = ((1 - damping_factor) / N) + (damping_factor * summation_for(page_r))

        if max_accuracy_reached():
            break

        pagerank = newrank.copy()

    return pagerank



if __name__ == "__main__":
    main()
