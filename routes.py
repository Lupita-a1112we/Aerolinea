from flask import Flask, render_template, request, redirect, url_for
from models import db, Cliente, Vuelo, Reserva

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vuelos')
def vuelos():
    vuelos = Vuelo.query.all()
    return render_template('vuelos.html', vuelos=vuelos)

@app.route('/reservar/<int:vuelo_id>', methods=['GET', 'POST'])
def reservar(vuelo_id):
    vuelo = Vuelo.query.get(vuelo_id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        
        cliente = Cliente(nombre=nombre, email=email)
        db.session.add(cliente)
        db.session.commit()
        
        reserva = Reserva(cliente_id=cliente.id, vuelo_id=vuelo.id)
        db.session.add(reserva)
        db.session.commit()
        
        return redirect(url_for('confirmar_reserva', reserva_id=reserva.id))
    
    return render_template('reservar.html', vuelo=vuelo)

@app.route('/confirmar_reserva/<int:reserva_id>')
def confirmar_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    return render_template('confirmar_reserva.html', reserva=reserva)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
 