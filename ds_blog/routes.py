from flask import render_template, url_for, redirect, flash
from ds_blog import ds_blog_inst


@ds_blog_inst.route('/')
@ds_blog_inst.route('/home')
def home():
    return render_template('home.html')

