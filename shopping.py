import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from time import strptime
import numpy as np

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        -0 Administrative, an integer
        -1 Administrative_Duration, a floating point number
        -2 Informational, an integer
        -3 Informational_Duration, a floating point number
        -4 ProductRelated, an integer
        -5 ProductRelated_Duration, a floating point number
        -6 BounceRates, a floating point number
        -7 ExitRates, a floating point number
        -8 PageValues, a floating point number
        -9 SpecialDay, a floating point number
        -10 Month, an index from 0 (January) to 11 (December)
        -11 OperatingSystems, an integer
        -12 Browser, an integer
        -13 Region, an integer
        -14 TrafficType, an integer
        -15 VisitorType, an integer 0 (not returning) or 1 (returning)
        -16 Weekend, an integer 0 (if false) or 1 (if true)

    -17
    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    def format_row(row):
        row[10] = 'Jun' if row[10] == 'June' else row[10]

        row[0] = int(row[0])
        row[1] = float(row[1])
        row[2] = int(row[2])
        row[3] = float(row[3])
        row[4] = int(row[4])
        row[5] = float(row[5])
        row[6] = float(row[6])
        row[7] = float(row[7])
        row[8] = float(row[8])
        row[9] = float(row[9])
        row[10] = strptime(row[10],'%b').tm_mon
        row[11] = int(row[11])
        row[12] = int(row[12])
        row[13] = int(row[13])
        row[14] = int(row[14])
        row[15] = 1 if row[15] == 'Returning_Visitor' else 0
        row[16] = 1 if row[16] == 'TRUE' else 0
        row[17] = 1 if row[17] == 'TRUE' else 0
        return row

    evidence = []
    labels = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader, None) # Skip header
        for row in reader:
            formatted_row = format_row(row)
            evidence.append(formatted_row[:-1])
            labels.append(formatted_row[-1])

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (labels, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    merged_arrary = np.add(labels, predictions)
    true_positive = np.where(merged_arrary == 2)
    true_negative = np.where(merged_arrary == 0)

    sensitivity = true_positive[0].size / labels.count(1)
    specificity = true_negative[0].size / labels.count(0)

    return (sensitivity, specificity)



if __name__ == "__main__":
    main()
