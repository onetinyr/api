import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from posts import app
from .database import session

@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """

    # Get the posts from the database
    posts = session.query(models.Post).order_by(models.Post.id)

    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")
  
@app.route("/api/posts/<int:id>", methods=["GET"])
def post_get(id):
    """ Single post endpoint """
    # Get the post from the database
    post = session.query(models.Post).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Return the post as JSON
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")
  
@app.route("/api/posts/<int:id>", methods=["DELETE"])
def post_delete(id):
    """ Single Post Delete endpoint """
    post = session.query(models.Post).get(id)
    
    #return 404 if post does not exist
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
      
    #session.query(models.Post).filter(id==id).delete()
    session.delete(post)
    session.commit()
    
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")
    
