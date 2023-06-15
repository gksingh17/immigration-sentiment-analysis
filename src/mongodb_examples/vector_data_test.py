from pymongo_get_database import get_database
dbname = get_database()
sample_word_embeddings = dbname["user_1_items"]

word_embeddings = {
    'word1': [4822, 4094, 991, 0, 1663, 0, 9, 835, 7, 4043, 3553, 4661, 1921, 3705, 0],
    'word2': [1443, 5283, 0, 3075, 5272, 2783, 2182, 0, 4715, 2569, 3056, 2538, 0, 2352, 0],
    'word3': [0.7, 0.8, 0.9, 0.4, 0.5, 0.6]
}

sample_word_embeddings.insert_one(word_embeddings)
# after this run test query to check insertion is being done or not