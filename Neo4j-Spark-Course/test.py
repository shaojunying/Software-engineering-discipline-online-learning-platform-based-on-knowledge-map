import numpy
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.partial_fit(numpy.array([1,1]), numpy.array(['aa']), ['aa','bb'])
clf.partial_fit(numpy.array([6,1]), numpy.array(['bb']))
clf.predict(numpy.array([9,1]))