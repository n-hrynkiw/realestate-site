from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database_setup import db, House, app
from cloudinary_setup import upload_image

CORS(app)

# Home Route
@app.route('/')
def home():
    return render_template("index.html")

# Get listings for a market
@app.route('/listings/<market>')
def get_listings(market):
    houses = House.query.filter_by(market=market).all()
    return jsonify({"listings": [house.__dict__ for house in houses]})

# Get house details
@app.route('/house/<market>/<house_id>')
def get_house(market, house_id):
    house = House.query.filter_by(market=market, house_id=house_id).first()
    return jsonify(house.__dict__) if house else jsonify({"error": "House not found"}), 404

# Upload house
@app.route('/upload', methods=['POST'])
def upload_house():
    data = request.form
    images = request.files.getlist('images')

    image_urls = [upload_image(image) for image in images if upload_image(image)]

    house = House(
        house_id=data['house_id'],
        market=data['market'],
        address=data['address'],
        price=data['price'],
        beds=data['beds'],
        baths=data['baths'],
        square_feet=data['square_feet'],
        details=data['details'],
        image_urls=image_urls
    )
    
    db.session.add(house)
    db.session.commit()
    return jsonify({"message": "House uploaded!"})

# Delete house
@app.route('/delete/<house_id>', methods=['DELETE'])
def delete_house(house_id):
    house = House.query.filter_by(house_id=house_id).first()
    if house:
        db.session.delete(house)
        db.session.commit()
        return jsonify({"message": "House deleted!"})
    return jsonify({"error": "House not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True, use_reloader=False)
