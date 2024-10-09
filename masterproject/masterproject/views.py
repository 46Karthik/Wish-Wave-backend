import random

def generate_numeric_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

def return_sql_results(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    result = []
    if rows:
        result = [json.loads(row[0]) for row in rows]
    return result

def return_response(statuscode, message, data=None):
    if data is not None:
        return {
            'status': statuscode,
            'message': message,
            'data': data
        }
    else:
        return {
            'status': statuscode,
            'message': message
        }