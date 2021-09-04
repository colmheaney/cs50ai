import csv
import itertools
import sys
import math
import pdb

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # # # Ensure probabilities sum to 1
    normalize(probabilities)

    # # # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    def get_p_have_trait(name, num_genes):
        if name in have_trait: return PROBS["trait"][num_genes][True]
        return PROBS["trait"][num_genes][False]

    def get_p_gene_from(parent):
        if parent in one_gene:
            return 0.5
        if parent in two_genes:
            return (1 - PROBS["mutation"])

        return PROBS["mutation"]

    def get_p_have_gene(name, num_genes):
        mother = people[name]['mother']
        father = people[name]['father']
        if mother is None and father is None:
            return PROBS["gene"][num_genes]
        else:
            if num_genes == 1:
                return get_p_gene_from(mother) * (1 - get_p_gene_from(father)) + get_p_gene_from(father) * (1 - get_p_gene_from(mother))

            elif num_genes == 2:
                return get_p_gene_from(mother) * get_p_gene_from(father)

            else:
                return (1 - get_p_gene_from(mother)) * (1 - get_p_gene_from(father))

    names = set(people)
    total_joint_p = []
    for name in names:
        # 1 copy
        if name in one_gene:
            p_have_gene = get_p_have_gene(name, 1)
            p_have_trait = get_p_have_trait(name, 1)

        # 2 copies
        elif name in two_genes:
            p_have_gene = get_p_have_gene(name, 2)
            p_have_trait = get_p_have_trait(name, 2)

        # 0 copies
        else:
            p_have_gene = get_p_have_gene(name, 0)
            p_have_trait = get_p_have_trait(name, 0)

        total_joint_p.append(p_have_trait * p_have_gene)
        
    return math.prod(total_joint_p)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    names = set(probabilities)
    for name in names:
        if name in one_gene:
            probabilities[name]["gene"][1] += p
        elif name in two_genes:
            probabilities[name]["gene"][2] += p
        else:
            probabilities[name]["gene"][0] += p

        if name in have_trait:
            probabilities[name]["trait"][True] += p
        else:
            probabilities[name]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    def get_normalized(probabilities):
        normalized = {}
        for p in probabilities:
            normalized[p] = probabilities[p] / sum(probabilities.values())

        return normalized

    names = set(probabilities)
    for name in names:
        normalized_genes = get_normalized(probabilities[name]["gene"])
        for g in probabilities[name]["gene"]:
            probabilities[name]["gene"][g] = normalized_genes[g]

        normalized_traits = get_normalized(probabilities[name]["trait"])
        for t in probabilities[name]["trait"]:
            probabilities[name]["trait"][t] = normalized_traits[t]


if __name__ == "__main__":
    main()
