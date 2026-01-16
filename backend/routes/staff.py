from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, mail
from models import LoanApplication, User
from flask_mail import Message

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/applications", methods=["GET"])
@jwt_required()
def all_apps():
    user = get_jwt_identity()
    if user["role"] != "staff":
        return jsonify(error="Forbidden"), 403

    apps = LoanApplication.query.all()
    return jsonify([
        {"id": a.id, "status": a.status} for a in apps
    ])

@staff_bp.route("/applications/<int:id>", methods=["PATCH"])
@jwt_required()
def review(id):
    user = get_jwt_identity()
    if user["role"] != "staff":
        return jsonify(error="Forbidden"), 403

    data = request.json
    app = LoanApplication.query.get(id)
    app.status = data["status"]
    app.feedback = data["feedback"]

    student = User.query.get(app.student_id)

    msg = Message(
        "Loan Application Update",
        recipients=[student.email],
        body=f"Status: {app.status}\nFeedback: {app.feedback}"
    )
    mail.send(msg)

    db.session.commit()
    return jsonify(message="Updated")
