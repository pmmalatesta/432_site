# Webserver!

from aiohttp import web
import jinja2, sqlite3
import datetime, random, requests, time
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
        print(request.headers['X-Forwarded-For']);
        loc = getloc(request.remote)
        #loc = getloc("136.160.90.40")
        ts = time.time()
        cursor = conn.cursor()
        query ="INSERT INTO tweets (content, likes, user) VALUES(\"%s\",0,\"%s\");" %(data['content'], data['username'])
        #print(query)
        cursor.execute("INSERT INTO tweets (content, likes, user, location, timestamp) VALUES(?,0,?,?,?)", (data['content'],data['username'],loc,ts))
        #cursor.execute("INSERT INTO tweets (content, likes, user) VALUES(\"%s\",0,\"%s\");" %(data['content'], data['username']))
        conn.commit()

    raise web.HTTPFound("/")

async def like(request):
    idnum = request.query['id']
    cursor = conn.cursor()
    cursor.execute("SELECT likes FROM tweets WHERE id=?;", (idnum,))
    result = cursor.fetchone()[0];
    likenum = result+1
    cursor.execute("UPDATE tweets SET likes=? WHERE id=?;", (likenum,idnum))
    conn.commit()
    raise web.HTTPFound("/")

async def lickjson(request):
    idnum = request.query['id']
    cursor = conn.cursor()
    cursor.execute("SELECT likes FROM tweets WHERE id=?;", (idnum,))
    result = cursor.fetchone()[0];
    likenum = result + 1
    cursor.execute("UPDATE tweets SET likes=? WHERE id=?;", (likenum, idnum))
    conn.commit()
    mess = {'likecount': likenum}
    return web.json_response(mess)

def getloc(ip):
    key = "f38ee63872ad01f750acfa99e7fc8530"
    urlreq = "http://api.ipstack.com/%s?access_key=%s" % (ip, key)
    result = requests.get(urlreq)
    ipinfo = result.json()
    return "%s, %s" % (ipinfo['city'],ipinfo['region_name'])

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
                    web.get('/likes.json',lickjson),
                    web.post('/tweet', addTweet),
                    web.get('/like', like)])

    #web.run_app(app, host="0.0.0.0", port=80)
    web.run_app(app,host="127.0.0.1", port=4000)
    #print("Webserver 1.0")

if __name__=="__main__":
    main()

