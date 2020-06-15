import tableauserverclient as TSC
import os

def getWorkbookByName(server, wb_name):
    workbooks = [x for x in TSC.Pager(server.workbooks) if x.name == wb_name]
    return None if len(workbooks) == 0 else workbooks.pop()

wbName = os.getenv("wbName");
TableauAdminPass = os.environ.get("TableauAdminPass")
tableau_auth = TSC.TableauAuth('admin', TableauAdminPass)
server = TSC.Server('https://tableau.naturalint.com',use_server_version=True)

with server.auth.sign_in(tableau_auth):
    wb = getWorkbookByName(server,wbName)
    results = server.workbooks.refresh(wb)

server.auth.sign_out()