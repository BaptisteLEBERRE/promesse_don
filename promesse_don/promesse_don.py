from flask import Flask, render_template, request, url_for, Markup
from pymongo import MongoClient
import json
import datetime
import pandas as pd
import html


client = MongoClient("mongodb+srv://Baptiste:4l4nm00r3@cluster0.b2scl.mongodb.net/?retryWrites=true&w=majority")
donations = client.promesse_don.donations

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulaire',methods = ['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        result = request.form
        user_civi = result['civi']
        user_last_name = result['user_last_name']
        user_first_name = result['user_first_name']
        user_phone_number = result['user_phone_number']
        user_email = result['user_email']
        user_money = float(result['user_money'])

        client.promesse_don.donations.insert_one({"civi": user_civi, "last_name": user_last_name, "first_name": user_first_name, "phone_number": user_phone_number, "email": user_email, "money": user_money, "date": datetime.datetime.now()})
        print("bla\nbla\nbla")
        return render_template('index.html')

    return render_template('formulaire.html')

@app.route('/infos',methods = ['GET'])
def infos():
    pipe = [{'$group': {'_id': 0, 'total': {'$sum': '$money'}}}]
    cursor = donations.aggregate(pipeline=pipe)
    for group in cursor:
        money = group['total']

    d_count = donations.find().count()

    d_dict = donations.find()
    d_list = []
    for instance in d_dict:
        d_list.append(instance)
    df = pd.DataFrame(d_list)
    html_df = df.to_html(classes = 'contribution', index=False)
    template =  html.unescape(render_template("infos.html", money_raised = money, donations_count = d_count, donation_tab = html_df))
    return template
    

if __name__ == '__main__':
    app.run(debug=True)