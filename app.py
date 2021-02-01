from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'assurancevie'
mysql = MySQL(app)

@app.route('/',methods=['GET', 'POST'])
def home():
    cur = mysql.connection.cursor()
    cur.execute("USE assurancevie")  # select the database
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'base table' AND table_schema= 'assurancevie'")
    mysql.connection.commit()
    tables = cur.fetchall()
    cur.close()

    return render_template("dbinfo.html", data=tables)




@app.route('/addcol/<string:tname>', methods=['GET', 'POST'])
def addcol(tname):
    if request.method== 'POST':
        cur = mysql.connection.cursor()
        cur.execute("ALTER table " +tname+" add column "+request.form['fname']+" "+request.form['type']+"("+request.form['leng']+") NOT NULL")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home") )
    return render_template("addcolumn.html", data=tname)
@app.route('/addrow/<string:tname>', methods=['GET', 'POST'])
def addrow(tname):
    if request.method=='POST':
        cur = mysql.connection.cursor()
        cur.execute(request.form['quer'])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'assurancevie' AND TABLE_NAME = '" +tname+"'")

    mysql.connection.commit()
    columns = cur.fetchall()
    cur.close()
    return render_template("addrow.html",data=columns)
@app.route('/drop/<string:tname>', methods=['GET', 'POST'])
def drop(tname):

    cur = mysql.connection.cursor()
    cur.execute(
        "drop table " +tname)
    mysql.connection.commit()
    table = cur.fetchall()
    cur.close()
    return redirect(url_for("home"))
@app.route('/data/<string:tname>', methods=['GET', 'POST'])
def data(tname):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'assurancevie' AND TABLE_NAME = '" + tname + "'")

    mysql.connection.commit()
    columns = cur.fetchall()
    nbcol=cur.rowcount
    cur.close()
    dt = mysql.connection.cursor()
    dt.execute("SELECT * FROM   " + tname)

    mysql.connection.commit()
    datas = dt.fetchall()
    dt.close()
    return render_template("datadisplay.html", data=columns,rows=datas,nbc=nbcol,table=tname)
@app.route('/droprow/<string:table>/<string:row>', methods=['GET', 'POST'])
def droprow(table,row):
    print("hii")
    cur = mysql.connection.cursor()
    cur.execute("delete from "+table+" where id="+row)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('data',tname=table))

if __name__ == '__main__':
    app.run(debug=True)
