from flask import Flask, request, jsonify, make_response, Blueprint
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os
from src.models import BlogPost
from src import db
from src.authenticate import token_required


blog_apis = Blueprint('blog_posts',__name__)





@blog_apis.route('/post', methods=['GET'])
@token_required
def get_all_posts(current_user):
    posts = BlogPost.query.filter_by(author_id=current_user.id).all()

    output = []

    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['title'] = post.title
        post_data['text'] = post.text
        output.append(post_data)

    return jsonify({'posts' : output})

@blog_apis.route('/post/<post_id>', methods=['GET'])
@token_required
def get_one_post(current_user, post_id):
    post = BlogPost.query.filter_by(id=post_id, author_id=current_user.id).first()

    if not post:
        return jsonify({'message' : 'No post found!'}), 404

    post_data = {}
    post_data['id'] = post.id
    post_data['title'] = post.title
    post_data['text'] = post.text

    return jsonify(post_data)

@blog_apis.route('/post', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()

    new_post = BlogPost(title=data['title'], text=data['text'], author_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message' : "New post created!"})


@blog_apis.route('/post/<post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    post = BlogPost.query.filter_by(id=post_id, author_id=current_user.id).first()

    if not post:
        return jsonify({'message' : 'No post found!'})

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message' : 'Post deleted!'})

