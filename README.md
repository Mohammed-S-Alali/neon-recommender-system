
![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png)

  

<i>Neon team Members:</i> Lama Al Harbi - Mohammad Al Ali - Monirah Bin Taleb - Aisha Hakami

# Neon Recommender System

  

### Install

Project is created with:

  

![Python](https://img.shields.io/badge/Python-3.8-blueviolet)

![Framework](https://img.shields.io/badge/Framework-Flask-red)

![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-green)

![API](https://img.shields.io/badge/API-TMDB-fcba03)

![Pandas](https://img.shields.io/badge/Pandas-1.1.3-red)

![Numpy](https://img.shields.io/badge/Numpy%20-1.19.2-blue)

![surpris](https://img.shields.io/badge/Surprise%20-0.1-lightgrey)

![anaconda](https://img.shields.io/badge/Anaconda-Navigator-green)

  
  

## Introduction

  

Nowadays, a recommender systems are used by all major web sites successfully in order to filter content and make suggestions in a personalized way. Thus, in terms of reduced the information overload on the users the recommender systems will creates a business value. Furthermore, the recommender systems are the most visible and successful applications of Machine Learning and Artificial Intelligence technology in practice. Therefore, our aim is to create a business value to a local company to improve their service by building a recommender system, and STC were selected for this project with their service Jawwy IPTV since they shared its data in the open data initiative.

  

## Methodology

  

#### Content-based Filtering (CB)

  

This filtration strategy is based on the data provided about the programs. The algorithm recommends programs that are similar to the ones that a user has liked in the past. This similarity (cosine similarity) is computed from the data we have about the programs as well as the user’s past preferences.

  

**Pros** :

1. No cold-start problem, unlike Collaborative Filtering, if the programs have sufficient descriptions, we avoid the “new item problem”.
2.  Able to recommend to users with unique tastes 
3.  Able to recommend new & unpopular items – No first-rater problem.

**Cons** :

1. Content-Based tend to over-specialization: they will recommend items similar to those already consumed, with a tendency of creating a “filter bubble”.
2. Never recommends items outside the user’s content profile, people might have multiple interests.


  

------------------

#### Collaborative Filtering (CL)

This filtration strategy is based on the combination of the user’s behavior and comparing and contrasting that with other users’ behavior in the database. The history of all users plays an important role in this algorithm. The main difference between content-based filtering and collaborative filtering that in the latter, the interaction of all users with the items influences the recommendation algorithm while for content-based filtering only the concerned user’s data is taken into account.

  

*Pros and Cons of collaborative filtering techniques*

**Pros**:

1. Collaborative filtering systems work by people in system, and it is expected that people to be better at evaluating information than a computed function.

  
  

**Cons**:

1. Cold Start: a major challenge of Collaborative Filtering technique can be how to make recommendations for a new user who has recently entered the system; that is called the cold-start user problem.

2. Sparsity:

- The user/ratings matrix is sparse.

- Hard to find users that have rated the same items.

  

3. First rater:

- Cannot recommend an item that has not been previously rated.

- New items, Esoteric items.

  

4. Popularity bias:

  

- Cannot recommend items to someone with unique taste.

- Tends to recommend popular items.

--------------
  

#### Popularity-Based Recommendation System

  

- It is a type of recommendation system which works on the principle of popularity and or anything which is in trend. These systems check about the movie which is in trend or are most popular among the users and directly recommend those.

  

- For example, if most users often watch a program then the recommendation system will get to know that the program is most popular so for every new user, the recommendation system will recommend that program to that user.

--------------
  
#### Hybrid Methods

Implement two or more different recommenders and combine predictions

- Overcomes previous cons.

- Create a weighted recommender (weights chosen equally, combining the results of predict_cf and predict_cn).

 - Create different weighted recommender (weights are chosen equally, combining the results of predict_cf, predict_cn, and predict_popularity) 

- Create recommender based on popularity with weighted CL and CB (which CL and CB predictions affected by popularity prediction)

- Keep the strengths of CL, CB and popularity models.

- Overcomes CL, CB and popularity models cons.
  

-----------------------

  

#### Surprise

Is a Python scikit for building and analyzing recommender systems that deal with explicit rating data.

  

Surprise was designed with the following purposes in mind:

  

- Give users perfect control over their experiments.

  

- Provide various ready-to-use prediction algorithms such as baseline algorithms, neighborhood methods.

  

- Make it easy to implement new algorithm ideas.

  

- Provide tools to evaluate, analyse and compare the algorithms’ performance. Cross-validation procedures can be run very easily using powerful CV iterators (inspired by scikit-learn excellent tools.

  

- We use SVD because it taking into account implicit ratings.

  
  

## How To Run The Website ?

  

1. Clone this repository to your local machine.

2. Install all the libraries mentioned in the [requirements.txt]

3. Get your API key from https://www.themoviedb.org/. (Refer the below section on how to get the API key)

3. Replace YOUR_API_KEY in **both** the places (line no. 23 and 43) of `static/recommend.js` file.

4. Open your terminal/command prompt from your project directory and run the file `main.py` by executing the command `python main.py`.

5. Go to your browser and type `http://127.0.0.1:5000/` in the address bar.

6. Hurray! That's it.

  

## How To Get The API Key?

  

Create an account in https://www.themoviedb.org/, click on the `API` link from the left hand sidebar in your account settings and fill all the details to apply for API key. If you are asked for the website URL, just give "NA" if you don't have one. You will see the API key in your `API` sidebar once your request is approved.

  

## The Datasets

  
### Data Sources

1.  [Jawwy Dataset](https://www.stc.com.sa/wps/wcm/connect/arabic/individual/campaign/bigdata?utm_source=twitter&utm_campaign=open_data_day&utm_medium=tweet&utm_content=arabic)

2.  [The Movies Dataset](https://www.themoviedb.org/)

3.  [The info dataest](https://www.kaggle.com/shivamb/netflix-shows)

  
  

### Data Dictionary


|Feature|Discreption|Type|Example|
|--------|-----------|-----------|-----------|
|user_id|IPTV users were selected at random for inclusion. Their ids have been anonymized.|object|19694|
|date|represent the year, month, day when the watching occurred|object|2017-12-03|
|show_id|Unique ID for every Movie|int32|1760|
|program_name| Name of program and the name of episode.|object|Hell On Wheels The White pirit|
|cleaned_desc| Program description without punctuation, HTML or NonAscii characters.|object|Born without legs and stuck in foster care for...|
|type| Represent either the program is movie or tv show|object|tv show, movie|
|duration_seconds| represent the watching duration by seconds.|int64|2212|
|total_duration| Represent the program's full duration in seconds.|int64|7380|
|average_watching|Represent the ratio watching for each user for particular program in seconds.|float64|0.299729|

-----

  
  

## Results

  

|model name|HitRate|
|------------|-----------|
|content based |0.13728731905266134|
|collaborative based |0.5310759173150407|
|hybrid based |0.21422652206225704|
|hybrid based + popularity|0.39064318927699987|
|hybrid based * popularity|0.5417913539892272|

  
  

>  **Note:** The **HitRate** Generate the top n recommendation for a user and compare them to those the user watched. If they match then increase the hit rate by 1, do this for the complete dataset to get the hit rate. Since, we want to recommend movies that new to the user so the closest to 0 the better. We sum the number of hits for each movie our top-N list and divide by the total number of movies.

  

---
|model|ٍRMSE|fit_time|test_time
|--------|-----------|-----------|-----------|
|SVDpp() Using ALS|0.3286|4.947597|0.239184|
|BaselineOnly() Using ALS|0.3292|0.030240|0.040861|
|SVD() Using ALS| 0.3318|1.138251|0.068111|
|NMF() Using ALS|0.3594|1.514930|0.058801|

---


  

### Inspiration
---

- This recommender system are based on [How to build a content-based movie recommender system with Natural Language Processing](https://towardsdatascience.com/how-to-build-from-scratch-a-content-based-movie-recommender-with-natural-language-processing-25ad400eb243) and [Building and Testing Recommender Systems With Surprise, Step-By-Step](https://towardsdatascience.com/building-and-testing-recommender-systems-with-surprise-step-by-step-d4ba702ef80b) on Towards data science website. Also, [hybrid-recommender system](https://github.com/jkhlr/hybrid-recommender-system/blob/master/hybrid-solutions.ipynb) on Github.

- Front-end design inspired by @kishan0725 Github - [The-Movie-Cinema](https://github.com/kishan0725/The-Movie-Cinema)

- Comparison of collaborative filtering algorithms - [high-performance recommender systems]([https://www.researchgate.net/publication/220593852_Comparison_of_collaborative_filtering_algorithms_Limitations_of_current_techniques_and_proposals_for_scalable_high-performance_recommender_systems](https://www.researchgate.net/publication/220593852_Comparison_of_collaborative_filtering_algorithms_Limitations_of_current_techniques_and_proposals_for_scalable_high-performance_recommender_systems))


