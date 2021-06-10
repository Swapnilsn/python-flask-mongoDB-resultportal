from flask import Flask , render_template ,request
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os


app=Flask("myapp")
client = MongoClient('mongodb://127.0.0.1:27017')

mydb = client["student_db"]
mycol = client["result"]

@app.route('/adlogin')
def adhome():
    return render_template('adlogin.html')


@app.route('/adlogin', methods=['POST'])
def do_admin_login():
    if request.form['password'] == '12345' and request.form['username'] == 'admin':
      return render_template('register.html')
    else:
         message = 'Please login to your account'
        
         return adhome()


#Home page
@app.route("/")
def main():
  return render_template("dashboard.html")  


@app.route("/logout")
def logout():
  return main()


@app.route("/checkresult")
def home():
  return render_template("index.html")  



# admin added record 
@app.route("/register",methods =['POST', 'GET'])
def auth():
    return render_template('register.html')



@app.route("/submit", methods=['POST'])
def upload():
    if request.method == 'POST':

        name = request.form.get("name")
        rollno = request.form.get("rollno")
        mobile= request.form.get("mobile")
       
        phym= request.form.get("physics")
        chm= request.form.get("chemistry")
        mthm= request.form.get("maths")
        

        values=[{
                    "name"	:name,
                    "phone" :mobile,
                    "rollno":(rollno),
                    
                   
                    "marks" : {
                                "physics":int(phym),
                                 "maths":int(mthm),
                                "chemistry":int(chm)
                                
                              }
                }]
        
        client['student_db']['result'].insert_many(values)

        return render_template("registerc.html",uname=name)
       
              

@app.route("/result")
def result():
    if request.method == "GET":
        name=request.args.get("name")
        roll=request.args.get("roll")
        result =client['student_db']['result'].find({"name" : name , "rollno" :(roll)} )

        if result.count() == 0:
            return render_template("index.html")

        for i in result:
            namer=(i['name'])
            rollr=(i['rollno'])
            physics=(i['marks']['physics'])
         
            maths=(i['marks']['maths'])
            chemistry=(i['marks']['chemistry'])
           
        
            total=physics+maths+chemistry
            per=(int(total)/int(300))*100
            per=round(per)
            formrender=render_template(
                "result.html" ,name=namer, roll=rollr, phy=str(physics) , 
                chem=str(chemistry) ,mth=str(maths) , tot=str(total) , percent=str(per)
            )
            output="Marks obtained by " + name + " are : " + str(total) + "percentage = " + str(per)
            return formrender
            
app.secret_key = os.urandom(12)
app.run(debug=True)


