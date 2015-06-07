from newspaper import Article

__author__ = 'nekmo'

def generic(url):
    article = Article(url)
    article.download()
    article.parse()
    return article