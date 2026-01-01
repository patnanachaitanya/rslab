from flask import Flask, request, render_template
import mysql.connector
import time

app = Flask(__name__)

MYSQL_CONFIG = {
    'host': 'localhost', 'user': 'root', 
    'password': '', 'port': 3306, 'database': 'sqli_lab'
}

def validate_tracking_id(tracking_id):
    """Return the matching row or None. Raise exceptions on DB errors."""
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    query = f"""
        SELECT o.id, o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.tracking_id = '{tracking_id}'
    """

    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close(); conn.close()
    return result

@app.route('/')
def index():
    tid = request.args.get('tracking_id', '')
    is_valid = validate_tracking_id(tid) if tid else False
    return render_template('index.html', tid=tid, valid=is_valid)

@app.route('/track')
def track():
    """🚨 MAIN BLIND SQLi ENDPOINT - 200/500 ONLY"""
    tid = request.args.get('tracking_id', '')
    if not tid:
        return ('tracking_id required', 400)

    try:
        row = validate_tracking_id(tid)
    except Exception as e:
        app.logger.exception('DB error')
        return (f'Internal Server Error: {e}', 500)

    if row:
        return (f'Order found (id={row[0]}, status={row[1]})', 200)
    else:
        return ('No order found', 404)

if __name__ == '__main__':
    print("🔥 http://localhost:5000/track?tracking_id=...")
    print("✅ 200 = TRUE  |  ❌ 500 = FALSE")
    app.run(port=5000)