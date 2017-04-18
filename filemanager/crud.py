from google.cloud import datastore
import datetime

ds = datastore.Client()

"""
@Method_Name: store_data
@Param_in: title, description, filename, file_url
@Description: This methods add a FileInfo entity to data store.
"""


def store_data(title, description, filename, file_url, size):
    entity = datastore.Entity(key=ds.key('FileInfo'))
    entity.update({
        'title': title,
        'description': description,
        'filename': filename,
        'url': file_url,
        'timestamp': datetime.datetime.utcnow()
    })
    ds.put(entity)


"""
@Method_Name: retrieve_files
@Description: Retrieve all the files in data store in DESCENDING order.
"""


def retrieve_files():
    return ds.query(kind='FileInfo', order=('-timestamp',)).fetch()


"""
@Method_Name: add_user
@Param_in: email, password, salt
@Description: This methods add an user entity to data store.
"""


def add(email, password, salt):
    entity = datastore.Entity(key=ds.key('Users'))
    entity.update({
        'email': email,
        'password': password,
        'salt': salt,
    })
    ds.put(entity)


"""
@Method_Name: retrieve_files
@Param_in:email
@Description: Retrieve the user entity based on email
"""


def get_user(email):
    query = ds.query(kind='Users')
    query.add_filter('email', '=', email)
    return query.fetch()
