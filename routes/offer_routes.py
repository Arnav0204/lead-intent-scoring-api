from flask import Blueprint,jsonify,request,current_app
from routes.dto.offer_dto import OfferDTO
from pydantic import ValidationError
from database_manager import DatabaseManager
import logging,json


offer_blueprint = Blueprint("offer_blueprint",__name__)

@offer_blueprint.route("/offer",methods=["POST"])
def create_offer():
    request_data = request.get_json()
    if request_data is None :
        logging.error("request data not found")
        return jsonify({"message":"request data not found"}),404

    try:
        dto = OfferDTO(**request_data)  
        create_offer_query = '''
            INSERT INTO offers (name,value_props,ideal_use_cases)
            VALUES (%s, %s, %s)
            RETURNING offer_id;
        '''
        create_offer_query_params = (
            dto.name,
            json.dumps(dto.value_props),      
            json.dumps(dto.ideal_use_cases)
        )
        #current_app.logger.info(f"name : {dto.name} , value_props: {dto.value_props} , ideal_use_cases : {dto.ideal_use_cases}")
        database_manager = DatabaseManager(current_app.config['DATABASE_URL'])
        response = database_manager.execute_query(create_offer_query,create_offer_query_params,True)
        if response and len(response) > 0:
            offer_id = response[0][0]
        else:
            offer_id = None

        return jsonify({
            "message": "Offer created successfully",
            "offer_id": offer_id
        }), 201  
    
    except ValidationError as e:
        logging.error("failed validation stage for request")
        return jsonify({"error": e.errors()}), 400
    
    except Exception as e:
        logging.error("failed to insert in database")
        return jsonify({"message":"failed to save data is offer table"})
    
        
