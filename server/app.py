from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.order_by(Message.created_at).all():
            messages.append(message.to_dict())
        return make_response(messages)
    elif request.method == 'POST':
        params = request.json
        new_message = Message(body=params['body'], username=params['username'])

        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if message:
        if request.method == 'PATCH':
            params = request.json
            # for attr in params:
            #     setattr(message, attr, params[attr])
            message.body = params['body']
            db.session.commit()
            return make_response(message.to_dict())
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()
            return make_response('', 204)

if __name__ == '__main__':
    app.run(port=5555)