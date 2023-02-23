import json
import pickle

with open('InsertProfile.json','r') as f:
        data = json.load(f)
        
annot = []
for i in data:
    for j in range(len(data[i])):
        annot.append(data[i][j])
print(annot)

labels = []
for i in data:
    for j in range(len(data[i])):
        labels.append(i)
print(labels)
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(binary=True)
train_annot = vectorizer.fit_transform(annot)

#print(vectorizer.get_feature_names_out())
#print(train_annot.toarray())

from sklearn import svm
clf_svm = svm.SVC(kernel='linear')
clf_svm.fit(train_annot, labels)

test_x = vectorizer.transform(['Recommend the best geometry for high speed machining'])
print(clf_svm.predict(test_x))
pickle.dump(clf_svm, open('profilemodel','wb'))

profilemodel = pickle.load(open('profilemodel','rb'))
result = profilemodel.predict(test_x)
print(result)
pickle.dump(vectorizer, open("profilevectorizer", "wb"))