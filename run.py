from flask import Flask, url_for, redirect, render_template, request, session, abort, escape
from models import *
sman2 = Flask(__name__)
import os, random
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import time

@sman2.route('/',  methods=['GET', 'POST'])
def index():
	get_user = session.get("user", None)
	abc = "fird0s"
	if "user" in session:
		auth=True
	else:
		auth=False		
	all_user = session_db.query(Users).all()[0:50]
	session_db.close()
	return render_template("index.html", all_user=all_user, auth=auth, get_user=get_user, abc=abc)


@sman2.route('/contact/',  methods=['GET', 'POST'])
def contact():
	if request.method == "POST":
		if request.form["contact-name"] and request.form["contact-email"] \
		   and request.form["contact-hp"] and request.form["contact-message"]:			
			
			contact = Contact(request.form["contact-name"], request.form["contact-email"], \
							  request.form["contact-hp"], request.form["contact-message"])
			session_db.add(contact)
			session_db.commit()
			session_db.close()
			return "thanks <b> %s</b> was send me a message :)" % request.form["contact-name"]		  
		else:
			return "All input form is required."
	else:
		return redirect(url_for('index')) 		
	return render_template("index.html")


@sman2.route('/register/', methods=["POST", "GET"])
def register():
	if request.method == "GET":
		return redirect(url_for('index'))

	if request.method == "POST":
		token = session.pop('_csrf_token', None)
		if not token or token != request.form.get('_csrf_token'):
		    	abort(403)
		if request.form["rg-name"] and request.form["rg-fullname"] and request.form["rg-mail"] and \
		   request.form["rg-password"]:
			try:
				user = Users(request.form["rg-name"], request.form["rg-fullname"], request.form["rg-password"], \
			    	         request.form["rg-mail"], request.form["rg-angkatan"], request.form["rg-hp"], "", request.remote_addr, "user")
				session_db.add(user)
				session_db.commit()
				session_db.close()
				return "thanks for register"
				
			except sqlalchemy.exc.IntegrityError:
				return "Sorry username or email alredy use"
				
			except sqlalchemy.exc.InvalidRequestError:
				session_db.rollback()
				session_db.close()
		else:
			return "All input form is required"	             
	
	return render_template("index.html")		
	
def generate_csrf_token(): 
    if '_csrf_token' not in session:
        session['_csrf_token'] = random.getrandbits(128)
    return session['_csrf_token']
    
sman2.jinja_env.globals['csrf_token'] = generate_csrf_token  	
	
@sman2.route('/user/<show_profil>')
def profile(show_profil):
	get_user = session.get("user", None)
	if "user" in session:
		auth=True
	else:
		auth=None
	try:
		profil_data = session_db.query(Users).filter_by(username = show_profil).one()
	except sqlalchemy.orm.exc.NoResultFound:
		log = Log(request=request.url, ip=request.remote_addr)
		session_db.add(log)
		session_db.commit()
		session_db.close()
		return redirect(url_for('index'))
	return render_template("details.html", profil_data=profil_data, auth=auth, get_user=get_user)


@sman2.route('/user/',  methods=['GET', 'POST'])
def user():
	if request.method == "POST":
		if request.form["user-login"] and request.form["user-password"]:
			try:
				check = session_db.query(Users).filter_by(username = request.form["user-login"]).one()
				if check.password == request.form["user-password"]:
					session['user'] = request.form['user-login']
					
					return redirect(url_for('profile', show_profil=check.username))
					session_db.close()	
				else: 
					return "your password is wrong"	
			except sqlalchemy.orm.exc.NoResultFound:	
				return "Your Username is wrong"
	if "user" in session:
		return "you logged as %s" % session['user']			
	return render_template("user.html", check=check)

@sman2.route('/admin/', methods=["GET", "POST"])
def admin():
	if "admin" in session:
		auth_admin=True
	else:
		auth_admin=False
	if request.method == "POST":
		if request.form["admin-user"] == "masuk" and request.form["admin-pass"] == "masuk":
			session['admin'] = "admin"
	all_log = all_log = session_db.query(Log).all()[0:20]
	all_log.reverse()		
	all_contact = session_db.query(Contact).all()[0:20]
	all_contact.reverse()
	all_user = session_db.query(Users).all()[0:20]
	all_user.reverse()
	return render_template("admin.html", auth_admin=auth_admin, all_log=all_log, all_contact=all_contact, all_user=all_user)
	
@sman2.route('/admin/contact/', methods=["GET", "POST"])	
def admincontact():
	if "admin" not in session:
		return redirect(url_for("admin"))
	all_contact = session_db.query(Contact).all()
	return render_template("admin-contact.html", all_contact=all_contact)

@sman2.route("/admin/contact/<int:hapus>/")
def contact_delete(hapus): 
	try:
		delete_contact = session_db.query(Contact).filter_by(id = hapus).one()	
		session_db.delete(delete_contact)
		session_db.commit()
		session_db.close()
	except sqlalchemy.orm.exc.NoResultFound:
		return "<script>alert('No data');</script>"
	return redirect(url_for("admincontact"))		
	
@sman2.route("/admin/user/")
def admin_user():
	if "admin" not in session:
		return redirect(url_for("admin"))
	all_user = session_db.query(Users).all()
	return render_template("admin-user.html", all_user=all_user)	
	
