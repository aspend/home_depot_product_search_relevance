# home_depot_product_search_relevance

This is our repo for the kaggle competition [Home depot product search relevance] (https://www.kaggle.com/c/home-depot-product-search-relevance)
## Data Exploration
I have a done an exploration even though there is not much to explore because the problem is mostly a nlp. At the end of the ipython notebook you can find a link of the best data exploration I found in the forum.

## Text pre-processing
The input of the queries is full of typos and there are some synonyms that work better. [Here] (https://www.kaggle.com/steubk/home-depot-product-search-relevance/fixing-typos/comments) an interesting discussion.
The main points are:
* We can use the dictionary created with google and posted in the discussion
* We can find some pattern and modify words in the query
* We should follow the suggestion give by Silogram.
  * moulded -> molded #both spellings are correct
  * chain saw -> chainsaw #Again both are correct
  * barbecue -> bbq
  * black decker -> black+decker #Actually makes the spelling incorrect, but conforms to Home Depot standard
  * 0.5 -> 1/2
  * two piece -> 2 piece
  * rigid saw -> ridgid saw #Again, 'rigid saw' is a legal spelling but it's probably not what the user intended. Is this a spelling correction or a thesaurus?
  * Referring to William's example that
  * 'circle your sawe'-> 'circular saw'
  * 'circle [string] saw' -> 'circular saw'
  * '[number] lithium' -> '[number]v lithium'
  * 'circle [string beginning with y and ending in r] sawe' -> 'circular saw'

## Feature Engineering
We need to create features from our clean data set:
