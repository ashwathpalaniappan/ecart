from flask import Flask, request, jsonify, make_response
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
import pymysql
import smtplib
from email.message import EmailMessage
 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qwertyashwath'
app.config['MYSQL_DATABASE_DB'] = 'ecart'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/register", methods=["POST", "GET"])
@cross_origin()
def register():
    if request.method == 'POST':
        
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (name, email, password)) 
        conn.commit()
        
        data = {'name':str(name),'email':str(email),'password':str(password)}
        return jsonify(data)

@app.route("/login", methods=["POST", "GET"])
@cross_origin()
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * from accounts where email=%s and password=%s', (email, password)) 
        #conn.commit()
        account = cursor.fetchone()
        print(account)
        if account:
            data = {'name':str(account['name']),'email':str(account['email']),'password':str(account['password'])}
            return jsonify(data)
        return make_response(jsonify({'msg': "NOT FOUND"}), 400)
        # return(jsonify({'msg': "NOT FOUND"}))


@app.route("/getProducts", methods=["GET"])
@cross_origin()
def get_products():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * from products')
    account = cursor.fetchall()
    if account:
        return jsonify(account)
    return make_response(jsonify({'msg': "NOT FOUND"}), 400)

@app.route("/orders", methods=["POST", "GET"])
@cross_origin()
def orders():
    if request.method == 'POST':
        
        name = request.json['name']
        email = request.json['email']       
        add1 = request.json['add1']  
        add2 = request.json['add2']  
        city = request.json['city']  
        state = request.json['state']  
        pincode = request.json['pincode']
        order_items = request.json['order_items']
        delivery = request.json['delivery']
        sub_total = request.json['sub_total']

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('INSERT INTO orders VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )', (name, email, add1, add2, city, state, pincode, order_items, delivery, sub_total)) 
        conn.commit()
        
        data = {'name':str(name),'email':str(email)}
        return jsonify(data)


@app.route("/mailing", methods=["POST", "GET"])
@cross_origin()
def mailing():
    if request.method == 'POST':
        
        name = request.json['name']
        email = request.json['email']

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login('srinivasasiddhastores@gmail.com', 'nstxxexzlwzvizsx')

        msg = EmailMessage()
        msg.set_content(f'Hello {name}!,\n\nThank you for being our valued customer. We hope our product will meet your expectations. Let us know if you have any questions. We hope you enjoy your new purchase! And to know further updates, check with our website:\nhttp://localhost:5000\n\n\nThankyou!')

        msg['Subject'] = 'Order Placed!'
        msg['From'] = 'srinivasasiddhastores@gmail.com'
        msg['To'] = email

        s.send_message(msg)
        s.quit()

        return jsonify({'res':'mail sent'})

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)