@sman2.route("/admin/user/delete/<int:hapus>")
def admin_user_delete(hapus):
	if "admin" not in session:
		return redirect(url_for("admin"))
	try:
		action = session_db.query(Users).filter_by(id = hapus).one()
		session_db.delete(action)
		session_db.commit()
		session_db.close()
		return redirect(url_for("admin_user"))
	except sqlalchemy.orm.exc.NoResultFound:
		return redirect(url_for("admin_user"))		
	return redirect(url_for("admin_user"))

@sman2.route("/admin/user/edit/<int:edit>/", methods=["GET", "POST"])
def admin_user_edit(edit):
	if "admin" not in session:
		return redirect(url_for("admin"))
	action = session_db.query(Users).filter_by(id = edit).one()
	if request.method == "POST":	
		try:
			action.username = request.form["edit-username"]
			action.fullname = request.form["edit-fullname"]
			action.email = request.form["edit-email"]
			action.handphone = request.form["edit-handphone"]
			action.angkatan = request.form["edit-angkatan"]
			action.work = request.form["edit-pekerjaan"]
			session_db.add(action)
			session_db.commit()
			session_db.close() 
			session.pop("user", None)
			session['user'] = request.form['edit-username']
			return redirect(url_for("admin_user"))
		except sqlalchemy.exc.IntegrityError:
			return "Your Email or Username alredy use"	
	return render_template("admin_user_edit.html", action=action)				
	
@sman2.route("/search/")
def search():
	get_user = session.get("user", None)
	if "user" in session:
		auth=True
	else:
		auth=None
	if request.method == "GET":
		if request.args.get("search-name", ""):
			nama = request.args.get("search-name", "")
			get_fullname = session_db.query(Users).filter(Users.fullname.like("%"+request.args.get("search-name", "")+"%"))
		else:
			return "Anda Belom Mengiisikan Nama."	
	return render_template("search.html", get_fullname=get_fullname, nama=nama, auth=auth, get_user=get_user)

@sman2.route("/edit/", methods=['GET', 'POST'])
def edit_user():
	if "user" in session:
		auth=True
	else:
		auth=None
	get_user = session.get("user", None)	
	profile = session_db.query(Users).filter_by(username = get_user).one()
	if request.method == "POST":
		try:	
			profile.fullname = request.form["edit-fullname"]
			profile.email = request.form["edit-email"]
			profile.handphone = request.form["edit-handphone"]
			profile.angkatan = request.form["edit-angkatan"]
			profile.work = request.form["edit-pekerjaan"]
			session_db.add(profile)
			session_db.commit()
			session_db.close()
			return redirect(url_for("edit_user"))
		except sqlalchemy.exc.IntegrityError:
			return "please <b>%s</b> alredy used by other people !"  % (request.form["edit-email"])
	return render_template("edit_user.html", auth=auth, get_user=get_user, profile=profile)

#@sman2.route("/admin/log-error/")
#def log_error():
#	if "admin" not in session:
#		return redirect(url_for("admin"))
#	all_log = session_db.query(Log).all()[0:1000]
#	all_log.reverse()
#	session_db.close()
#	return render_template("log.html", all_log=all_log)

@sman2.route('/angkatan/<cari_angkatan>/', methods=["POST", "GET"])
def angkatan(cari_angkatan):
	if "user" in session:
		auth=True
	else:
		auth=None
	get_user = session.get("user", None)	
	get_fullname = session_db.query(Users).filter_by(angkatan = cari_angkatan).all()
	angkatan = cari_angkatan
	return render_template("angkatan.html", auth=auth, get_user=get_user, get_fullname=get_fullname, angkatan=angkatan)

@sman2.route('/logout/', methods=["POST", "GET"])
def logout():
	if not "user" in session:
		return redirect(url_for("index"))
	get_user = session.get("user", None)
	profil_data = session_db.query(Users).filter_by(username = get_user).one()
	profil_data.ip = request.remote_addr
	session_db.add(profil_data)
	session_db.commit()
    	session_db.close()
	session.pop("user", None)
	return redirect(url_for('index'))


@sman2.route('/forgot/', methods=["POST", "GET"])
def forgot():
	if request.method == "POST":
		if request.form["forgot-password"]:
			try:
				reset = session_db.query(Users).filter_by(email = request.form["forgot-password"]).one()
				return "<p class='alert alert-success'><b>Well done</b> | Password has been sent to your mail.</p>"
			except sqlalchemy.orm.exc.NoResultFound:	
				return "<p class='alert alert-error'><b>ERROR</b> | Your email does not exist.</p>"
				  
	return render_template("forgot.html")

@sman2.errorhandler(404)
def not_found(error):
	log = Log(request=request.url, ip=request.remote_addr, time=datetime.now(), referer=request.referrer)
	session_db.add(log)
	session_db.commit()
	session_db.close()
	return redirect(url_for('index'))

@sman2.route("/test", methods=["GET", "POST"])
def test():
	if request.method == "POST":
		if request.form["test-text"]:
			return "hello"
	return request.query_string

if __name__ == "__main__":
	sman2.secret_key = '_Wx0ksck~\[p99923@#@!#!@#423raakleas'
	sman2.debug = True
	sman2.run()

