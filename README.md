# zscore_pvals_locfdr

This project showcases a webscraper for a provided URL CSV of allrecipe (a recipe sharing site) links. 

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

