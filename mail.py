#!/usr/bin/python

import smtplib

def send_forgot(receiver):
	sender = "your@mail.dk"
	inbox = """
		Your Username : fird0s
		Your Password : yourpass
		"""
	header = ["From: " + sender, "Subject: Reset Your Password", "To: " + receiver, "Content-Type: text/html", inbox]

	try:
		session = smtplib.SMTP('localhost')
		session.ehlo()
		session.starttls()
		session.login('firdaus@jones.dk', '')
		session.sendmail(sender, receiver, header)
		session.quit()
	finally:		
		datauser.email = request.form["email"]	
		datauser.angkatan = request.form["angkatan"]	
		datauser.handphone = request.form["hp"]	
		datauser.work = request.form["pekerjaan"]	
		datauser.status = request.form["status"]	
