'''
This helper script creates 3 different lists with the following differences:
* One is by descending z-scores 
* One by descending average reviews 
* One by asending p-values 

Author: Victor Ngo
'''
import statistics
from math import sqrt
import pandas as pd

# Converting a Z-score to a p-value in Python.
import scipy.stats as st
import os 

zScoreFile = "data/starReviews-with-z-scores.csv"
averageReviewFile = "data/starReviews-sortedByDescendingAverageReview.csv"
pValFile = "data/starReviews-with-p-values-sortedAscending.csv"

def deleteFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
        print("Successfully! The File has been removed")
    else:
        print("Can not delete the file as it doesn't exists")

deleteFile(zScoreFile)
deleteFile(averageReviewFile)
deleteFile(pValFile)

fileStream = open(zScoreFile, "a")
fileStream2 = open(averageReviewFile, "a")
fileStream3 = open(pValFile, "a")

print()
averageReviewScoreTotal = 0
averageReviewScoreList = []
starReviewsDataFrame = pd.read_csv('starReviewFrequenciesOfPeanutButterCookieRecipes.csv')
# starReviewsDataFrame = starReviewsDataFrame.head()
starReviews = starReviewsDataFrame.values.tolist()
n = 0
numInsufficientReviews = 0
print(starReviews)
for i, [url, 
        rating5, rating4, rating3, rating2, rating1, ratingTotal
    ] in enumerate(starReviews):
    averageReview = (5*rating5 + 4*rating4 + 3*rating3 + 2*rating2 + rating1) / ratingTotal
    averageReviewScoreTotal += averageReview
    averageReviewScoreList.append(averageReview)
    print('reviews', [url, 
        rating5, rating4, rating3, rating2, rating1, ratingTotal])
    averageReview = (5*rating5 + 4*rating4 + 3*rating3 + 2*rating2 + rating1) / ratingTotal
    
    sum = rating5 * pow(5 - averageReview, 2) + \
        rating4 * pow(4 - averageReview, 2) + \
        rating3 * pow(3 - averageReview, 2) + \
        rating2 * pow(2 - averageReview, 2) + \
        rating1 * pow(1 - averageReview, 2)

    if (ratingTotal - 1) == 0:
        numInsufficientReviews = numInsufficientReviews + 1
        continue
    try:
        indivSDev = sqrt(sum / (ratingTotal - 1))
        n = n + 1
    except ValueError:
        print("Can't divide by zero!")
        # TODO - store these somewhere
        numInsufficientReviews = numInsufficientReviews + 1
        continue
    if (indivSDev == 0):
        numInsufficientReviews = numInsufficientReviews + 1
        continue
        # TODO store these somewhere too!
    
mu = averageReviewScoreTotal / n
print('n is' + str(n) + 'mu is:' + str(mu))

# sdev = statistics.stdev(averageReviewScoreList)
outputs = []

# calculates z scores for each recipe and writes a newline on a CSV file
for i, [url, 
        rating5, rating4, rating3, rating2, rating1, ratingTotal
    ] in enumerate(starReviews):
    averageReview = (5*rating5 + 4*rating4 + 3*rating3 + 2*rating2 + rating1) / ratingTotal
    
    sum = rating5 * pow(5 - averageReview, 2) + \
        rating4 * pow(4 - averageReview, 2) + \
        rating3 * pow(3 - averageReview, 2) + \
        rating2 * pow(2 - averageReview, 2) + \
        rating1 * pow(1 - averageReview, 2)

    if (ratingTotal - 1) == 0:
        continue
    try:
        indivSDev = sqrt(sum / (ratingTotal - 1))
    except ValueError:
        print("Can't divide by zero!")
        # TODO - store these somewhere
        continue
    if (indivSDev == 0): # ignore review when sum = 0
        continue
        # TODO store these somewhere too!

    indivStdErr = indivSDev / sqrt(ratingTotal)
    # zScore = (averageReview - mu) / indivSDev
    zScore = (averageReview - mu) / indivStdErr
    pvalue = st.norm.sf(zScore) # This transforms the Z-score to a p-value.
    pvalueAbs = st.norm.sf(abs(zScore))

    output = [url, 
        rating5, rating4, rating3, rating2, rating1, ratingTotal,
        averageReview,
        zScore, 
        pvalue,
        # 'Non abs' + str(pvalue) + ' AbsPVal' + str(pvalueAbs),
        indivSDev
    ]
    outputs.append(output)

def sortingFunctionZScores (outputArray):
    print('z score is:' + str(outputArray[len(outputArray) - 1]))
    print('output array is:' + ' '.join(map(lambda x: str(x), outputArray)))
    return outputArray[len(outputArray) - 3]

def getAveragesSort (outputArray):
    print('average review' + str(outputArray[len(outputArray) - 2]))
    return outputArray[len(outputArray) - 4]

def getPScoreSort (outputArray):
    return outputArray[len(outputArray) - 2]

outputs.sort(reverse=True, key=sortingFunctionZScores)
print('\n'.join(map(lambda x: str(x), outputs)) + '\n')

for i, outputArray in enumerate(outputs):
    fileStream.write(','.join(map(lambda x: str(x), outputArray)) + '\n')

fileStream.write('n is' + str(n) + '. mu is:' + str(mu))
fileStream.close()

outputs.sort(reverse=True, key=getAveragesSort)
for i, outputArray in enumerate(outputs):
    fileStream2.write(','.join(map(lambda x: str(x), outputArray)) + '\n')

fileStream2.write('n is' + str(n) + '. mu is:' + str(mu))
fileStream2.close()

outputs.sort(reverse=False, key=getPScoreSort)
for i, outputArray in enumerate(outputs):
    fileStream3.write(','.join(map(lambda x: str(x), outputArray)) + '\n')

fileStream3.write('n is' + str(n) + '. mu is:' + str(mu))
fileStream3.close()

print('numInsufficientReviews:' + str(numInsufficientReviews))