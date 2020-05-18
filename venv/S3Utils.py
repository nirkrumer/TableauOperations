import tableauserverclient as TSC
import boto3
from botocore.exceptions import NoCredentialsError

def getWorkbookByName(server, wb_name):
    workbooks = [x for x in TSC.Pager(server.workbooks) if x.name == wb_name]
    return None if len(workbooks) == 0 else workbooks.pop()

ACCESS_KEY = '####'
SECRET_KEY = '*****/WtfFO4elC+X2h'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

tableau_auth = TSC.TableauAuth('admin', 'xqKE4ynYHzoGCiVwPWsBGZrT')
server = TSC.Server('https://tableau.naturalint.com',use_server_version=True)

with server.auth.sign_in(tableau_auth):
    file_path = server.workbooks.download(getWorkbookByName(server, "Media Profit").id)
    uploaded = upload_to_aws(file_path, 'conversions-stg', 'boomi/tableauWB/mp.twbx')