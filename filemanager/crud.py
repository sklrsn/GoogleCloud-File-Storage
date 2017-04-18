from google.cloud import datastore
import datetime

ds = datastore.Client()


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


def retrieve_files():
    return ds.query(kind='FileInfo', order=('-timestamp',)).fetch()


def add(email, password, salt):
    entity = datastore.Entity(key=ds.key('Users'))
    entity.update({
        'email': email,
        'password': password,
        'salt': salt,
    })
    ds.put(entity)


def get_user(email):
    query = ds.query(kind='Users')
    query.add_filter('email', '=', email)
    return query.fetch()
