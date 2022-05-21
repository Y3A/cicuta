from hashlib import sha256

# http path
fetch_path = "/jquery3.37/"
get_task_path = "/tailwinds8.1/"
res_path = "/submitwebcache/"

# http post variable name
data_var = "data"

# encryption
key = sha256("7eykutaxx".encode()).digest()[:32]

# http response
res_none_existent = 405
res_success = 200
res_no_tasks = 404