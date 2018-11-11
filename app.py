from flask import Flask, render_template , flash , request
import os
from wtforms import Form, TextField , TextAreaField , validators, StringField, SubmitField, FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug import secure_filename

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ResuableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    customer_id = TextField('Customer_id:',validators=[validators.required(), validators.Length(min=6, max=35)])
    photo = FileField(validators=[FileRequired()])


@app.route("/", methods=['GET', 'POST'])
#@app.route('/upload', methods=['GET', 'POST'])
def hello():

    form = ResuableForm(request.form)

    print(form.errors)

    if request.method == 'POST':
        name = request.form['name']
        customer_id = request.form['customer_id']
        photo = request.form['photo']

        if form.validate():
            flash('Hello ' + name)
            f = form.photo.data()
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                app.instance_path, 'photos', filename
            ))
            #filename = secure_filename(form.file.data.filename)
            #form.file.data.save('index' + filename)
            #flash('Hello %s , now please upload the customer id and upload the valid document to complete the KYC ' % name)
    else:
        flash('All the form fields are required. ')
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)