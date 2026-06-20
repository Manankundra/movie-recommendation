import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("data\movies.csv")
ratings = pd.read_csv("data\Ratings.csv")

merged = pd.merge(movies , ratings , on="movieId", how="inner")

user_movie_matrix = merged.pivot_table(
    index="userId",
    columns="title",
    values="rating"
)

movie_rating_count = merged.groupby("title")["rating"].count()
popular_movies = movie_rating_count[movie_rating_count >= 50].index

filtered_matrix = user_movie_matrix[popular_movies]
filtered_matrix_filled = filtered_matrix.fillna(0)


similarity = cosine_similarity(filtered_matrix_filled.T)

def recommend(movie_name , n=5):
    
    if movie_name not in filtered_matrix_filled.columns:
        return "Movie not found in the data set ."
    
    movie_index = filtered_matrix_filled.columns.get_loc(movie_name)
    similar_movies = similarity[movie_index]
    movies_list = sorted(list(enumerate(similar_movies)),key=lambda x : x[1] , reverse=True)
    recommended = movies_list[1:n+1]
    
    for i in recommended : 
        print(filtered_matrix_filled.columns[i[0]])
        

# ***************************************************************


content_based_data = pd.read_csv(r"data\content_based.csv")
content_based_data["movie_id"] = content_based_data.index

filled_content_data = content_based_data.fillna(0)

titles = filled_content_data["title"]
generes = filled_content_data[[
    "Action","Adventure","Animation","Comedy","Crime",
    "Drama","Family","Fantasy","History","Horror",
    "Music","Mystery","Romance","Sci-Fi","Thriller",
    "War","Western"
]]

similarity2 = cosine_similarity(generes)

def recommend_content(movie_name , n=5):
    
    if movie_name not in filled_content_data["title"].values:
        return "Movie not found in the data set ."
    
    movie_index = filled_content_data[filled_content_data["title"]==movie_name].index[0]
    
    similar_movies = similarity2[movie_index]
    
    movie_list = sorted(list(enumerate(similar_movies)),key=lambda x:x[1] , reverse=True)[1:n+1]
    
    recommendations = [filled_content_data.iloc[i[0]]["title"] for i in movie_list]
    return recommendations
    
# ***********************************