from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Note {self.id} {self.title}>"

@app.route('/')
def index():
    notes = Note.query.order_by(Note.id.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title or not description:
            flash('Title and Description are required.', 'error')
            return render_template('form.html', note={'title': title, 'description': description}, action='Add')

        note = Note(title=title, description=description)
        db.session.add(note)
        db.session.commit()
        flash('Record added successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', note={}, action='Add')

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title or not description:
            flash('Title and Description are required.', 'error')
            return render_template('form.html', note=note, action='Edit')

        note.title = title
        note.description = description
        db.session.commit()
        flash('Record updated successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', note=note, action='Edit')

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Record deleted successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)