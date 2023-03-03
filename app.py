
from flask import Flask, request
from pymongo import MongoClient
from dbconnect import MongoDatabaseProperty

from bson.json_util import dumps


app = Flask(__name__)

colz = MongoDatabaseProperty()
 

@app.route('/')
def test():
    return 'Hello World'

@app.route('/getProperty', methods = ['GET'])
# ‘/’ URL is bound with hello_world() function.
def getProperty():
   
    #Get all entries from mongo. Inside {} filters can be added
    res = colz.find({})
    
    if res:
        # Converting to the JSON
        list_cur = list(res)
        json_data = dumps(list_cur, indent = 2) 
    
        return json_data
    else:
        return "Error could not retieve data", 400


@app.route('/addProperty', methods = ['POST'])
def postProperty():

    post_body = request.json

    if "greenscore" not in post_body:
        return "Missing 'greenscore' in body", 400

    if "address" not in post_body:
        return "Missing 'address' in body", 400
    
    if "property-values" not in post_body:
        return "Missing 'property-values' in body", 400
    
    if "energy" not in post_body["property-values"]:
        return "Missing 'energy' in body", 400
    
    if "co2" not in post_body["property-values"]:
        return "Missing 'co2' in body", 400
    
    if "waste" not in post_body["property-values"]:
        return "Missing 'waste' in body", 400
    
    if "clean-energy" not in post_body["property-values"]:
        return "Missing 'clean-energy' in body", 400
    
    if "area" not in post_body["property-values"]:
        return "Missing 'area' in body", 400
    
    if "property-type" not in post_body["property-values"]:
        return "Missing 'property-type' in body", 400
    

    
    temp_dict = {"address":post_body["address"]}

    res = colz.find_one(temp_dict)
    if res:
        return 'already exists', 409


    colz.insert_one(post_body)

    res = colz.find_one(temp_dict)
    if res:
        return str(res["_id"])
    else: 
        return 'could not add to mongo', 400

    
 
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0', port=5000)