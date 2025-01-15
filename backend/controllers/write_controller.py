from dao.mongo_dao import MongoDao
from flask import request, Response, json, Blueprint, current_app
from service.writer import update_commodity_in_atlas

# user controller blueprint to be registered with api blueprint
writers = Blueprint("writer", __name__)
    
@writers.route('/update/<commodity>', methods = ["POST"])
def update_commodity(commodity):
    try:
        mongo_dao = current_app.mongo_dao
        res = update_commodity_in_atlas(mongo_dao=mongo_dao, commodity=commodity)

        if res:
            return Response(
                response=json.dumps({'status': "success",
                                    "message": "Data updated successfully"}), 
                                    status=200)

    except Exception as e:
        return Response(response=json.dumps({"error": f"Internal Server Error: {str(e)}", 
                                             "status": "failure"}), 
                                             status=500)
