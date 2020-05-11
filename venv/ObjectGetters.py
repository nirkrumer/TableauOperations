import tableauserverclient as TSC


# Server #

def tableau_sign_in(url_server, user_name, password):
    tableau_auth = TSC.TableauAuth(user_name, password)
    server = TSC.Server(url_server)
    server.version = os.getenv("TABLEAU_API_VERSION", default="3.2")
    server.auth.sign_in(tableau_auth)
    return server

def tableauSignOut(server):
    server.auth.sign_out()   

# ------------------------------------------------------------------

def getWorkbookByName(server, wb_name):
    workbooks = [x for x in TSC.Pager(server.workbooks) if x.name == wb_name]
    return None if len(workbooks) == 0 else workbooks.pop()

def getUserListByGroup (server, group_name):

    groups = [x for x in TSC.Pager(server.groups) if x.name == group_name]
    return None if len(groups) == 0 else groups.pop()

def getViewByWbId(server, wbId, viewName):
    views = [x for x in TSC.Pager(server.views)
             if (x.workbook_id == wbId and x.name == viewName)]
    # views = []
    # for x in TSC.Pager(server.views):
    #     if (x.workbook_id == wbId and x.name == viewName):
    #         views.append(x)
    return None if len(views) == 0 else views.pop()

def getSubsciptionByName(server, wb_name):
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, wb_name))
    matching_workbooks, pagination_item = server.subscriptions.get(req_option)
    assert len(matching_workbooks) > 0, 'No subscription named {0} found'.format(wb_name)
    workbook = matching_workbooks[0]
    return workbook

def getUserByEmail(server, email):
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, email))
    matching_users, pagination_item = server.users.get(req_option)
    assert len(matching_users) > 0, 'No users named {0} found'.format(email)
    user = matching_users[0]
    return user

def getUserById(server, id):
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, id))
    matching_users, pagination_item = server.users.get(req_option)
    assert len(matching_users) > 0, 'No users named {0} found'.format(id)
    user = matching_users[0]
    return user

def getScheduleByName(server, name):
    schedules = [x for x in TSC.Pager(server.schedules) if x.name == name]
    return None if len(schedules) == 0 else schedules.pop()