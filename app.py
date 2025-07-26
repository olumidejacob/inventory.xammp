from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
if __name__== "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1",port=5000)
app.secret_key = 'some_random_data'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "inventory"

mysql = MySQL(app)
@app.route('/')
def landing():
    return render_template('landpage.html')

@app.route('/sell')
def sell():
    return render_template('sellingpage.html',)

@app.route('/home')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM softdrinktbl")
    data = cursor.fetchall()
     cursor.execute("SELECT * FROM snacks"
    item = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('index.html', drinks=data, snack=item)


@app.route('/insert_drink', methods=['POST'])
def insert_drink():
    if request.method == 'POST':
        name = request.form['name_of_drink']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        drink_subtype = request.form['drink_subtype']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO softdrinktbl (name_of_drink, price, quantity, expiry_date, batch_number, drink_subtype) VALUES (%s, %s, %s, %s, %s, %s)", (name, price, quantity, expiry_date, batch_number, drink_subtype))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('Index'))
        
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    cursor = mysql.connection.cursor()

    if request.method == "POST":
        name = request.form['name_of_drink']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor.execute("""
            UPDATE drinks_inventory
            SET name_of_drink = %s, price = %s, quantity = %s, expiry_date = %s, batch_number = %s, subtype = %s
            WHERE ID = %s
        """, (name, price, quantity, expiry_date, batch_number, subtype, id))

        mysql.connection.commit()
        cursor.close()
        flash(f"{name} updated successfully!", "success")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM drinks_inventory WHERE ID = %s", (id,))
    drink = cursor.fetchone()
    cursor.close()
    return render_template("UPDATEON_DRINKS_INVENTORY.HTML", drink=drink)

@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM drinks_inventory WHERE ID = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Drink deleted successfully!", "success")
        return redirect(url_for('index'))


@app.route('/insert_snack', methods=['POST'])
def insert_snack():
     if request.method == 'POST':
        name = request.form['name_of_item']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form["expiry_date"]
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM snacks WHERE name_of_item = %s",
                       (name,))
        existing = cursor.fetchone()

        if existing:
            flash(f"{name} already exists!", "warning")
            cursor.close()
            return redirect(url_for('index'))
        
        cursor.execute("INSERT INTO snack (name_of_item, price, quantity, expiry_date, batch_number, subtype) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, price,quantity, expiry_date, batch_number, subtype))
        mysql.connection.commit()
        cursor.close()
        flash(f"{name} added successfully!", "success")
        return redirect(url_for('index'))

@app.route("/delete_snack/<int:id>", methods=["GET"])
def delete_snack(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM beverages WHERE ID = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        flash("snack deleted successfully!", "success")
        return redirect(url_for('index'))


@app.route('/edit_snack/<int:id>', methods=['GET', 'POST'])
def edit_snack(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name_of_item']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        subtype = request.form['subtype']

        cursor.execute(""" UPDATE beverages
                        SET name_of_item = %s, price = %s, quantity =%s, expiry_date = %s, batch_number = %s, subtype = %s
                         WHERE ID = %s
                     """, (name, price, quantity, expiry_date, batch_number, subtype, id))
        mysql.connection.commit()
        cursor.close()
        flash(f"{name} updated successfully!", "success")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM beverages WHERE ID = %s", (id,))
    item = cursor.fetchone()
    cursor.close()
    return render_template("snacks.html", snack=item)

    

if __name__ == '__main__': 
    app.run(debug=True) 