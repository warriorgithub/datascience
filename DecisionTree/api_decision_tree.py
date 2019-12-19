import pandas as pd
from flask import Flask, request, render_template, jsonify

import data_controller as dc
from models import Questions, Decision_Node, Leaf, QuestionPreserve

qp = QuestionPreserve(None, None)
wehealth_tranining = pd.read_excel('wehealth.xlsx')

user_input = [None] * 4


def get_question_response(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        print ("Predicted: %s" %(dc.print_leaf(classify(user_input, my_tree))))
        return classify(user_input, my_tree)

    qp.question = question
    return question


def user_interaction(val=None, question=None, rows=None):
    if not val:
        return get_question_response(rows)

    else:
        true_rows, false_rows = dc.partition(rows, qp.question)
        if val.lower() == 'yes':
            user_input.insert(qp.question.column, qp.question.value)
            return get_question_response(pd.DataFrame(true_rows))
        elif val.lower() == 'no':
            user_input.insert(qp.question.column, qp.question.value)
            return get_question_response(pd.DataFrame(false_rows))


def find_best_split(rows):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
    best_gain = 0  # keep track of the best information gain
    best_question = None  # keep train of the feature / value that produced it
    current_uncertainty = dc.gini(rows)

    n_features = len(rows.columns) - 1  # number of columns
    for col in range(n_features):  # for each feature
        values = rows.iloc[:, col].unique()  # unique values in the column

        for val in values:  # for each value

            question = Questions(col, val)

            # try splitting the dataset
            true_rows, false_rows = dc.partition(rows, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = dc.information_gain(pd.DataFrame(true_rows), pd.DataFrame(false_rows), current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy dataset.
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


def build_tree(rows):
    """Builds the tree.

    Rules of recursion: 1) Believe that it works. 2) Start by checking
    for the base case (no further information gain). 3) Prepare for
    giant stack traces.
    """

    # Try partitioing the dataset on each of the unique attribute,
    # calculate the information gain,
    # and return the question that produces the highest gain.
    gain, question = find_best_split(rows)

    # Base case: no further info gain
    # Since we can ask no further questions,
    # we'll return a leaf.
    if gain == 0:
        return Leaf(rows)

    # If we reach here, we have found a useful feature / value
    # to partition on.
    true_rows, false_rows = dc.partition(rows, question)

    # Recursively build the true branch.
    true_branch = build_tree(pd.DataFrame(true_rows))

    # Recursively build the false branch.
    false_branch = build_tree(pd.DataFrame(false_rows))

    # Return a Question node.
    # This records the best feature / value to ask at this point,
    # as well as the branches to follow
    # dependingo on the answer.
    return Decision_Node(question, true_branch, false_branch)


my_tree = build_tree(wehealth_tranining)


def classify(row, node):
    """See the 'rules of recursion' above."""
    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    print(row[1])
    if node.question.matchs(row):
        # print("row . ",row )

        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("chat_template.html")


@app.route("/get_question", methods=['GET'])
def index():
    res = request.args.get('msg')
    question = user_interaction(val=res, rows=wehealth_tranining)
    print question
    return jsonify({'question': question.__repr__()})


if __name__ == '__main__':
    app.run(host='localhost')
