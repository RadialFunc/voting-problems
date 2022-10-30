from flask import Flask, render_template, url_for, request, session, redirect, flash, session
import math
from replit import db
import random
app = Flask(__name__)
app.secret_key = 'ifjeriogjeriogjrtoig'

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        if session == {}:
            return render_template("index.html")
        else:
            return render_template("index2.html")


@app.route('/questions', methods=["GET", "POST"])
def questions():
    if request.method == "GET":
        if session == {}:
            return redirect('/')
        if db[session['full']][4]:
            return redirect('/')
        if session['account'] == "1":
            return render_template("questionsc.html")
        else:
            return render_template("questions.html")

    else:
        for i in range(1, 16):
            random = "q"+str(i)
            db[session['full']][3].append(request.form[random])
        db[session['full']][4] = True
        if session['account'] == "1":
            db[session['full']][7] = request.form['manifesto']
            imgurl = request.form["avatar"]
            db[session['full']][8] = imgurl
        return redirect("/")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        first = request.form["first"]
        last = request.form["last"]
        if first + last in db.keys():
            return render_template("404.html",
                                   message="Account already exists.")
        session['account'] = request.form['role']
        session['full'] = first + last
        if session['account']=="1":
        	db[first + last] = [request.form["password"],	request.form["zipcode"], request.form['role'], [], False, first, last, "", ""]
        else:
        	db[first + last] = [request.form["password"],	request.form["zipcode"], request.form['role'], [], False, first, last]	
        return redirect("/questions")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        first = request.form["first"]
        last = request.form["last"]
        password = request.form["password"]
        full = first + last
        if full not in db.keys():
            return render_template("404.html", message="Account not found.")
        else:
            if db[full][0] != password:
                return render_template("404.html",
                                       message="Incorrect Password.")
            else:
                session['account'] = db[full][2]
                session['full'] = full
                return redirect("/")


@app.route('/explore')
def explore():
    if session == {}:
        return redirect('/')
    count =0 
    other = 0
    stuff = []
    for account in db.keys():
        if count%4==0:
            stuff.append([])
        if db[account][2] == "1":
            count+=1
            stuff[other].append(account)
        if count%4==0:
            other+=1
		
    return render_template("explore.html", info=db, stuff=stuff)
  

@app.route('/explore/<name>')
def explorename(name):
	return render_template("people.html",person = name, description = db[name][7])

@app.route('/dashboard', methods=["GET", "POST"])
def dashboardc():
    if request.method == 'GET':
        if session == {}:
            return redirect("/")
        if session["account"] == "1":
            return render_template("dashboardc.html")
        valuee = {}
        for person in db.keys():
            total =0
            if db[person][2] =="1":
                if len(db[person][3])<15: 
                    print(person)
                for i in range (0, 15):
                    total += abs(int(db[person][3][i]) - int(db[session['full']][3][i]))
                valuee[person] = total

        valuee = dict(sorted(valuee.items(), key=lambda item: item[1]))
        v = list(valuee.keys())
        a = [v[0], v[1], v[2], v[3], v[4]]
        print(a)
        return render_template("dashboardv.html", people=a, info=db)
    else:
        avatarEdited = request.form["avatarEdited"]
        manifestoEdited = request.form["manifestoEdited"]
        print(session['full'])
        if avatarEdited != "":
            db[session['full']][8] =  avatarEdited
        if manifestoEdited != "":
            db[session['full']][7] = manifestoEdited

        return redirect("/dashboard")
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/news')
def news():
	return render_template("news.html")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=random.randint(2000, 9000))
