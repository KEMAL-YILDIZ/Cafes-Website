from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes data.db"
bootstrap = Bootstrap5(app)

db = SQLAlchemy(app)


class CafesData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), unique=True, nullable=False)
    open = db.Column(db.String(250), nullable=False)
    close = db.Column(db.String(250), nullable=False)
    coffee = db.Column(db.String(250), nullable=False)
    wifi = db.Column(db.String(250), nullable=False)
    power = db.Column(db.String(250), nullable=False)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    opening_time = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    closing_time = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee = SelectField("Coffee Rating",
                         choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi = SelectField("WIFI Strength Rating",
                       choices=["📡", "📡📡", "📡📡📡", "📡📡📡📡", "📡📡📡📡📡"], validators=[DataRequired()])
    power = SelectField("Power Socket Availability",
                        choices=["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if request.method:
        if form.validate_on_submit():
            new_cafe = CafesData(name=form.cafe.data, location=form.location.data, open=form.opening_time.data,
                                 close=form.closing_time.data, coffee=form.coffee.data, wifi=form.wifi.data,
                                 power=form.power.data)
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


@app.route('/cafes')
def cafes():
    result = db.session.execute(db.Select(CafesData).order_by(CafesData.name)).scalars()
    return render_template("cafes.html", cafes=result)


@app.route('/delete')
def delete():
    id = request.args.get("id")
    cafe_to_del = db.session.execute(db.Select(CafesData).where(CafesData.id == id)).scalar()
    db.session.delete(cafe_to_del)
    db.session.commit()
    return redirect(url_for("cafes"))


if __name__ == '__main__':
    app.run(debug=True)
