import pymysql
from app import app
from connection import connect
from flask import jsonify, request, flash


# GET ALL
@app.route("/students", methods=["GET"])
def students():
    try:
        conn = connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        print(rows)
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


# # GET ONE
# @app.route("/select/<id>", methods=["GET"])
# def userone(id):
#     try:
#         conn = connect()
#         cur = conn.cursor(pymysql.cursors.DictCursor)
#         cur.execute("SELECT * FROM FlaskMysql WHERE NAMEID =" + id)
#         rows = cur.fetchall()
#         resp = jsonify(rows)
#         resp.status_code = 200
#         return resp
#     except Exception as e:
#         print(e)
#     finally:
#         cur.close()
#         conn.close()


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

    return jsonify({"result": output})


# Update
@app.route("/students/update-student/<name>", methods=["PUT"])
def updates(name):
    conn = connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    password = request.json["password"]
    classId = request.json["class"]
    query = f"UPDATE student SET Password = {password}, Class = {classId} WHERE Name = {name})"
    cur.execute(query)
    conn.commit()
    cur.close()
    output = {
        "name": name,
        "password": password,
        "Message": "Success",
    }

    return jsonify({"result": output})


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
