from flask import Flask, render_template, request, redirect, flash, abort
from dynaconf import Dynaconf
import flask_login
import pymysql

app = Flask(__name__)

conf = Dynaconf(
    settings_files = ["settings.toml"]
)

login_manger = flask_login.LoginManager()
login_manger.init_app(app)
login_manger.login_view = ('/sign_up')


class User:
    is_authenticated = True 
    is_anonymous = False 
    is_active = True



def connect_db():
    conn = pymysql.connect(
        host = "10.100.34.80",
        database = "scardenas_aureliomotors",
        user = 'scardenas',
        password = conf.password,
        autocommit = True,
        cursorclass = pymysql.cursors.DictCursor

    )

    return conn
   
@app.route("/")
def index():
    return render_template("homepage.html.jinja")


@app.route("/browse")
def product_browse():
    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM `Product` ;")

    results = cursor.fetchall()



    cursor.close()
    conn.close()


    return  render_template("browse.html.jinja", product = results)



@app.route("/product/<product_id>")
def product_page(product_id):
    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM `Product`WHERE `id` = {product_id};")



    result = cursor.fetchone()
    if result is None:
          abort(404)

    cursor.close()
    conn.close()








    return result


@app.route("/sign_up", methods=["POST","GET"])
def signup():
 if flask_login.current_user.is_authenticated:
        return redirect ("/")
 else:


    if request.method == "POST":
           
     first_name = request.form["first_name"]
     last_name = request.form["last_name"]
    

     Email_address = request.form["Email_address"]
     Password = request.form["Password"]
     
     conn = connect_db()

     cursor = conn.cursor()
     try:
        cursor.execute(f"""
                        return redirect("/sgin_in")




                INSTERT INTO 'Customer'
                    ('first_name', 'last_name', 'username','email','password')
                    VALUES
                     ('{first_name}', '{last_name}', '{Email_address}','{Password}')
         """)       
     except pymysql.error.IntegrityError:
        flash("sorry this email has already taken please try another one")
    
    return render_template("sign_up.html.jinja")






 @app.route('/cart')
 def cart():
      return "cart page "



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html.jinja'), 404

@app.route("/product/<product_id>/cart", methods=["post"])
@flask_login.login_required
def add_to_cart(product_id):
    try: 
        gty = int(request.form.get('gty',1))
    except ValueError:
        flash("invalid quantity")


#get gyt from form 
#get customer id 

#add data to the database

#bring user to cart page 

@app.route("/cartpage")
@flask_login.login_required
def cart_page(): 
    conn = connect_db()
    cursor = conn.cursor()

    customer_id = flask_login.current_user.id

    cursor.excute("SELECT  `name` , `price`, `gyt`, `image`, `product_id`, `cart`, `id` * FROM `cart_page` WHERE `customer_id` = {custmomer_id}; ")

    results = cursor.fetchall()

    cursor.close()

    conn.close()



    return render_template("cart_page.html.jinja", products=results)





   
 