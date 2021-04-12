# Webserver!

from aiohttp import web
import jinja2, sqlite3
import datetime, random, requests, time, aiohttp
import aiohttp_jinja2
global conn
import hashlib, secrets
#@aiohttp_jinja2.template('home.html.jinja2')
async def home(request):
    #if "logged_in" not in request.cookies:
    #    raise web.HTTPFound('/login')
    # they have a cookie is it correct?
    conn = sqlite3.connect("tweetdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT userName FROM users WHERE cookie = ?", (request.cookies['logged_in'],))
    whodis = cursor.fetchone()
    if whodis is None:
        login=False
        usern = "NA"
    else:
        login=True
        usern = whodis[0]

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tweets ORDER BY likes DESC")
    results = cursor.fetchall()
    conn.close()
    context = {"tittle": "WEBSITE", "money": random.randint(100,10000000), "twits": results,'loggedin':login,"user":usern}
    response= aiohttp_jinja2.render_template('home.html.jinja2',request,context)
    response.set_cookie('looged_in', 'yes')
    return response

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

@aiohttp_jinja2.template('loginpage.html.jinja2')
async def loginpg(request):
    return {}

async def logout(request):
    response = aiohttp_jinja2.render_template('loginpage.html.jinja2', request, {})
    response.cookies['logged_in'] = ''
    return response


async def addTweet(request):
    print(request.cookies['logged_in'])
    if "logged_in" not in request.cookies:
        raise web.HTTPFound('/login')
    # they have a cookie is it correct?
    conn = sqlite3.connect("tweetdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE cookie = ?", (request.cookies['logged_in'],))
    goodcook = cursor.fetchone()
    if goodcook is None:
        conn.close()
        raise web.HTTPFound('/login')
    data = await request.post()
    if data['content'] !="":
        loc = getloc(request.headers['X-Forwarded-For'])
        #loc = getloc("136.160.90.40")
        ts = time.time()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tweets (content, likes, user, location, timestamp) VALUES(?,0,?,?,?)", (data['content'],goodcook[0],loc,ts))
        #cursor.execute("INSERT INTO tweets (content, likes, user) VALUES(\"%s\",0,\"%s\");" %(data['content'], data['username']))
        conn.commit()
        conn.close()
        raise web.HTTPFound("/")
    raise web.HTTPFound('/login')

async def logpost(request):
    data = await request.post()
    conn = sqlite3.connect("tweetdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password,salt FROM users WHERE username = ?",(data['username'],))
    rec=cursor.fetchone()
    conn.close()
    if rec == None:
        raise web.HTTPFound('/')
    else:
        tocomp = data['pword'] + rec[1]
        if rec[0] == hashlib.md5(tocomp.encode('ascii')).hexdigest():
            conn = sqlite3.connect("tweetdb.db")
            cursor = conn.cursor()
            cook = secrets.token_hex(8)
            cursor.execute("UPDATE users SET cookie = ? WHERE username=?", (cook, data['username']))
            conn.commit()
            conn.close()
            response = web.Response(text="congrats!",
                                    status=302,
                                    headers={'Location':"/"})
            response.cookies['logged_in'] = cook
            return response
        else:
            raise web.HTTPFound('/')
    #cursor = conn.cursor()
    #cursor.execute("SELECT password FROM users WHERE username=?;", (uName,))
    #result = cursor.fetchone()[0];
    #if result == pword:

async def like(request):
    idnum = request.query['id']
    conn = sqlite3.connect("tweetdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT likes FROM tweets WHERE id=?;", (idnum,))
    result = cursor.fetchone()[0];
    likenum = result+1
    cursor.execute("UPDATE tweets SET likes=? WHERE id=?;", (likenum,idnum))
    conn.commit()
    conn.close()
    raise web.HTTPFound("/")

async def lickjson(request):
    idnum = request.query['id']
    conn = sqlite3.connect("tweetdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT likes FROM tweets WHERE id=?;", (idnum,))
    result = cursor.fetchone()[0];
    likenum = result + 1
    cursor.execute("UPDATE tweets SET likes=? WHERE id=?;", (likenum, idnum))
    conn.commit()
    conn.close()
    mess = {'likecount': likenum}
    return web.json_response(mess)

async def deltweet(request):
    mess = {'mess': "bad"}
    idnum = request.query['id']
    conn = sqlite3.connect("tweetdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user FROM tweets WHERE id=?;", (idnum,))
    result = cursor.fetchone()[0];
    cursor.execute("SELECT userName FROM users WHERE cookie=?;", (request.cookies['logged_in'],))
    r2 = cursor.fetchone()
    if r2 is None or r2[0] != result:
        return web.json_response(mess)
    cursor.execute("DELETE FROM tweets WHERE id=?;", (idnum,))
    conn.commit()
    conn.close()
    raise web.HTTPFound("/")

async def kewlbus(request):
    try:
        r = requests.get("http://127.0.0.1:5000/data.json")
        mess = {'connect': 1}
        return web.json_response(mess)
    except:
        mess = {'connect': 0}
        return web.json_response(mess)


def getloc(ip):
    key = "f38ee63872ad01f750acfa99e7fc8530"
    urlreq = "http://api.ipstack.com/%s?access_key=%s" % (ip, key)
    result = requests.get(urlreq)
    ipinfo = result.json()
    return "%s, %s" % (ipinfo['city'],ipinfo['region_name'])

def main():

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
                    web.get('/like', like),
                    web.get('/login', loginpg),
                    web.post('/login',logpost),
                    web.get('/logout',logout),
                    web.get('/delete.json',deltweet),
                    web.get('/redir', home),
                    web.get('/kewl.json', kewlbus)])
    #web.run_app(app, host="0.0.0.0", port=80)
    web.run_app(app,host="127.0.0.1", port=4000)
    #print("Webserver 1.0")

if __name__=="__main__":
    main()

