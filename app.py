from flask import Flask, request, jsonify
from util import get_order_status, get_str_from_food_dict, extract_session_id, insert_order_item,get_next_order_id, get_order_total, insert_order_tracking
app = Flask(__name__)

inprogress_order = {}

''' formate
#inprogress_order = {
     session_id = {pizza:1, samosa :2},
     seeion_id = {chole bhatire:1, dosa:3}
 }'''

def track_order(parameters:dict,session_id):
    order_id = int(parameters["number"])
    status = get_order_status(order_id)

    if status:
        fulfilment_text = f"The order status for order id {order_id} is {status}"
    else:
        fulfilment_text = f"No order found with order id {order_id}"
    

    return jsonify({"fulfillmentText": fulfilment_text})


                   

def add_order(parameters:dict,session_id):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfilment_text  = "Sorry i dont understand please specify food iteam and quantites clearly"
        return jsonify({"fulfillmentText": fulfilment_text})
    else:
        new_food_dict = dict(zip(food_items, quantities))
        if session_id in inprogress_order:
            result = {}
            for key in inprogress_order[session_id].keys() | new_food_dict.keys():
                result[key] = inprogress_order[session_id].get(key, 0) + new_food_dict.get(key, 0)
            # current_dict = inprogress_order[session_id]
            # current_dict.update(new_food_dict)
            inprogress_order[session_id] = result

        else:
            inprogress_order[session_id] = new_food_dict

        order_str = get_str_from_food_dict(inprogress_order[session_id])
        # print("**************")
        # print(inprogress_order)
        return jsonify({"fulfillmentText": f"So far you have {order_str} do you want anything else?"})
    


def remove_order(parameters:dict,session_id):
    if session_id not in inprogress_order:
        return jsonify({"fulfillmentText": "I am having trouble finding your order plz place new order"})
    
    current_food_dict = inprogress_order[session_id]
    food_item = parameters['food-item']

    removed = []
    no_item = []

    for item in food_item:
        if item not in current_food_dict:
            no_item.append(item)
            # return jsonify({"fulfillmentText": f"The given food item {','.join(no_item)} not in your order list Anything else you wnat!"})
        else:
            removed.append(item)
            del current_food_dict[item]
        
    if len(removed)>0:
        fulfilment_text = f"We have removed {','.join(removed)} from your order list\n"
    if len(no_item)>0:
        fulfilment_text += f"Your current order does not have {','.join(no_item)} \n"
    if len(current_food_dict.keys()) == 0:
        fulfilment_text += "Your order is empty"
    else:    
        order_str = get_str_from_food_dict(current_food_dict)
        fulfilment_text += f"Here is what is left in your order {order_str} Anything else you want!"

    return jsonify({"fulfillmentText": fulfilment_text})

        
        
        


def complete_order(parameters:dict,session_id):

    if session_id not in inprogress_order:
        fulfilment_text = "I am having trouble to find your order. Sorry! Can you place a new order"

    else:
        order = inprogress_order[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfilment_text = "Sorry i could not place your order due to backend error. "\
                              "please place new order again"
        else:
            order_total = get_order_total(order_id)
            fulfilment_text = "Awesome We have placed your orde. r"\
                              f"Here is your order id: {order_id}. "\
                              f"Your order bill is {order_total} which you can pay at the time of delivery"
        del inprogress_order[session_id]  # this will remove placed order from dict
    
    return jsonify({"fulfillmentText": fulfilment_text})
            

def save_to_db(order:dict):
    next_order_id = get_next_order_id()
    for food_items, quantity in order.items():
        rcode = insert_order_item(food_items, 
                          quantity, 
                          next_order_id)
        if rcode == -1:
            return -1
    insert_order_tracking(next_order_id,"in progress")
    return next_order_id

@app.route("/",methods = ["POST"])
def index():
    data = request.get_json()
    intent = data["queryResult"]["intent"]["displayName"]
    parameters = data['queryResult']['parameters']
    query_result = data.get("queryResult", {})
    output_contexts = query_result.get("outputContexts", [])
    # session_id = output_contexts[0]["name"].split("/")[4]
    session_id = extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {'track-order:context-order-tracking': track_order,
                           'order-add-context:ongoing-order': add_order,
                           'order-complete-context:ongoing-order': complete_order,
                           'order-remove-context:ongoing-order': remove_order
                        }
    function = intent_handler_dict[intent]
    return function(parameters, session_id)

if __name__ == "__main__":
    app.run(debug=True)



