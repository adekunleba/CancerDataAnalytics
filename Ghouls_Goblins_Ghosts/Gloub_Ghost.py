
# coding: utf-8

# In[ ]:

import os

path = r"C:/Users/ADEKUNLE/Documents/GitHub/Kaggle Scripts/"
os.chdir(path)


# ### Fast and Naive implementation of Machine Leaning on Kaggle Ghouls,Goblins and Ghost DataSet

# In[ ]:

import pandas as pd
df = pd.read_csv('Ghouls_Goblins_Ghosts/Datasets/train.csv', index_col= 'id')
print(df.head())

testset = pd.read_csv('Ghouls_Goblins_Ghosts/Datasets/test.csv', index_col= 'id')
print(testset.head())


# ## Preliminary Data Exploration on Data
# Once the data is in dataframe, there are couple of preliminary exploration to carry out on the data.
# * Describe the data
# * Observe if there is null value in the data

# In[ ]:

print(df.describe(), '\n\n ----------------')
print(pd.isnull(df).any())


# In[ ]:

get_ipython().magic('matplotlib inline')
#Playing around with some plot using pandas plot() function, group the features into the mean per the type and plot the values 
#You can do same for each column of the grouped data, this particular plot help knows the importance of features on prediction
df.groupby('type').mean()['rotting_flesh'].plot(kind = 'bar')


# In[ ]:

#Output the label as y and drop the column from the datafram
y = df.type.copy()
X = df.drop('type', axis = 1)
print(X.dtypes)


# In[ ]:




# In[ ]:

#get the column of list of testset
columns = testset.columns.ravel().tolist()
#concatenate train and test sets together
concat_data = pd.concat([X, testset])

print(concat_data.head(), '\n\n', testset.tail())
#Looks the same


# In[ ]:

#TODO: How to know if color is important with the classification, plot a graph of color and how much they occur within the
#....monster class.
#define a function to encode a pandas.series
def encode_data(series):
    encoded = series.astype('category').cat.codes
    return encoded

y_encode = encode_data(y)
#concat_data['encode_color'] = encode_data(concat_data.color)
concat_data.drop('color', axis = 1, inplace = True)
#TODO: Try out get_dummies on color
#concat_data = pd.get_dummies(concat_data)
concat_data.head()

#TODO: Try dropping color after evaluating if its significant to your prediction


# In[ ]:

index_list = testset.index.ravel().tolist()

train_data, test_data = concat_data[~concat_data.index.isin(index_list)], concat_data[concat_data.index.isin(index_list)]
print(test_data.head(), '\n\n', train_data.head())


# In[ ]:




# In[ ]:

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_data, y_encode, test_size = 0.3, random_state = 7)


# In[ ]:

##### Try Support Vector on Data and draw Decision Boundary
from sklearn.svm import SVC
svc = SVC()
#svc = SVC(kernel = 'linear')
#svc.fit(train_data, y_encode)
#score = svc.score(X_test, y_test)
#print('Naively, SVC classifies data with {0}'.format(score*100) + ' accuracy')
#print(cross_val_score(svc, train_data, y_encode))

#Draw decision boundary


# In[ ]:

#TODO: #Implement a simple GridSearch on your dataset
from sklearn import grid_search
C = [i for i in range(1, 31)]
parameters = {'kernel': ('linear', 'poly', 'rbf', 'sigmoid'), 'C': [i for i in range(1, 30)]}
classifier = grid_search.GridSearchCV(svc, parameters)
classifier.fit(data_train, y_encode)


# In[ ]:

model = classifier.best_estimator_

from sklearn.model_selection import cross_val_score
print(cross_val_score(model, train_data, y_encode).mean())


# In[ ]:

y_guess = model.predict(test_data)

y_guess = pd.Series(y_guess).replace([0, 1, 2], ['Ghost', 'Ghoul', 'Goblin'])

#predictions = pd.Series(clfs[clf]['predictions']).replace([0, 1, 2], ['Ghost', 'Ghoul', 'Goblin'])
submission = pd.DataFrame(pd.concat([pd.Series(index_list), y_guess], axis = 1))
submission.columns = ['id', 'type']
submission.to_csv('submission_without_color' + '.csv', index = False)


# In[ ]:

from sklearn import linear_model
from sklearn import tree
from sklearn import neighbors
from sklearn import ensemble
from sklearn import svm
from sklearn import gaussian_process
from sklearn import naive_bayes
from sklearn import neural_network
from sklearn.model_selection import cross_val_score
clfs = {}

