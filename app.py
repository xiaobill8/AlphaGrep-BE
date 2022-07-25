from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route("/")
# @app.route("/index")
# def index():
#     return "Hello, World!"


# if __name__ == "__main__":
#     app.debug = True
#     app.run()


# @app.route("/")
# def main():
#     students = []
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM students")
#     for row in cursor.fetchall():
#         students.append({"name": row[0], "password": row[1], "class": row[2]})
#     conn.close()
#     return render_template("studentlist.html", students=students)


# if __name__ == "__main__":
#     app.run()
