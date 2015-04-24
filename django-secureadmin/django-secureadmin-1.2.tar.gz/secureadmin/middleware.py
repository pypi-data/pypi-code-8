# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from secureadmin.models import SecureAdmin 
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response,redirect
from datetime import datetime
from random import randint
from django.conf import settings
from django.template import Template,Context


class ipcheck(object):
    def process_request(self,request):
          if request.user.is_authenticated() :
	       errorcode = False
	       setattr(request, '_dont_enforce_csrf_checks', True)
	       if request.POST.get("code") :
		    userscode = SecureAdmin.objects.filter(user_id=request.user.id)
		    code = request.POST.get("code")
		    for usercode in userscode :
		        dbcode = usercode.ipcode
		        if code == dbcode :
	                    userip = request.META["REMOTE_ADDR"]
                            ip = userip.split('.')
                            ipnow = usercode.ip,ip[0]+'.'+ip[1]
			    update = SecureAdmin.objects.filter(user_id=request.user.id).update(ip=ipnow,ipmail="f",ipcode="f")
		        else :
			    errorcode = True
		  
               path = request.get_full_path()
               logout = getattr(settings, 'SECUREADMIN_LOGOUTURL', '/logout')
               if not logout in path :
	           userid = request.user.id
                   users = SecureAdmin.objects.all().filter(user_id=userid)
		   if not users :
                        userip = request.META["REMOTE_ADDR"]
                        ipuser = userip.split('.')
                        ipnow = ipuser[0]+'.'+ipuser[1]
		 	update = SecureAdmin.objects.create(ip=ipnow,user_id=request.user.id,ipmail="f",ipcode="f")
		   for user in users :
                      if user and user.ip:
                          userip = request.META["REMOTE_ADDR"]
                          ipuser = userip.split('.')
                          ipnow = ipuser[0]+'.'+ipuser[1]
		          if not str(ipnow) in str(user.ip) :
			      if not user.ipmail == "t" :
				  date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
				  code = randint(999999999999999,9999999999999999)
				  mailtext = """\
Hi ,

-------------
Login Details :
Date : {{date}}
IP : {{ip}}
-------------
If You :
Login Code : {{code}}
"""
				  smailtext2 = getattr(settings, 'SECUREADMIN_MAILBODY', mailtext)
				  smailtext3 = Template(smailtext2)
                                  smailtext = smailtext3.render(Context({'date': date,'code': code,'ip': userip}))
				  smailsubject = getattr(settings, 'SECUREADMIN_MAILSUBJECT', "Unusual sign in attempt prevented")
				  smailfrom = getattr(settings, 'SECUREADMIN_MAILFROM', "Security <secure@localhost>")
				  send_mail(smailsubject,smailtext,(smailfrom),[request.user.email])
				  update = SecureAdmin.objects.filter(user_id=userid).update(ipmail="t",ipcode=code)
				  testip = SecureAdmin.objects.filter(user_id=request.user.id)
				  for test in testip :
					if len(test.ip) >= 800:
						updatedb = SecureAdmin.objects.filter(user_id=request.user.id).update(ip="null")
			      stemplate = getattr(settings, 'SECUREADMIN_TEMPLATE', "locked")
                              return render(request,stemplate,{'ipnow': ipnow,'errorcode': errorcode})
    	  return

