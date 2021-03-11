# Webserver!

from aiohttp import web
import jinja2, sqlite3
import datetime, random
import aiohttp_jinja2
global conn
@aiohttp_jinja2.template('home.html.jinja2')
async def home(request):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tweets ORDER BY likes DESC")
    results = cursor.fetchall()
    return {"tittle": "WEBSITE", "money": random.randint(100,10000000), "twits": results}

@aiohttp_jinja2.template('yoga.html.jinja2')
async def yoga(request):

    return {"benefits": ["Improved Flexibility", "Relaxation", "Injury Prevention", "Mindfulness"]}

@aiohttp_jinja2.template('baking.html.jinja2')
async def baking(request):
    return {"tod" : datetime.datetime.now().hour}

@aiohttp_jinja2.template('jits.html.jinja2')
async def jits(request):
    listoNames = ["South American Ground Karate", "Involuntary Yoga", "Jiu Jitsu", "柔術", "Combat Cuddles", "The Gentle Art", "Sweaty Tights Session"]
    return {"whatwecalled": random.choice(listoNames)}


async def addTweet(request):
    data = await request.post()
    if data['username'] != "" and data['content'] !="":
        cursor = conn.cursor()
        query ="INSERT INTO tweets (content, likes, user) VALUES(\"%s\",0,\"%s\");" %(data['content'], data['username'])
        #print(query)
        cursor.execute("INSERT INTO tweets (content, likes, user) VALUES(?,0,?)", (data['content'],data['username']))
        #cursor.execute("INSERT INTO tweets (content, likes, user) VALUES(\"%s\",0,\"%s\");" %(data['content'], data['username']))
        conn.commit()
    raise web.HTTPFound("/")

async def like(request):
    idnum = int(request.query['id'])
    cursor = conn.cursor()
    query = "SELECT likes FROM tweets WHERE id=\"%d\"" %idnum
    cursor.execute(query)
    result = cursor.fetchone()[0];
    likenum = result+1
    addlike = "UPDATE tweets SET likes=%d WHERE id=%d;" %(likenum,idnum)
    cursor.execute("UPDATE tweets SET likes=? WHERE id=?;", (likenum,idnum))
    conn.commit()
    raise web.HTTPFound("/")

def main():
    global conn
    conn = sqlite3.connect("tweetdb.db")
    app = web.Application()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))
    app.add_routes([web.get('/', home),
                    web.get('/yoga', yoga),
                    web.get('/baking', baking),
                    web.get('/jits', jits),
                    web.static('/static', 'static'),
                    web.post('/tweet', addTweet),
                    web.get('/like', like)])

    #web.run_app(app, host="0.0.0.0", port=80)
    web.run_app(app,host="0.0.0.0", port=80)
    #print("Webserver 1.0")

if __name__=="__main__":
    main()

