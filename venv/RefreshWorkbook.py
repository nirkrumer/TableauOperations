import tableauserverclient as TSC
import os

def getWorkbookByName(server, wb_name):
    workbooks = [x for x in TSC.Pager(server.workbooks) if x.name == wb_name]
    return None if len(workbooks) == 0 else workbooks.pop()

isScheduleExists = False
wbName = os.getenv("wbName");
TableauAdminPass = os.environ.get("TableauAdminPass")
tableau_auth = TSC.TableauAuth('admin', TableauAdminPass)
server = TSC.Server('https://tableau.naturalint.com',use_server_version=True)

with server.auth.sign_in(tableau_auth):
    all_tasks, pagination_item = server.tasks.get()    
    wb = getWorkbookByName(server,wbName)
    if (wb == None):
        print ("No workbook was found")

    for task in all_tasks:
        if task.target.id == wb.id:
            print("wbName = " + wb.name + " runs by schedule: task id = " + task.target.id + ", task sched = "+ task.schedule_id + ",type = " + task.target.type)
            server.tasks.run(task)
            isScheduleExists = True
            break
    if (isScheduleExists == False):
        print("wbName = " + wb.name + "(without schedule) runs!")
        results = server.workbooks.refresh(wb.id)

server.auth.sign_out()