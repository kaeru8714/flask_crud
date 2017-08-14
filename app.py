from flask import Flask, render_template, request, url_for, session, redirect
from mongoengine import IntField, StringField, Document, BooleanField, connect

connect("anging")

class Item(Document):
    name = StringField()
    price = IntField()
    quantity = IntField()
    availability = BooleanField()

    def delete_item(self):
        self.delete()

    def edit_item(self, name=None, price=None, quantity=None, availability=None):
        if (name):
            self.name = name
        if (price):
            self.price = price
        if (quantity):
            self.quantity = quantity
        if (availability):
            self.availability = availability
        self.save()

def create_item(name, price=None, quantity=None, availablity=None):
    i = Item()
    i.name = name
    if (price):
        i.price = int(price)
    if (quantity):
        i.quantity = int(quantity)
    i.availability = bool(availablity)
    i.save()

def edit_item(id, name, price=None, quantity=None, availablity=None):
    i = Item.objects(id=id)[0]
    i.name = name
    if (price):
        i.price = int(price)
    if (quantity):
        i.quantity = int(quantity)
    i.availability = bool(availablity)
    i.save()

def delete_item(id):
    i = Item.objects(id=id)[0]
    i.delete()

app = Flask(__name__)


@app.route('/')
def route():
    return redirect(url_for('list'))

@app.route('/list')
def list():
    dataSet = Item.objects()
    return render_template('list.html', dataSet=dataSet)

@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/create_action', methods=["GET", "POST"])
def create_action():
    if request.method == "POST":
        n = request.form['name']
        p = request.form['price']
        q = request.form['quantity']
        if (request.form['availability'] == 'false'):
            a = False
        else:
            a = True
        create_item(n,p,q,a)

    return redirect(url_for("list"))

@app.route('/edit_action', methods=["GET", "POST"])
def edit_action():
    if request.method == "POST":
        print(request.form)
        i = request.form['id']
        n = request.form['name']
        p = request.form['price']
        q = request.form['quantity']
        if (request.form['availability'] == 'false'):
            a = False
        else:
            a = True
        edit_item(i,n,p,q,a)
    return redirect(url_for("list"))


@app.route('/edit/<id>')
def edit(id):
    item = Item.objects(id=id)[0]
    return render_template("edit.html", item=item)

@app.route('/delete/<id>')
def delete(id):
    delete_item(id)
    return redirect(url_for("list"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)
