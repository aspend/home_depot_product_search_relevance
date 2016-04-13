# home_depot_product_search_relevance

This is our repo for the kaggle competition [Home depot product search relevance] (https://www.kaggle.com/c/home-depot-product-search-relevance)
## Data Exploration
I have a done an exploration. However, there is not much to explore because the problem is mostly nlp. At the end of the ipython notebook you can find a link of the best data exploration I found in the forum.

## Text pre-processing
The input of the queries is full of typos and there are some synonyms that work better. [Here] (https://www.kaggle.com/steubk/home-depot-product-search-relevance/fixing-typos/comments) an interesting discussion.
The main points are:
* We can use the dictionary created with google and posted in the discussion
* We can find some pattern and modify text
So far, I have followed [this] (https://www.kaggle.com/the1owl/home-depot-product-search-relevance/first-xgb-script/code) code  and I have added the google dictionary that is checking the typos. I believe it is already a good job. but I might have done some mistakes. (it takes quite a lot of time to run (10 min).. because I added the stemming on the product description). I did not use the stop words because we can use them just when we use TfIdf and word2vec..

## Feature Engineering
We need to create features from our clean data set. We could start to brainstorm some ideas. From [here] (https://www.kaggle.com/c/home-depot-product-search-relevance/forums/t/19993/number-of-features-how-to-go-from-20-to-200) we can get some good ideas
* length of the query in letters
* length of the query in words
* The number of typos in the query (?)
* Word2Vec between query and description/attributes/title
* TfIdf between query and description/attributes/title
* If word of the query is in the description (?)
* If word of the query is in the attributes (?)
* if word of the query is in the title (?)
*
