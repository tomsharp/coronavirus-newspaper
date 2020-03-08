import sqlite3
import pandas as pd
import numpy as np
from newspaper import Article
from newspaper import fulltext
import requests
from bs4 import BeautifulSoup

def get_incomplete_rows(site):
    with sqlite3.connect("data/newspaper.db") as conn:
        q = """
             SELECT * 
             FROM articles 
             WHERE site = "{}"
             AND title IS NULL
             AND authors IS NULL
             AND date IS NULL
             AND text IS NULL
             """.format(site)
        df = pd.read_sql(q, conn)
        return df

def build_article_data_cnn(row, db_path='data/newspaper.db'):
    url = row['link']
    article = Article(url)
    article.download()
    
    try:
        article.parse()

        row['title'] = article.title
        row['authors'] = ", ".join(article.authors)
        date = article.publish_date
        try:
            date = date.date()
        except:
            pass
        row['date'] = date

        html = article.html
        soup = BeautifulSoup(html, 'html.parser')
        text_divs = soup.findAll("div", {"class": "zn-body__paragraph"})
        row['text'] = " ".join([div.text for div in text_divs])

        return row
    
    except:
        row['title'] = np.nan 
        row['authors'] = np.nan 
        row['date'] = np.nan
        row['text'] = np.nan 
        return row

def build_article_data_nytimes(row, db_path='data/newspaper.db'):
    url = row['link']
    article = Article(url)
    article.download()
    
    try:
        article.parse()

        row['title'] = article.title
        row['authors'] = ", ".join(article.authors)
        date = article.publish_date
        try:
            date = date.date()
        except:
            pass
        row['date'] = date

        html = article.html
        soup = BeautifulSoup(html, 'html.parser')
        text_divs = soup.findAll("p")
        row['text'] = " ".join([div.text for div in text_divs])

        return row
    
    except:
        row['title'] = np.nan 
        row['authors'] = np.nan 
        row['date'] = np.nan
        row['text'] = np.nan  
        return row

def add_article_data(df, db_path="data/newspaper.db"):
    for _, row in df.iterrows():
        values = list(row.values[2:])
        values.append(row.values[1])
        values = tuple(values)

        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                        UPDATE articles 
                        SET title=?, 
                            authors=?, 
                            date=?, 
                            text=?
                        WHERE link=?;
                        """, values)
            conn.commit()


if __name__ == '__main__':
        
    # cnn
    cnn = get_incomplete_rows('cnn')
    assert len(cnn) != 0
    print("cnn articles:", len(cnn))
    cnn = cnn.apply(build_article_data_cnn, axis=1)
    add_article_data(cnn)

    # nytimes
    nytimes = get_incomplete_rows('nytimes')
    assert len(nytimes) != 0
    print("nytimes articles:", len(nytimes))
    nytimes = nytimes.apply(build_article_data_nytimes, axis=1) 
    add_article_data(nytimes)