from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veritabani.db'
db = SQLAlchemy(app)


class Veri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    car_model = db.Column(db.String(50))
    car_km = db.Column(db.Integer)
    car_year = db.Column(db.Integer)
    phone_number = db.Column(db.String(20))


def create_table():
    with app.app_context():
        db.create_all()


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        car_model = request.form['car_model']
        car_km = request.form['car_km']
        car_year = request.form['car_year']
        phone_number = request.form['phone_number']

        veri = Veri.query.filter_by(id=id).first()
        veri.first_name = first_name
        veri.last_name = last_name
        veri.car_model = car_model
        veri.car_km = car_km
        veri.car_year = car_year
        veri.phone_number = phone_number

        db.session.commit()

        return redirect('/veriler')

    veri = Veri.query.get(id)
    return render_template('edit.html', veri=veri)


@app.route('/delete/<int:id>')
def delete(id):
    veri = Veri.query.get(id)
    db.session.delete(veri)
    db.session.commit()

    return redirect('/veriler')


@app.route('/details/<int:id>')
def details(id):
    veri = Veri.query.get(id)
    return render_template('details.html', veri=veri)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        car_model = request.form['car_model']
        car_km = request.form['car_km']
        car_year = request.form['car_year']
        phone_number = request.form['phone_number']

        yeni_veri = Veri(first_name=first_name, last_name=last_name, car_model=car_model, car_km=car_km,
                         car_year=car_year, phone_number=phone_number)
        db.session.add(yeni_veri)
        db.session.commit()

        return redirect('/veriler')

    return render_template('index.html')


@app.route('/veriler')
def veriler():
    veriler = Veri.query.all()

    return render_template('data.html', veriler=veriler)


if __name__ == '__main__':
    create_table()
    app.run()
