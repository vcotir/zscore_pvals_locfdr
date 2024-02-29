# zscore_pvals_locfdr

Ranking is an important tool that guides the decision making of those observing the rankings (whether that be users viewing Google search results, Pintrest's recommendations, Netflix movies). For this reason, it is important that mathematical components behind ranking algorithms be studied to elucidate the biases of such ranking algorithms and make more informed intentional decisions based on more full awareness of the tradeoffs.

The intention of this project was to compare the effects of biases in the top 10-20 results of lists sorted by average reviews, by p-value, and with local false discovery rate - a Bayesian statistic. 

[Link to the completed paper.](https://colab.research.google.com/drive/1KsOVZY-s884T0jOYFK4jzweSs4wL5Gu7#scrollTo=XWmVFdxNrvHL)

This codebase showcases the prelimenary components of this project. In particular, it showcases a webscraper for a provided URL CSV of allrecipe (a recipe sharing site) links. 

`modifledSudhanScraper.py` refers to a list of URL CSVs of allrecipe links and generates a new URL CSV list with review frequencies on 6 new fields (5 star, 4, 3, 2, 1 star reviews and 1 total reviews column)

> Example input of URL CSV entries
```
https://www.allrecipes.com/recipe/285598/golden-mashed-potatoes-with-green-onions/
https://www.allrecipes.com/recipe/285623/air-fryer-shrimp-tacos/
https://www.allrecipes.com/recipe/285597/golden-mashed-potatoes/
https://www.allrecipes.com/recipe/285749/brown-butter-apple-crisp-bars/
https://www.allrecipes.com/recipe/285741/christmas-brownies/
```

> Example output of URL CSV entries
```
https://www.allrecipes.com/recipe/228539/sweet-and-easy-spaghetti-squash/,3,0,0,1,4,8
https://www.allrecipes.com/recipe/10527/peanut-butter-no-bakes/,7,5,6,8,4,30
https://www.allrecipes.com/recipe/17003/old-fashioned-cream-scones/,2,1,1,3,1,8
https://www.allrecipes.com/recipe/24293/homemade-caramels/,14,0,4,9,13,40
https://www.allrecipes.com/recipe/109324/peanut-butter-delight/,0,1,0,0,1,2
```

`pValZValScript.py` creates a folder of CSVs where the extracted recipe review frequencies are sorted by the following metrics:
* Descending z-scores
* Descending average reviews
* Ascending p-values
