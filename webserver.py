# Webserver!

from aiohttp import web
import jinja2
import datetime, random
import aiohttp_jinja2
@aiohttp_jinja2.template('home.html.jinja2')
async def home(request):

    return {"tittle": "WEBSITE", "money": random.randint(100,10000000)}

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


def main():
    app = web.Application()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))
    app.add_routes([web.get('/', home),
                    web.get('/yoga', yoga),
                    web.get('/baking', baking),
                    web.get('/jits', jits),
                    web.static('/static', 'static')])

    web.run_app(app, host="0.0.0.0", port=80)
    #print("Webserver 1.0")

if __name__=="__main__":
    main()

