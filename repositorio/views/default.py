from pyramid.view import view_config
from pymongo import MongoClient  
import json

@view_config(route_name='home', renderer='../templates/hometemplate.jinja2')
def home(request):
    return { }

@view_config(route_name='getposts', renderer='json')
def get_posts(request):
    client = MongoClient("mongodb+srv://teste:123@cluster0-jejnw.mongodb.net/test?retryWrites=true")
    db = client.base_deeper 
    posts = db.posts.find()  
    modelsview = []

    for post in posts: 
        theme_id = str(post['theme_id'])  
        data = {
            "_id": str(post['_id']),
            "theme_id": theme_id,
            "name": post['name'],
            "path": post['path'],
            "theme": db.themes.find_one({'_id': int(theme_id)})['name'] 
        } 
        modelsview.append(data)        

    return {'posts':  modelsview }

@view_config(route_name='ranking', renderer='../templates/rankingtemplate.jinja2')
def themes_ranking(request):
    return {}
  

@view_config(route_name='getranking', renderer='json')
def get_ranking(request):

    client = MongoClient("mongodb+srv://teste:123@cluster0-jejnw.mongodb.net/test?retryWrites=true")
    db = client.base_deeper

    pipeline = [ {"$group": {"_id": "$theme_id", "count": {"$sum": 1}}}]
    likes = list(db.posts_likes.aggregate(pipeline))
    notlikes = list(db.posts_notlikes.aggregate(pipeline)) 
    themes = db.themes.find()  

    modelsview = []
    for theme in themes:  
        theme_id = int(theme['_id'])
        liked = 0.0
        notliked = 0.0
        for like_theme in likes:  
            if int(like_theme['_id']) == theme_id:
                liked = float(like_theme['count']) 

        for notlike_theme in notlikes:            
            if int(notlike_theme['_id']) == theme_id:
                notliked = float(notlike_theme['count'])  
             
        score = liked - (notliked/2) 
        data = {             
            "score": score,
            "name": theme['name'] 
        } 
        modelsview.append(data)    

    return { "ranking" : sorted(modelsview, key = lambda i: i['score'], reverse = True)  }     

@view_config(route_name='themes', renderer='json')
def get_themes(request):
    client = MongoClient("mongodb+srv://teste:123@cluster0-jejnw.mongodb.net/test?retryWrites=true")
    db = client.base_deeper
    themes = list(db.themes.find())  
    return { "themes" : themes } 

@view_config(route_name='post', renderer='../templates/posttemplate.jinja2')
def view(request):    
    return {} 

@view_config(route_name='post', renderer='json', request_method='POST')
def post_video(request):

    name = request.POST['name']
    theme_id = request.POST['theme_id']   
    filename = request.storage.save(request.POST['file'], randomize=True)

    client = MongoClient("mongodb+srv://teste:123@cluster0-jejnw.mongodb.net/test?retryWrites=true")
    db = client.base_deeper  
    post = {  
              "theme_id" : theme_id, 
              "name" : name,
              "path": "/static/uploads/"+filename
           }
    posts = db.posts
    post_id = str(posts.insert_one(post).inserted_id)

    return {"post": {"_id" : post_id, "theme_id" : theme_id,"name" : name,"path": "/static/uploads/"+filename,"theme": db.themes.find_one({'_id': int(theme_id)})['name']} } 

@view_config(route_name='liked', renderer='json', request_method='POST')
def post_liked(request): 
    theme_id = request.POST['theme_id']
    post_id = request.POST['post_id']

    client = MongoClient("mongodb+srv://teste:123@cluster0-jejnw.mongodb.net/test?retryWrites=true")
    db = client.base_deeper  
    post_liked = { 
              "theme_id" : theme_id, 
              "post_id" : post_id 
           }
    posts_likes = db.posts_likes
    posts_likes.insert_one(post_liked)

    return {'result': "OK"}

@view_config(route_name='notliked', renderer='json', request_method='POST')
def post_notliked(request): 
    theme_id = request.POST['theme_id']
    post_id = request.POST['post_id']

    client = MongoClient("mongodb+srv://teste:123@cluster0-jejnw.mongodb.net/test?retryWrites=true")
    db = client.base_deeper  
    post_notliked = { 
              "theme_id" : theme_id, 
              "post_id" : post_id 
           }
    posts_notlikes = db.posts_notlikes
    posts_notlikes.insert_one(post_notliked)

    return {'result': "OK"} 

    