clfs['lr'] = {'clf': linear_model.LogisticRegression(), 'name':'LogisticRegression'}
clfs['rf'] = {'clf': ensemble.RandomForestClassifier(n_estimators=750, n_jobs=-1), 'name':'RandomForest'}
clfs['tr'] = {'clf': tree.DecisionTreeClassifier(), 'name':'DecisionTree'}
clfs['knn'] = {'clf': neighbors.KNeighborsClassifier(n_neighbors=4), 'name':'kNearestNeighbors'}
clfs['svc'] = {'clf': svm.SVC(kernel="linear"), 'name': 'SupportVectorClassifier'}
clfs['nusvc'] = {'clf': svm.NuSVC(), 'name': 'NuSVC'}
clfs['linearsvc'] = {'clf': svm.LinearSVC(), 'name': 'LinearSVC'}
clfs['SGD'] = {'clf': linear_model.SGDClassifier(), 'name': 'SGDClassifier'}
clfs['GPC'] = {'clf': gaussian_process.GaussianProcessClassifier(), 'name': 'GaussianProcess'}
clfs['nb'] = {'clf': naive_bayes.GaussianNB(), 'name':'GaussianNaiveBayes'}
clfs['bag'] = {'clf': ensemble.BaggingClassifier(neighbors.KNeighborsClassifier(), max_samples=0.5, max_features=0.5), 'name': "BaggingClassifier"}
clfs['gbc'] = {'clf': ensemble.GradientBoostingClassifier(), 'name': 'GradientBoostingClassifier'}
clfs['mlp'] = {'clf': neural_network.MLPClassifier(hidden_layer_sizes=(10,8,3), alpha=1e-5, solver='lbfgs'), 'name': 'MultilayerPerceptron'}


# In[ ]:

for clf in clfs:
    clfs[clf]['score'] = cross_val_score(clfs[clf]['clf'], train_data, y_encode.values.ravel(), cv=100)
    print(clfs[clf]['name'] + ": %0.4f (+/- %0.4f)" % (clfs[clf]['score'].mean(), clfs[clf]['score'].std()*2))


# In[ ]:

for clf in clfs:
    clfs[clf]['clf'].fit(train_data, y_encode.values.ravel())
for clf in clfs:
    clfs[clf]['predictions'] = clfs[clf]['clf'].predict(test_data)


# In[ ]:




# In[ ]:

for clf in clfs:
    predictions = pd.Series(clfs[clf]['predictions']).replace([0, 1, 2], ['Ghost', 'Ghoul', 'Goblin'])
    submission = pd.DataFrame(pd.concat([pd.Series(index_list), predictions], axis = 1))
    submission.columns = ['id', 'type']
    print(submission.head())
    submission.to_csv(clfs[clf]['name'] + '.csv', index = False)


# Improving your model

# In[ ]:

#Nice function to always submit kaggle assignment
def submission(model, fname, X):
    ans = pd.DataFrame(columns=['PassengerId', 'Survived'])
    ans.PassengerId = PassengerId
    ans.Survived = pd.Series(model.predict(X), index=ans.index)
    ans.to_csv(fname, index=False)


# In[ ]:

get_ipython().magic('pinfo pd.read_html')


# Naively, Training SVC gave a 74% accuracy, to try if training on the whole training dataset and testing on the provided dataset will ever imporve the accuracy of the model(what to watch out for is the effect of more training data)
#   * Caution: ensure you watch out for encoding the datasets seperately

# pd.get_dummies will work on both test and train data samples as long as you use the same variable names

# ### Suggestions that could be tried to make the model better
# * I can try to use get_dummy() encoding patter to see if there will be changes
# * I can try to normalize the dataset, or better still look through the dataset and look out the irrelevanceies in the dataset
# Note, once you have a model, I think the tunning aspect of Machine learning is, looking at the available data, what could probably be added, what could be removed.
# * I can try to look at dataset that are irrelevant in making predictions and try to remove them, since the end goal is to ensure that whatever dataset you give to it, it can successfully make a better prediction fro you.

# In[ ]:

#Apply PCA to train_data and test_data for visualization
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import numpy as np


from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
pca.fit(train_data)
    
data_train = pca.transform(train_data)

fig = plt.figure()
ax = fig.add_subplot(111) #Add subplot to the figure created
padding = 0.6
resolution = 0.0025
colors = ['royalblue','forestgreen','ghostwhite']
x_min, x_max = data_train[:, 0].min(), data_train[:, 0].max()
y_min, y_max = data_train[:, 1].min(), data_train[:, 1].max()
x_range = x_max - x_min
y_range = y_max - y_min
x_min -= x_range * padding
y_min -= y_range * padding
x_max += x_range * padding
y_max += y_range * padding
         #np.meshgrid creates a coordinate matrix from coordinate vectors (3 * 3 matrix)
xx, yy = np.meshgrid(np.arange(x_min, x_max, resolution), #arange return a given values from x_min, to x_max with resolution step
                       np.arange(y_min, y_max, resolution))

Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
  #np.c_just concatenate xx.ravel(), and yy.ravel()
Z = Z.reshape(xx.shape)

  # Plot the contour map
    #Contour lines are lines drawn to join two points of the same elevated height viewed for a level(e.g. sea level)
    #So using a data x, y, you can draw a contour line from it to make your decision plane   
cs = plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm)
#showing the contour line without the 'f'

for label in range(len(np.unique(y_encode))):
    indices = np.where(y_encode == label)
    plt.scatter(data_train[indices, 0], data_train[indices, 1], c=colors[label], label=str(label), alpha=0.8)

    
plt.show()

