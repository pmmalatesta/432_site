import sqlite3

def main():
    conn = sqlite3.connect("devdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content,likes FROM tweets ORDER BY likes DESC")
    results = cursor.fetchall()
    for twit in results:
        print("tweet %s, likes: %d" % (twit[0],twit[1]))

main()