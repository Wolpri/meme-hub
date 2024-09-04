from flask import Flask, request, render_template, redirect, send_file
import sqlite3
import base64
from PIL import Image
import os

def image_to_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html', template_folder='./templates', static_folder='./static')
  elif request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, password))
    connection.commit()
    connection.close()
    return redirect('/login')



@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html', template_folder='./templates', static_folder='./static')
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()
    if result:
      return redirect('/mem')
    else:
      return render_template('login.html', template_folder='./templates', static_folder='./static')

@app.route('/mem')
def mem():
  return render_template('mem.html', template_folder='./templates', static_folder='./static')


@app.route('/image')
def get_image():
  imageName = request.args.get('imageName')
  image_path = os.path.join('static/meme', imageName + '.png')
  return {'image': image_to_base64(image_path)}


if __name__ == '__main__':
  app.run
