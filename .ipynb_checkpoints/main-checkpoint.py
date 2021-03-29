import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader,Dataset
import json
import bs4 as bs
import urllib.request
import pickle
import requests


def similarity1():
    data = pd.read_csv('data/main_data.csv')

    watch_crosstab_transpose = pd.read_csv('data/watch0.csv')
    watch_crosstab_transpose.reset_index(drop=True, inplace=True)
    watch_crosstab_transpose.set_index('movie_title',inplace=True,drop=True)
    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix_desc = count.fit_transform(data['comb'])

    # generating the cosine similarity matrix on program description
    cosine_sim = cosine_similarity(count_matrix_desc, count_matrix_desc)

    # generating the cosine similarity matrix on watch history
    cosine_sim_w = cosine_similarity(watch_crosstab_transpose.values, watch_crosstab_transpose.values)
    
    # assign the sum of watch per program as number_of_watch column
    watch_crosstab_transpose['number_of_watch'] = watch_crosstab_transpose.eq(1).sum(axis=1)

    # define the array which holds the precent of popularity
    prec_watch_mat = watch_crosstab_transpose['number_of_watch'].values/(len(watch_crosstab_transpose.columns)-1)

    return data,cosine_sim,cosine_sim_w,prec_watch_mat

def rcmnd0(m):
    m = m.lower()
    data,cosine_sim,cosine_sim_w,prec_watch_mat = similarity1()
    
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        data_df = data.copy()
        data_df.reset_index(drop=True, inplace=True)
        data_df.set_index('movie_title',inplace=True,drop=True)
        indices = pd.Series(data_df.index)

        # initializing the empty list of recommended movies
        recommended_movies = []    
        # gettin the index of the movie that matches the title
        idx = indices[indices == m].index[0]

        # creating a Series with the similarity scores of program description in descending order
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)        
        # getting the indexes of the 5 most similar movies
        top_5_indexes = list(score_series.iloc[1:5].index)
        # populating the list with the titles of the best 5 matching movies
        for i in top_5_indexes:
            recommended_movies.append(list(data_df.index)[i])

        return recommended_movies

def rcmnd1(m,type_of_recommendation):
    # m = m.lower()
    
    data,cosine_sim,cosine_sim_w,prec_watch_mat = similarity1()
    
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        data_df = data.copy()
        data_df.reset_index(drop=True, inplace=True)
        data_df.set_index('movie_title',inplace=True,drop=True)
        indices = pd.Series(data_df.index)
        
        # initializing the empty list of recommended movies
        recommended_movies = []
    
        # gettin the index of the movie that matches the title
        idx = indices[indices == m].index[0]
    
        if type_of_recommendation == 0:
            
            # creating a Series with the similarity scores of program description in descending order
            score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
        
        elif  type_of_recommendation == 1:
            
            # creating a Series with the similarity scores of watch history in descending order
            score_series = pd.Series(cosine_sim_w[idx]).sort_values(ascending = False)
        
        elif  type_of_recommendation == 2:
            
            # creating a Series with the similarity scores between watch history and program description in descending order
            score_series = pd.Series(cosine_sim_w[idx]*0.5 + cosine_sim[idx]*0.5).sort_values(ascending = False)

        elif  type_of_recommendation == 3:
            
            # creating a Series with the similarity scores between watch history and program description 
            # with popularity of program as indepent variables in descending order
            score_series = pd.Series(cosine_sim_w[idx]*0.33 + cosine_sim[idx]*0.33 + prec_watch_mat*0.34).sort_values(ascending = False)

        elif  type_of_recommendation == 4:
            
            # creating a Series with the similarity scores between watch history and program description 
            # as depent variables on popularity of program in descending order
            score_series = pd.Series((cosine_sim_w[idx]*0.5 + cosine_sim[idx]*0.5) * prec_watch_mat).sort_values(ascending = False)
        
        else:
            print('You have entered wrong value')
            return

        
        # getting the indexes of the 4 most similar movies
        top_4_indexes = list(score_series.iloc[1:5].index)
        
        # populating the list with the titles of the best 4 matching movies
        for i in top_4_indexes:
            recommended_movies.append(list(data_df.index)[i])
            
        return recommended_movies

def suprise(user_id):

    supris = pickle.load(open('supris.pkl','rb'))

    df_data= pd.read_csv('data/concat_data.csv')

    reader = Reader(rating_scale=(0.03, 1.0))
    data = Dataset.load_from_df(df_data[['user_id', 'show_id', 'average_watching']], reader)
    
    # get the list of the movie ids
    unique_ids = df_data['show_id'].unique()

    # get the list of the ids that the userid has rated
    iids1001 = df_data.loc[df_data['user_id']== user_id, 'show_id']

    # remove the rated movies for the recommendations
    movies_to_predict = np.setdiff1d(unique_ids,iids1001)

    my_recs = []
    for iid in movies_to_predict:
        my_recs.append((iid, supris.predict(uid=user_id,iid=iid).est))
    top_4_movie = pd.DataFrame(my_recs, columns=['iid', 'predictions']).sort_values('predictions', ascending=False).head(4) 
    top_4_movie['movie_title'] = top_4_movie.iid.map(lambda x: df_data.loc[df_data['show_id']== x , 'program_name'].iloc[0]) 
    return top_4_movie.movie_title.values.tolist()

# converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["','')
    my_list[-1] = my_list[-1].replace('"]','')
    return my_list

def get_suggestions():
    data = pd.read_csv('data/main_data.csv')
    return list(data['movie_title'].str.capitalize())

def get_user_id_list():
    data = pd.read_csv('data/concat_data.csv')
    return data.user_id.unique().tolist()


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    suggestions = get_suggestions()
    user_id_list = get_user_id_list()
    return render_template('home.html',suggestions=suggestions,user_id_list=user_id_list)

@app.route("/similarity",methods=["POST"])
def similarity():
    movie = request.form['name']
    user_id = request.form['user_id']
    movie = str(movie).lower()

    rc = rcmnd0(movie)
    arr_recommend = [suprise(user_id),rc,rcmnd1(movie,1),rcmnd1(movie,2),rcmnd1(movie,3),rcmnd1(movie,4)]
    
    if type(rc)==type('string'):
        return rc
    else:
        m_str=[ "---".join(element) for element in arr_recommend]
        return '_'.join(m_str)


@app.route("/recommend",methods=["POST"])
def recommend():
    # getting data from AJAX request
    title = request.form['title']
    cast_ids = request.form['cast_ids']
    cast_names = request.form['cast_names']
    cast_chars = request.form['cast_chars']
    cast_bdays = request.form['cast_bdays']
    cast_bios = request.form['cast_bios']
    cast_places = request.form['cast_places']
    cast_profiles = request.form['cast_profiles']
    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    rec_movies = [request.form[f'rec_movies_{i}'] for i in range(6)]
    rec_posters = [request.form[f'rec_posters_{i}'] for i in range(6)]

    # get movie suggestions for auto complete
    suggestions = get_suggestions()

    # call the convert_to_list function for every string that needs to be converted to list
    for i in range(6):
        rec_movies[i] = convert_to_list(rec_movies[i])
        rec_posters[i] = convert_to_list(rec_posters[i])

    cast_names = convert_to_list(cast_names)
    cast_chars = convert_to_list(cast_chars)
    cast_profiles = convert_to_list(cast_profiles)
    cast_bdays = convert_to_list(cast_bdays)
    cast_bios = convert_to_list(cast_bios)
    cast_places = convert_to_list(cast_places)
    
    unknown_img = 'https://bit.ly/2LSNCnp'

    for index, link in enumerate(cast_profiles):
        if link == 'https://image.tmdb.org/t/p/originalnull':
            cast_profiles[index] = unknown_img
        
    # convert string to list (eg. "[1,2,3]" to [1,2,3])
    cast_ids = cast_ids.split(',')
    cast_ids[0] = cast_ids[0].replace("[","")
    cast_ids[-1] = cast_ids[-1].replace("]","")
    
    # rendering the string to python string
    for i in range(len(cast_bios)):
        cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"','\"')
    
    # combining multiple lists as a dictionary which can be passed to the html file so that it can be processed easily and the order of information will be preserved
    movie_cards = []
    for index_arr_mov, arr_mov in enumerate(rec_movies):
            movie_cards.append({rec_posters[index_arr_mov][i]: arr_mov[i] for i in range(len(arr_mov))})

    casts = {cast_names[i]:[cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(4)}

    cast_list = [cast_ids, cast_chars, cast_profiles, cast_bdays, cast_places, cast_bios]

    max = 0
    for index, value in enumerate(cast_list):
        if len(value) > max:
            max = len(value)
    
    for index, value in enumerate(cast_list):
        if len(value) < max:
            if index == 0:
                cast_ids = cast_ids + ['None' for i in range(max - len(value))]
            elif index == 1:
                cast_chars = cast_chars + ['None' for i in range(max - len(value))]
            elif index == 2:
                cast_profiles = cast_profiles + [unknown_img for i in range(max - len(value))]
            elif index == 3:
                cast_bdays = cast_bdays + ['None' for i in range(max - len(value))]
            elif index == 4:
                cast_places = cast_places + ['None' for i in range(max - len(value))]
            elif index == 5:
                cast_bios = cast_bios + ['None' for i in range(max - len(value))]

    cast_details = {cast_names[i]:[cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in range(4)}

    
    # passing all the data to the html file
    return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,
        vote_count=vote_count,release_date=release_date,runtime=runtime,status=status,genres=genres,
        movie_cards_0=movie_cards[0],movie_cards_1=movie_cards[1],movie_cards_2=movie_cards[2],movie_cards_3=movie_cards[3],movie_cards_4=movie_cards[4],movie_cards_5=movie_cards[5],casts=casts,cast_details=cast_details)

if __name__ == '__main__':
    app.run(debug=True)
