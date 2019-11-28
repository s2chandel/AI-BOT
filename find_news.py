from newsapi import NewsApiClient


def find_news(text):
    newsapi = NewsApiClient(api_key='7c63c31875a14c92bd46c5562e423ff3')
    all_articles = newsapi.get_everything(q=text, sources='bbc-news',
                                      domains='http://www.bbc.co.uk',
                                      # from_param='2019-07-01',
                                      # to='2019-07-15',
                                      language='en',
                                      sort_by='publishedAt',
                                      page_size=5
                                    #   page=1
    )

    return all_articles
