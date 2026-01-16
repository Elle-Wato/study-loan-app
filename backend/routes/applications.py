import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from extensions import db
from models import LoanApplication, Document

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app_bp = Blueprint("applications", __name__)

@app_bp.route("", methods=["POST"])
@jwt_required()
def apply():
    user = get_jwt_identity()
    app = LoanApplication(student_id=user["id"])
    db.session.add(app)
    db.session.commit()

    files = request.files.getlist("documents")
    for f in files:
        filename = secure_filename(f.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(path)

        doc = Document(application_id=app.id, filename=filename, filepath=path)
        db.session.add(doc)

    db.session.commit()
    return jsonify(message="Application submitted")
