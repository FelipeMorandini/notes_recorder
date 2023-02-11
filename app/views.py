import json
from app import db
from .models import Note
from flask_login import login_required, current_user
from flask import Blueprint, flash, jsonify, render_template, request

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is empty!', category='error')
        else:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', category='success')
        
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    note = Note.query.get(note_id)
    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})