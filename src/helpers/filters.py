from src import app
import string


@app.template_filter('uc_words')
def uc_words(text):
    return string.capwords(text)
