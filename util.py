import sqlite3

def update_articles_table(links, site):
    bad_links = []
    with sqlite3.connect('data/newspaper.db') as conn:
        c = conn.cursor()
        for link in links:
            c.execute("""SELECT link
                        FROM articles
                        WHERE link="{}"
                        """.format(link))
            
            result = c.fetchone()
            if result:
                print("link already exists: {}".format(link))
                bad_links.append(link)
            else:
                c.execute("INSERT INTO articles VALUES (?, ?, NULL, NULL, NULL, NULL)", (site, link))
                conn.commit()
        return bad_links 