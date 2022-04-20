import nltk

'''
This method helps download the NLTK word datasets required for autophrase and domain-relevance.
NOTE: Make sure you are using a common conda environment for all the three components
and use the same environment to download the datasets.
'''
def download_nltk_data():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

if __main__ == '__main__':
    download_nltk_data()