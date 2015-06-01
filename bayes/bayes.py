# Originally written to classify newsgroup messages based on the group they came from.
# Thus comments and code reflect the idea of 'messages' and 'categories'.
# Math still works regardless.

from operator import mul
import re

class Classifier:
    def __init__(self):
        # words include A-Z, '_' and allow contractions
        #self.SPLITTER = re.compile("(\w[\w']*\w|\w)")
    
        # words include A-Z and allow contractions
        self.SPLITTER = re.compile("([a-zA-Z][a-zA-Z']*[a-zA-Z]|[a-zA-Z])")

        # default 'n' to use
        self.TRAINING_SIZE = 0.5
        # default minimum word size (i.e. 3 avoids 'it', 'is', etc)
        self.MIN_FEAT_LEN = 3

        # track probabilities
        self.PROBABILITIES = {
            'p(C)':   {},
            'p(w|C)': {}
        }

        # track different document categories trained
        self.CATEGORIES = []

        # track word count by the document category where they are used
        # key is category, value is # of words in that category
        self.WORD_CT_BY_CATEGORY = {}

        # track word usage in each category
        # key is word, value is dict of {category: count}
        self.WORD_COUNTS_INV = {}

    # 'data' is an argument of form:
    #   {'cat1': [(id, [line1, line2, ...]), ..., (id, [line1, line2, ...])],
    #    'cat2': [(id, [line1, line2, ...]), ..., (id, [line1, line2, ...])],
    #    'cat3': ...}
    # For however many categories you want.  Often binary (class v. class) works best.
    def train(self, data):
        category_msg_ct = {}
        # track total message count (float for division later)
        total_msg_ct = 0.0

        # iterate through messages in each category
        for cat, msgs in data.items():
            # track the category
            self.CATEGORIES.append(cat)
            self.WORD_CT_BY_CATEGORY[cat] = 0

            category_msg_ct[cat] = len(msgs)
            total_msg_ct += len(msgs)
         
            for id,  msg in msgs[:int(round(self.TRAINING_SIZE * len(msgs)))]:
                self.train_message(msg, cat)

        # update the category conditional probability
        self.update_pC(category_msg_ct, total_msg_ct)

    # 'data' is a dataset just like for 'train()'
    # 'categories' is a list of categorie strings to train if you only 
    #              want a subset, i.e. ['cat1', 'cat3']
    def train_categories(self, data, categories):
        new_data = {}
        for cat in categories:
            new_data[cat] = data[cat]
        self.train(new_data)

    def train_message(self, msg, cat):
        # get counts of each 'word'
        counts = get_feature_counts(msg, self.SPLITTER, self.MIN_FEAT_LEN)
        for word, ct in counts.items():
            # default for each word is an empty dictionary
            self.WORD_COUNTS_INV.setdefault(word, {})
            # default key in that dictionary maps each category to a zero count
            self.WORD_COUNTS_INV[word].setdefault(cat, 0)
            # update the word count
            self.WORD_COUNTS_INV[word][cat] += ct
            self.WORD_CT_BY_CATEGORY[cat] += ct

    # update p(category), i.e. # messages in category / # total messages
    def update_pC(self, category_msg_ct, total_msg_ct):
        for k, v in category_msg_ct.items():
            prob = float(v) / total_msg_ct
            self.PROBABILITIES['p(C)'][k] = prob

    # same argument explanation as train()
    def classify(self, data):
        correct = 0
        total = 0.0

        for cat, msgs in data.items():
            for id, msg in msgs[int(round(self.TRAINING_SIZE * len(msgs))):]:
                pred = self.classify_message(msg, data.keys())[0][1]
                if pred == cat:
                    correct += 1
                total += 1
    
        score = correct / total * 100
        return score

    # same argument explanation as train_categories()
    def classify_categories(self, data, categories):
        new_data = {}
        for cat in categories:
            new_data[cat] = data[cat]
        return self.classify(new_data)

    def classify_message(self, msg, cats):
        # initial p(message|category) of 1.0
        category_prob = {k: 1.0 for k in cats}
        words = get_features(msg, self.SPLITTER, self.MIN_FEAT_LEN)
        for c in cats:
            for word in words:
                p = self.get_pwC(word, c)
                if p is None or p == 0.0: continue
                # multiple current probability by p(word|category)
                category_prob[c] *= p
            # multiply by p(category) to get final p(message|category)
            category_prob[c] *= self.get_pC(c)
        return list(reversed(sorted([(v, k) for k, v in category_prob.items()])))

    # returns p(category)
    def get_pC(self, cat):
        return self.PROBABILITIES['p(C)'][cat]

    # returns p(word | category)
    def get_pwC(self, word, cat):
        # defaults for each word is a dictionary with each category set to 0
        self.WORD_COUNTS_INV.setdefault(word, {})
        count = self.WORD_COUNTS_INV[word].setdefault(cat, 0)
        # normalize probability for words we haven't seen in training
        return (1 + count) / (1 + float(self.WORD_CT_BY_CATEGORY[cat]))

# counts words in the text of a message
# - 'msg' is a list of lines
# - returns a dictionary with {'word': count} pairs
# - type of 'words' is determined by the regex splitter used
# - returned features are automatically lowercase and longer than minlength
def get_feature_counts(msg, splitter, minlength=2):
    counts = {}
    words = filter(lambda x: len(x) > minlength, splitter.findall('\n'.join(msg)))
    for word in words:
        word = word.lower()
        if word not in counts.keys(): counts[word] = 1
        else:                         counts[word] = counts[word] + 1
    return counts

# returns 'words' in the text of a message
# - 'msg' is a list of lines
# - type of 'words' is determined by the regex splitter used
# - returned features are automatically lowercase and longer than minlength
def get_features(msg, splitter, minlength=2):
    return [w.lower() for w in filter(lambda x: len(x) > minlength, \
        splitter.findall('\n'.join(msg)))]

