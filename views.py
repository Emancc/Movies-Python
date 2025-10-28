from flask.views import View

class UserView(View):
    def get(self):
        return jsonify({'message': 'Hello World'})
