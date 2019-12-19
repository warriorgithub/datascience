import data_controller as dc


class Questions:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def matchs(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        return "Do you have %s ?" % (str(self.value))


class Decision_Node:
    """A Decision Node asks a question.

    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


class Leaf:
    """A Leaf node classifies data.

    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training data that reach this leaf.
    """

    def __init__(self, rows):
        self.predictions = dc.class_counts(rows)


class QuestionPreserve:

    def __init__(self, question, u_input):
        self.question = question
        self.user_input = u_input
