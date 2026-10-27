from flask import Blueprint, request, jsonify
from users.models.db import db
from products.models.product_model import Product

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('/api/productos', methods=['GET'])
def get_productos():
    return jsonify([p.to_dict() for p in Product.query.all()])

@product_controller.route('/api/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    p = Product.query.get(producto_id)
    if p is None:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify(p.to_dict())

@product_controller.route('/api/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    p = Product(nombre=data['nombre'],
                descripcion=data.get('descripcion'),
                precio=data['precio'],
                stock=data.get('stock', 0))
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@product_controller.route('/api/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    p = Product.query.get(producto_id)
    if p is None:
        return jsonify({'error': 'Producto no encontrado'}), 404
    data = request.get_json()
    p.nombre = data.get('nombre', p.nombre)
    p.descripcion = data.get('descripcion', p.descripcion)
    p.precio = data.get('precio', p.precio)
    p.stock = data.get('stock', p.stock)
    db.session.commit()
    return jsonify(p.to_dict())

@product_controller.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    p = Product.query.get(producto_id)
    if p is None:
        return jsonify({'error': 'Producto no encontrado'}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({'mensaje': 'Producto eliminado'})
