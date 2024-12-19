from flask import Flask, render_template, request, redirect, flash, abort
from dynaconf import Dynaconf

app = Flask(__name__)

conf = Dynaconf(
    settings_files = ["settings.toml"]
)



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
        return redirct ("/")
 else:


    if request.method == "POST":
           
     first_name = request.form["first_name"]
     last_name = request.form["last_name"]
    

     Email_address = request.form["Email_address"]
     Password = request.form["Password"]
     

     conn = connect_db()

     cursor = conn.cursor()
     cursor.execute(f"""
     return redirect("/sgin_in")




          INSTERT INTO 'Customer'
              ('first_name', 'last_name', 'username','email','password')
              VALUES
              ('{first_name}', '{last_name}', '{Email_address}','{Password}')
     """)
     except pymysql.err.IntegrityError:
         flash("sorry this email has already taken please try another one")
    
    return render_template("sign_up.html.jinja")






      @app.route('/cart')
      def cart 
      return "cart page "



@app.errorhandler(404)
def page_not_found(e):
return render_template('404.html.jinja'), 404

   
 