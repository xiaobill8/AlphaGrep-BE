import logging
from flask import Flask, jsonify, request, flash
from flask_cors import CORS
import pymysql
from connection import connect

app = Flask(__name__)
cors = CORS(app)

logging.getLogger("flask_cors").level = logging.DEBUG

app.config["CORS_HEADERS"] = "Content-Type"

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


# INSERT
@app.route("/students/create-student", methods=["POST"])
def inst():
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


# GET ONE
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


# UPDATE
@app.route("/students/update-student/<name>", methods=["PUT"])
def updates(name):
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
        "Message": "Success",
    }
    resp = jsonify({"result": output})
    return resp


# # DELETE
# @app.route("/delete/<id>", methods=["DELETE"])
# def delete(id):
#     conn = connect()
#     cur = conn.cursor(pymysql.cursors.DictCursor)
#     firstname = request.json["firstname"]
#     lastname = request.json["lastname"]
#     query = "DELETE FROM FLASKMYSQL Where NameId = '" + id + "'"
#     cur.execute(query)
#     conn.commit()
#     cur.close()
#     output = {
#         "firstname": request.json["firstname"],
#         "lastname": request.json["lastname"],
#         "Message": "DELETED",
#     }
#     return jsonify({"result": output})


if __name__ == "__main__":
    app.debug = True
    app.run()


# if __name__ == "__main__":
#     app.run()
