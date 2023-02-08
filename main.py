from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
            # print(column.name)
        return dictionary
        #method 2: using dictiounary comprahnsion
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    data = db.session.query(Cafe).all()
    random_data = random.choice(data)
    return jsonify(cafe=random_data.to_dict())


new = []


@app.route("/all", methods=["GET"])
def all_data():
    data = db.session.query(Cafe).all()
    for i in data:
        new.append(i.to_dict())
        print(i)
    return jsonify(cafe=new)


@app.route("/search", methods=["GET"])
def search_cafe():
    query_location = request.args.get("loc")
    data = db.session.query(Cafe).filter_by(location=query_location).first()
    if data:
        return jsonify(cafe=data.to_dict())
    else:
        return jsonify(error={"not found": "sorry, we don't have a cafe at that location."})


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(responce={"succes": "Succesfully added the new cafe."})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=['PATCH'])
def update_coffee_price(cafe_id):
    query_price = request.args.get("price")
    data = db.session.query(Cafe).filter_by(id=cafe_id).first()
    # print(data)
    if data:
        da_to_update = Cafe.query.get(cafe_id)
        da_to_update.coffee_price = query_price
        db.session.commit()
        return jsonify(responce={"succes": "Succesfully added the new cafe."})
    else:
        return jsonify(error={"not found": "Sorry a cafe with that id was not found in database."})


## HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=['DELETE'])
def delete_cafe_data(cafe_id):
    qury_token = request.args.get("api_key")
    # print(data)

    if qury_token == 'TopSecretAPIKey':
        data = db.session.query(Cafe).filter_by(id=cafe_id).first()
        if data:
            da_to_delete = Cafe.query.get(cafe_id)
            db.session.delete(da_to_delete)
            db.session.commit()
            return jsonify(responce={"succes": "Succesfully deleted the new cafe."})
        else:
            return jsonify(error={"not found": "cafe id is not"})
    else:
        return jsonify(error={"error": "you'r api key is not valid check again"})


if __name__ == '__main__':
    app.run(debug=True)

