import mysql.connector
import re
# MySQL database connection parameters
conn = mysql.connector.connect(
        user = 'root',
        password =  "Harshal@2002",
        host = 'localhost',
        database =  'pandeyji_eatery'

        )

def get_order_status(order_id: int):
    
    try:
        
        cursor = conn.cursor()

        # SQL query to fetch status based on order_id
        query = ("SELECT status FROM order_tracking WHERE order_id = %s")
        cursor.execute(query, (order_id,))

        # Fetch the status
        result = cursor.fetchone()

        cursor.close()
        if result:
            return result[0]
        else:
            return "Order ID not found"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    

def get_str_from_food_dict(new_food_dict:dict):
    return ", ".join([f"{int(value)} {key}" for key , value in new_food_dict.items()])


def extract_session_id(session_str:str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_str = match.group(1)
        return extracted_str
    
def insert_order_item(food_items, quantity, order_id):

    try:
        cursor = conn.cursor()
        cursor.callproc("insert_order_item",(food_items, quantity, order_id) )
        conn.commit()
        cursor.close()
        print("order item inserted succesfully")
        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        conn.rollback()
        return -1

def get_order_total(order_id):
    cursor = conn.cursor()
    query = f"select get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def insert_order_tracking(order_id, status):
    cursor = conn.cursor()

    # SQL query to fetch status based on order_id
    query = "insert into order_tracking (order_id, status) values (%s,%s)"
    cursor.execute(query, (order_id,status))

    conn.commit()

    cursor.close()



def get_next_order_id():
    cursor = conn.cursor()

    # SQL query to fetch status based on order_id
    query = ("select max(order_id) from orders")
    cursor.execute(query)

    # Fetch the status
    result = cursor.fetchone()[0]

    cursor.close()

    if result is None:
        return 1
    else:
        return result+1




