from flask import request, Response, json, Blueprint, current_app
from service.reader import get_analysis, get_graph_yearwise, get_commodities_list
from middleware.validator import validate_request

# user controller blueprint to be registered with api blueprint
readers = Blueprint("reader", __name__)

# route for login api/users/signin
@readers.route('/analysis/<commodity>', methods = ["POST"])
def analysis(commodity):
    try: 
        data = request.json
        mongo_dao = current_app.mongo_dao

        if "markets" in data and type(data['markets'])==list:
            if len(data['markets']) == 0:
                data['markets'] = None
            mongo_dao = current_app.mongo_dao
            res = get_analysis(commodity=commodity, mongo_dao=mongo_dao, markets=data['markets'])
            return Response(
                response=json.dumps(res),
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps({'status': "failed",
                                        "message": "markets should be a list"}),
                status=400,
                mimetype='application/json'
            )
        
    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed", 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )
    

@readers.route('/graph', methods = ["POST"])
def graph():
    try:
        data = request.json
        mongo_dao = current_app.mongo_dao


        valid, data = validate_request(request, ["commodity", "from_year", "to_year", "markets"])
        if not valid:
            return Response(
                response=json.dumps({'status': "failed",
                                        "message": "from_year, to_year and market are required"}),
                status=400,
                mimetype='application/json'
            )

        if type(data['from_year']) == int and type(data['to_year']) == int and type(data['markets'])==list:
                if len(data['markets']) == 0:
                    data['markets'] = None
                res = get_graph_yearwise(commodity=data["commodity"], mongo_dao=mongo_dao, from_year=data['from_year'], to_year=data['to_year'], markets=data['markets'])
                return Response(
                    response=res,
                    status=200,
                    mimetype='application/json'
                )
        else:
            return Response(
                response=json.dumps({'status': "failed",
                                    "message": "from_year and to_year and market should be int, int and list respectively"}),
                status=400,
                mimetype='application/json'
            )
    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed", 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )
    
@readers.route('/get_commodities', methods = ["POST"])
def get_commodity_l():
    try:
        mongo_dao = current_app.mongo_dao
        res = get_commodities_list(mongo_dao=mongo_dao)
        return Response(
            response=json.dumps(res),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed", 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )
    

