import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from connection import connect
import csv

app = Flask(__name__)
cors = CORS(app, resources={r"/students/*": {"origins": "*"}})
cors = CORS(app, resources={r"/scores/*": {"origins": "*"}})
cors = CORS(app, resources={r"/top-students": {"origins": "*"}})

logging.getLogger("flask_cors").level = logging.DEBUG

# GET ALL STUDENTS
@app.route("/students", methods=["GET"])
def students():
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


@app.route("/scores", methods=["GET"])
def students():
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM score")
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# GET ALL STUDENTS
@app.route("/top-students", methods=["GET"])
def top_students():
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        sql_query = """
            SELECT Name, Password, Class, Subject, Score from (
                SELECT Student.Name, Student.Password, Student.Class, Score.Subject, Score.Score,
                    @Subject_rank := IF(@current_Subject = Score.Subject, @Subject_rank + 1, 1)
                    AS Subject_rank,
                    @Subject_rank := Score.Subject
                FROM Student 
                INNER JOIN Score ON Student.Name=Score.Name
                ORDER BY Score.Subject, Score.Score desc ) ranked_rows
            WHERE Subject_rank <= 2
        """
        cur.execute(sql_query)
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# Insert Student
@app.route("/students/create-student", methods=["POST"])
def inst():
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        name = request.json["name"]
        password = request.json["password"]
        classId = request.json["class"]
        query = f"insert into student (Name, Password, Class) values ('{name}', '{password}', '{classId}')"
        cur.execute(query)
        conn.commit()
        cur.close()
        output = {
            "name": name,
            "password": password,
            "class": classId,
            "Message": "Success",
        }
        resp = jsonify({"result": output})
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# Add Score
@app.route("/scores/add-score", methods=["POST"])
def inst():
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        name = request.json["name"]
        subject = request.json["subject"]
        score = request.json["score"]
        query = f"insert into score (Name, Subject, Score) values ('{name}', '{subject}', '{score}')"
        cur.execute(query)
        conn.commit()
        cur.close()
        output = {
            "name": name,
            "subject": subject,
            "score": score,
            "Message": "Success",
        }
        resp = jsonify({"result": output})

        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# Upload students CSV
@app.route("/students/upload-csv", methods=["POST"])
def upload():
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        form_dict = request.form.to_dict()
        str_file_value = form_dict.get("csvInput")
        file_t = str_file_value.splitlines()
        csv_reader = csv.reader(file_t, delimiter=",")
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            query = f"insert into student (Name, Password, Class) values ('{row[0]}', '{row[1]}', '{row[2]}')"
            cur.execute(query)
            conn.commit()
        output = {
            "Message": "Success",
        }
        resp = jsonify({"result": output})
        resp.status_code = 200
        return resp
    except Exception as e:
        # TODO: Return error resp to FE
        print(e)
    finally:
        cur.close()
        conn.close()


# Upload scores CSV
@app.route("/scores/upload-csv", methods=["POST"])
def upload():
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        form_dict = request.form.to_dict()
        str_file_value = form_dict.get("csvInput")
        file_t = str_file_value.splitlines()
        csv_reader = csv.reader(file_t, delimiter=",")
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            query = f"insert into score (Name, Subject, Score) values ('{row[0]}', '{row[1]}', '{row[2]}')"
            cur.execute(query)
            conn.commit()
        output = {
            "Message": "Success",
        }
        resp = jsonify({"result": output})
        resp.status_code = 200
        return resp
    except Exception as e:
        # TODO: Return error resp to FE
        print(e)
    finally:
        cur.close()
        conn.close()


# Get one student
@app.route("/students/update-student/<name>", methods=["GET"])
def userone(name):
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(f"SELECT * FROM student WHERE Name = '{name}'")
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# Get one score
@app.route("/scores/update-score/<name>/<subject>", methods=["GET"])
def userone(name, subject):
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(
            f"SELECT * FROM score WHERE Name = '{name}' AND Subject = '{subject}'"
        )
        rows = cur.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# UPDATE
@app.route("/students/update-student/<name>", methods=["PUT"])
def updates(name):
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        password = request.json["password"]
        classId = request.json["class"]
        query = f"UPDATE student SET Password = '{password}', Class = '{classId}' WHERE Name = '{name}'"
        cur.execute(query)
        conn.commit()
        cur.close()
        output = {
            "name": name,
            "password": password,
            "class": classId,
            "Message": "Success",
        }
        resp = jsonify({"result": output})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# UPDATE
@app.route("/scores/update-score/<name>/<subject>", methods=["PUT"])
def updates(name, subject):
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        score = request.json["score"]
        query = f"UPDATE student SET Score = '{score}' WHERE Name = '{name}' AND Subject = '{subject}'"
        cur.execute(query)
        conn.commit()
        cur.close()
        output = {
            "name": name,
            "subject": subject,
            "score": score,
            "Message": "Success",
        }
        resp = jsonify({"result": output})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# DELETE
@app.route("/students/delete-student/<name>", methods=["DELETE"])
def delete(name):
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        query = f"DELETE FROM student WHERE Name = '{name}'"
        cur.execute(query)
        conn.commit()
        output = {
            "name": name,
            "Message": "DELETED",
        }
        resp = jsonify({"result": output})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# DELETE
@app.route("/scores/delete-score/<name>/<subject>", methods=["DELETE"])
def delete(name, subject):
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        query = f"DELETE FROM student WHERE Name = '{name}' AND Subject = '{subject}"
        cur.execute(query)
        conn.commit()
        output = {
            "name": name,
            "Message": "DELETED",
        }
        resp = jsonify({"result": output})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    app.debug = True
    app.run()


# if __name__ == "__main__":
#     app.run()
