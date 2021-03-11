import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similarity1():
    data = pd.read_csv('main_data.csv')
#     data.reset_index(drop=True, inplace=True)
#     data.set_index('movie_title',inplace=True,drop=True)
    watch_crosstab_transpose = pd.read_csv('watch0.csv')
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
        
#         data.reset_index(drop=True, inplace=True)
#         data.set_index('movie_title',inplace=True,drop=True)
#         indices = pd.Series(data.index)
#         title = m
        # initializing the empty list of recommended movies
        recommended_movies = []    
        # gettin the index of the movie that matches the title
        idx = indices[indices == m].index[0]
#         idx = data.loc[data['movie_title']==m].index[0]

        # creating a Series with the similarity scores of program description in descending order
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)        
        # getting the indexes of the 10 most similar movies
        top_10_indexes = list(score_series.iloc[1:5].index)
        # populating the list with the titles of the best 10 matching movies
        for i in top_10_indexes:
            recommended_movies.append(list(data_df.index)[i])         
        return recommended_moviesdef rcmnd1(m,type_of_recommendation):
    # m = m.lower()

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