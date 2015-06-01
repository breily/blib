
bayes
=====

* Implements naive Bayes document classification.
* Given a number of text documents that are assigned to certain categories,
  can predict the probability of a new document appearing in a category.
* I.e. email, newsgroup messages, languages, etc.

Usage
-----

Create a message set:
    
    >>> data = {'english': [(1, ['this is english', 'verbs nouns adjectives'])],
                'deutsch': [(2, ['es ist Deutsch', 'ich will Deutsch sprechen'])]
               }

Create a classifier and train:

    >>> c = bayes.Classifier()
    >>> c.train(data)

And predict future data:

    >>> c.classify_message(['ich liebe Deutsch'], ['english', 'deutsch'])
    [(0.06, 'deutsch'), ('0.0139', 'english')]

