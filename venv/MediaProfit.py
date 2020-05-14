import tableauserverclient as TSC
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import date
import datetime
import os

    # ----------------------- UTILS ---------------------------------

def getWorkbookByName(server, wb_name):
    workbooks = [x for x in TSC.Pager(server.workbooks) if x.name == wb_name]
    return None if len(workbooks) == 0 else workbooks.pop()

def getUserListByGroup(server, group_name):
    groups = [x for x in TSC.Pager(server.groups) if x.name == group_name]
    return None if len(groups) == 0 else groups.pop()

def getViewByWbId(server, wbId, viewName):
     views = [x for x in TSC.Pager(server.views) if (x.workbook_id == wbId and x.name == viewName)]
     return None if len(views) == 0 else views.pop()

# TableauAdminPass = os.environ.get("TableauAdminPass")
# tableau_auth = TSC.TableauAuth('admin', TableauAdminPass)
tableau_auth = TSC.TableauAuth('admin', 'xqKE4ynYHzoGCiVwPWsBGZrT')
server = TSC.Server('https://tableau.naturalint.com',use_server_version=True)

with server.auth.sign_in(tableau_auth):
    view_item = (getViewByWbId(server,
            getWorkbookByName(server, "Media Profit").id,"Management Dashboard"))
    group = (getUserListByGroup(server,"Push Tests"))

    users = []
    pagination_item = server.groups.populate_users(group)
    for user in group.users:
        users.append(user.name)
    server.views.populate_image(view_item)
    with open('./Screenshots/dashboard-screenshot-'+ str(date.today()) +'.png', 'wb') as f:
         f.write(view_item.image)
    server.auth.sign_out()
# ----------------- EMAIL SETTINGS -------------------------

    port = 465
    context = ssl.create_default_context()
    sender_email = "boomi@naturalint.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Management Dashboard - " + str(date.today())
    message["From"] = sender_email
    messageText = '<html><body><h3>dear all, please review ' + str(datetime.datetime.now().strftime("%B")) + \
                  ' Rev & GP status as of ' + str(date.today()) + ' below & linked' \
                  '</h3>' + '<p>' '<img src="cid:image1" height="800" width="1200">' \
                    '</p>' + '</body></html>'
    message.attach(MIMEText(messageText, "html"))

    fp = open('./Screenshots/dashboard-screenshot-'+ str(date.today()) +'.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("boomi@naturalint.com", "b89qPL4b")
        for reciever in users:
            message["To"] = reciever
            server.sendmail(sender_email, reciever, message.as_string())

        server.quit()