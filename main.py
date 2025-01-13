from flask import Flask, render_template, request, redirect, flash, abort
from dynaconf import Dynaconf
import flask_login
import pymysql

conf = Dynaconf(
    settings_files = ["settings.toml"]
)

app = Flask(__name__) 
app.secret_key = conf.secret_key



login_manger = flask_login.LoginManager()
login_manger.init_app(app)
login_manger.login_view = ('/sign_up')


class User:
    is_authenticated = True 
    is_anonymous = False 
    is_active = True

    def __init__(self, user_id, username, email, first_name, last_name):
        self.id = user_id 
        self.username = username 
        self.email = email
        self.first_name = first_name 
        self.last_name = last_name

        def get_id(self):
            return str(self.id)
        

@login_manger.user_loader
def load_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM `Customer` WHERE `id` = {user_id}")

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is not None:
        return User(result["id"], result["username"], result["email"], result["first_name"], result["last_name"])
    
        



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
    
     username = request.form["username"]
     email = request.form["email"]


     password = request.form["password"]
     confirmpassword = request.form["confirmpassword"]

     if len(password) < 12:
         flash("Your password must be atleast 12 characters")
         return render_template("sign_up.html.jinja")
     conn = connect_db()

     cursor = conn.cursor()
     try:
        cursor.execute(f"""
                INSERT INTO `Customer`
                    (`first_name`, `last_name`, `username`, `email`, `password`)
                VALUES
                     ('{first_name}', '{last_name}', '{email}','{password}','{username}')
         """)       
     except pymysql.err.IntegrityError:
        flash("sorry this email has already taken please try another one")
     else:
         return redirect("/signin")
     finally:
         cursor.close()
         conn.close()
    
    return render_template("sign_up.html.jinja")







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





@app.route('/cart')
def cart():
    return render_template('cart_page.html.jinja')
    # @app.route('/cart/<cart_id>/del", method=["POST"])
    #            @flask_login.login_required
    #            def delete_cart(cart_id):
               
    #            conn = connect_db

    #            cursor = conn.cursor()


    @app.route("/products/<product_id>/reviews", methods=['POST'])
    @flask_login.login_required
    def review():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"""
                    
""")


    