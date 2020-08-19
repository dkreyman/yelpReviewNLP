#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Natural Language Processing Project
# 
# Welcome to the NLP Project for this section of the course. In this NLP project you will be attempting to classify Yelp Reviews into 1 star or 5 star categories based off the text content in the reviews. This will be a simpler procedure than the lecture, since we will utilize the pipeline methods for more complex tasks.
# 
# We will use the [Yelp Review Data Set from Kaggle](https://www.kaggle.com/c/yelp-recsys-2013).
# 
# Each observation in this dataset is a review of a particular business by a particular user.
# 
# The "stars" column is the number of stars (1 through 5) assigned by the reviewer to the business. (Higher stars is better.) In other words, it is the rating of the business by the person who wrote the review.
# 
# The "cool" column is the number of "cool" votes this review received from other Yelp users. 
# 
# All reviews start with 0 "cool" votes, and there is no limit to how many "cool" votes a review can receive. In other words, it is a rating of the review itself, not a rating of the business.
# 
# The "useful" and "funny" columns are similar to the "cool" column.
# 
# Let's get started! Just follow the directions below!

# ## Imports
#  **Import the usual suspects. :) **

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# ## The Data
# 
# **Read the yelp.csv file and set it as a dataframe called yelp.**

# In[4]:


df = pd.read_csv('yelp.csv')


# ** Check the head, info , and describe methods on yelp.**

# In[5]:


df.info()


# In[6]:


df.describe()


# In[7]:


df.head()


# **Create a new column called "text length" which is the number of words in the text column.**

# In[18]:


df['text length'] = df['text'].apply(len)


# # EDA
# 
# Let's explore the data
# 
# ## Imports
# 
# **Import the data visualization libraries if you haven't done so already.**

# In[101]:





# **Use FacetGrid from the seaborn library to create a grid of 5 histograms of text length based off of the star ratings. Reference the seaborn documentation for hints on this**

# In[19]:


g = sns.FacetGrid(df, col = 'stars')
g.map(plt.hist,'text length')


# **Create a boxplot of text length for each star category.**

# In[21]:


sns.boxplot(df['stars'], df['text length'])


# **Create a countplot of the number of occurrences for each type of star rating.**

# In[25]:


sns.countplot(x = df['stars'])


# ** Use groupby to get the mean values of the numerical columns, you should be able to create this dataframe with the operation:**

# In[28]:


stars = df.groupby('stars').mean()
stars


# **Use the corr() method on that groupby dataframe to produce this dataframe:**

# In[34]:


stars.corr()


# **Then use seaborn to create a heatmap based off that .corr() dataframe:**

# In[35]:


sns.heatmap(stars.corr(), cmap = 'coolwarm', annot = True)


# ## NLP Classification Task
# 
# Let's move on to the actual task. To make things a little easier, go ahead and only grab reviews that were either 1 star or 5 stars.
# 
# **Create a dataframe called yelp_class that contains the columns of yelp dataframe but for only the 1 or 5 star reviews.**

# In[51]:


yelp_class = df[(df.stars == 1) | (df.stars == 5)]


# ** Create two objects X and y. X will be the 'text' column of yelp_class and y will be the 'stars' column of yelp_class. (Your features and target/labels)**

# In[52]:


X = yelp_class['text']
y = yelp_class['stars']


# **Import CountVectorizer and create a CountVectorizer object.**

# In[53]:


from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer()


# ** Use the fit_transform method on the CountVectorizer object and pass in X (the 'text' column). Save this result by overwriting X.**

# In[54]:


X = vec.fit_transform(X)


# ## Train Test Split
# 
# Let's split our data into training and testing data.
# 
# ** Use train_test_split to split up the data into X_train, X_test, y_train, y_test. Use test_size=0.3 and random_state=101 **

# In[58]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


# In[121]:





# ## Training a Model
# 
# Time to train a model!
# 
# ** Import MultinomialNB and create an instance of the estimator and call is nb **

# In[60]:


from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()


# **Now fit nb using the training data.**

# In[61]:


nb.fit(X_train, y_train)


# ## Predictions and Evaluations
# 
# Time to see how our model did!
# 
# **Use the predict method off of nb to predict labels from X_test.**

# In[64]:


prediction =nb.predict(X_test)


# ** Create a confusion matrix and classification report using these predictions and y_test **

# In[63]:


from sklearn.metrics import confusion_matrix, classification_report


# In[66]:


print(confusion_matrix(y_test,prediction))
print(classification_report(y_test,prediction))


# **Great! Let's see what happens if we try to include TF-IDF to this process using a pipeline.**

# # Using Text Processing
# 
# ** Import TfidfTransformer from sklearn. **

# In[68]:


from sklearn.feature_extraction.text import TfidfTransformer


# ** Import Pipeline from sklearn. **

# In[71]:


from sklearn.pipeline import Pipeline


# ** Now create a pipeline with the following steps:CountVectorizer(), TfidfTransformer(),MultinomialNB()**

# In[73]:


pipeline = Pipeline([
    ('vec', CountVectorizer()),
    ('tfid', TfidfTransformer()),
    ('classifier', MultinomialNB()),
    
])


# ## Using the Pipeline
# 
# **Time to use the pipeline! Remember this pipeline has all your pre-process steps in it already, meaning we'll need to re-split the original data (Remember that we overwrote X as the CountVectorized version. What we need is just the text**

# ### Train Test Split
# 
# **Redo the train test split on the yelp_class object.**

# In[74]:


X = yelp_class['text']
y = yelp_class['stars']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


# **Now fit the pipeline to the training data. Remember you can't use the same training data as last time because that data has already been vectorized. We need to pass in just the text and labels**

# In[75]:


pipeline.fit(X_train, y_train)


# ### Predictions and Evaluation
# 
# ** Now use the pipeline to predict from the X_test and create a classification report and confusion matrix. You should notice strange results.**

# In[76]:


prediction2 = pipeline.predict(X_test)


# In[77]:


print(confusion_matrix(y_test,prediction))
print(classification_report(y_test,prediction))


# Looks like Tf-Idf actually made things worse! That is it for this project. But there is still a lot more you can play with:
# 
# **Some other things to try....**
# Try going back and playing around with the pipeline steps and seeing if creating a custom analyzer like we did in the lecture helps (note: it probably won't). Or recreate the pipeline with just the CountVectorizer() and NaiveBayes. Does changing the ML model at the end to another classifier help at all?

# # Great Job!
