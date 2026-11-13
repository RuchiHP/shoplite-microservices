import os

from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Database settings come from environment variables (needed later for Docker/Kubernetes)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.environ.get("MONGO_DB", "productdb")

client = MongoClient(MONGO_URI)
products = client[MONGO_DB]["products"]


def to_json(product):
    """Convert MongoDB's _id into a normal string id."""
    product["id"] = str(product.pop("_id"))
    return product


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/products", methods=["GET"])
def list_products():
    return jsonify([to_json(p) for p in products.find()]), 200


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or data.get("price") is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        product = {
            "name": data["name"],
            "price": float(data["price"]),
            "description": data.get("description", ""),
            "stock": int(data.get("stock", 0)),
        }
    except (TypeError, ValueError):
        return jsonify({"error": "Price and stock must be numbers"}), 400

    result = products.insert_one(product)
    product["_id"] = result.inserted_id
    return jsonify(to_json(product)), 201


@app.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = products.find_one({"_id": ObjectId(product_id)})
    except InvalidId:
        return jsonify({"error": "Invalid product id"}), 400

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(to_json(product)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))