from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import psycopg2
import uuid

import csv

def getConn():
    conn = psycopg2.connect(
        host="ec2-52-87-107-83.compute-1.amazonaws.com",
        database="de3l9vv4et8h54",
        user="xlimixfjzdzbyg",
        password="28d55dcf38e3c118db590ff0db40f9f46ff7d4eec3eae45c05571b8385265e89");
    return conn;
    
app = Flask(__name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates')


@app.route('/')
@app.route('/Index')
def main_page():
    conn = getConn();
    cur = conn.cursor();
    
    cur.execute("SELECT * FROM colorname");
    records = cur.fetchall()
    
    cur.close();

    return render_template('Index.html', names=records);

@app.route('/delete', methods=['POST', 'GET'])
def delete_page():
    conn = getConn();
    cur = conn.cursor();
    sql = """DELETE FROM colorname WHERE cn_id = %s;"""
    color_id = request.args.get('id');
    
    result = cur.execute(sql, (color_id,));
    conn.commit();
    cur.close;

    return main_page();
    
@app.route('/add')
def add_page():
    return render_template('Add.html');
    
@app.route('/insert', methods=['POST', 'GET'])
def add_insert_page():
    conn = getConn();
    cur = conn.cursor();
    sql = """INSERT INTO colorname(cn_id, color_name, color_hex, color_r, color_g, color_b)
             VALUES(%s, %s, %s, %s, %s, %s);"""
    color_id = str(uuid.uuid1());
    color_name = request.args.get('color_name');
    color_color = request.args.get('color_color');
    r = int(color_color[1:3], 16);
    g = int(color_color[3:5], 16);
    b = int(color_color[5:7], 16);
    
    result = cur.execute(sql, (color_id, color_name,color_color, r, g, b));
    conn.commit();
    cur.close;
    return main_page();

@app.route('/defaultColorInsertion')
def insert_all():
    with open('colors.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        conn = getConn();
        cur = conn.cursor();
        sql = """INSERT INTO colorname(cn_id, color_name, color_hex, color_r, color_g, color_b)
                 VALUES(%s, %s, %s, %s, %s, %s);"""
        
        for row in csv_reader:
            print(str(row));
            color_id = str(row[0]);
            color_name = str(row[1]);
            color_color = str(row[2]);
            r = row[3];
            g = row[4];
            b = row[5];
            line_count += 1;
            result = cur.execute(sql, (color_id, color_name, color_color, r, g, b));
            conn.commit();
        cur.close;
        print(f'Processed {line_count} lines.')    
    return render_template('Add.html');

@app.route('/download')
def download():
    conn = getConn();
    cur = conn.cursor();
    cur.execute("SELECT * FROM colorname");
    records = cur.fetchall()
    csvStrings= []
    for csvLine in records:
        csvStrings += [csvLine[0] + ",\"" +csvLine[1] + "\"," +csvLine[2] + "," + str(csvLine[3]) + "," + str(csvLine[4]) + "," +str(csvLine[5])];
    response = make_response("\n".join(csvStrings));
    response.headers['Content-Disposition'] = "attachment; filename=colors.csv"
    conn.close();
    return response;