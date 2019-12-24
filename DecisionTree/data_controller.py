


def unique_values(df,col):
    return df[col].unique()


def class_counts(df):
    counts = {}
    for rows in df.iloc[:,-1]:
        if rows not in counts:
            counts[rows] = 0
        counts[rows] += 1
    return counts


def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


def gini(rows):
    """Calculate the Gini Impurity for a list of rows.

    There are a few different ways to do this, I thought this one was
    the most concise. See:
    https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
    """
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity


def information_gain(left, right, current_uncertainty):
    """Information Gain.

    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def partition(df, question):
    """Partitions a dataset.

    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """

    true_branch, false_branch = [], []
    for index, row in df.iterrows():
        if question.matchs(row):
            true_branch.append(row)
        else:
            false_branch.append(row)
    return true_branch, false_branch


def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs