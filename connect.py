import psycopg2

from config import config


def connect():
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def select(s):
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(s)
        selection = cur.fetchall()
        # print(selection)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return selection


def update(s):
    conn = None
    updated_rows = 0
    try:
        params = config()

        print('Connecting to the PostgreSQL database to update')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(""" UPDATE crawler SET visited = True WHERE url = '""" + s + """'""")
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return updated_rows


def update_timestamp(link, s):
    conn = None
    updated_rows = 0
    try:
        params = config()

        print('Connecting to the PostgreSQL database to update')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""UPDATE ksiazki SET scrap_time = (%s) WHERE url = '""" + link + """'""", (s,))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return updated_rows


def update_meta(query):
    conn = None
    updated_rows = 0
    try:
        params = config()

        print('Connecting to the PostgreSQL database to update')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return updated_rows


def update_book(link, book):
    conn = None
    updated_rows = 0
    try:
        params = config()

        print('Connecting to the PostgreSQL database to update')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = """ UPDATE k_data 
        SET title= %s, author=%s, price=%s, publisher=%s, series=%s, year=%s, pages=%s, cover=%s, 
        shop_url=%s, img_url=%s 
        WHERE shop_url = '""" + link + """'"""
        book_data = (book.title, book.author, book.price, book.publisher, book.series, book.year, book.pages,
                     book.cover, book.shop_url, book.img_url)
        cur.execute(query, book_data)
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return updated_rows


def insert(s, tabela='crawler', column='url'):
    conn = None
    try:
        params = config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        insert_query = """INSERT INTO """ + tabela + """ (""" + column + """) VALUES ('""" + s + """')"""
        cur.execute(insert_query)
        conn.commit()
        print("Record inserted successfully")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_book(book):
    conn = None
    try:
        params = config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        insert_query = """INSERT INTO k_data
         (title, author, price, publisher, series, year, pages, cover, shop_url, img_url) 
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        book_data = (book.title, book.author, book.price, book.publisher, book.series, book.year, book.pages,
                     book.cover, book.shop_url, book.img_url)
        cur.execute(insert_query, book_data)
        conn.commit()
        print("Record inserted successfully")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    # connect()
    l1 = select('select url from crawler')
    l2 = [x[0] for x in l1]
    print(*l2)
