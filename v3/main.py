import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/room/create', methods=['POST'])
def room_create():
    try:        
        _json = request.json
        _name = _json['name']
        _capacity = _json['capacity']
        _start = _json['start']
        _end = _json['end']
        if _name and _capacity and _start and _end and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO room(name, capacity, start, end) VALUES(%s, %s, %s, %s)"
            bindData = (_name, _capacity, _start, _end)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Room added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
     
@app.route('/room')
def room():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, capacity, start, end FROM room")
        roomRows = cursor.fetchall()
        respone = jsonify(roomRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/room/search/<string:name>')
def room_search_name(name):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT name, capacity, start, end FROM room WHERE name =%s", name)
        roomRow = cursor.fetchone()
        respone = jsonify(roomRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/room/search/<int:capacity>/<string:by_date>')
def room_search_capacity_date(capacity, by_date):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `room` WHERE `capacity` >=%s AND `end` <=%s", [capacity, by_date])
        roomRows = cursor.fetchall()
        respone = jsonify(roomRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/room/rent', methods=['PUT'])
def room_rent():
    try:
        _json = request.json
        _id = _json['id']
        _start = _json['start']
        _end = _json['end']
        if _start and _end and _id and request.method == 'PUT':			
            sqlQuery = "UPDATE room SET start=%s, end=%s WHERE id=%s"
            bindData = (_start, _end, _id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Room booked successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_room(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM room WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('Room deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Route not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()