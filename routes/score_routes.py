from flask import Blueprint,jsonify,request,current_app
from database_manager import DatabaseManager
from routes.helper import Helper


score_blueprint = Blueprint("score_blueprint",__name__)

@score_blueprint.route("/results",methods=["GET"])
def get_results():
    # Get offer_id from query parameters
    offer_id = request.args.get("offer_id")
    
    if not offer_id:
        current_app.logger.error("offer_id not found in query parameters")
        return jsonify({"message": "offer_id is required as query parameter"}), 400
    
    try:
        database_manager = DatabaseManager(current_app.config['DATABASE_URL'])
        
        # Query to get all results for a specific offer_id
        results_query = '''
            SELECT 
                l.name,
                l.role, 
                l.company,
                s.intent,
                s.total_score,
                s.reasoning
            FROM leads l
            JOIN scores s ON l.lead_id = s.lead_id
            JOIN offers o ON s.offer_id = o.offer_id
            WHERE o.offer_id = %s
            ORDER BY s.total_score DESC
        '''
        
        current_app.logger.info(f"Fetching results for offer_id: {offer_id}")
        rows = database_manager.execute_query(results_query, (offer_id,), True)
        
        if not rows:
            current_app.logger.warning(f"No results found for offer_id={offer_id}")
            return jsonify([]), 200  # Return empty array if no results
        
        # Format the results
        results = []
        for row in rows:
            result = {
                "name": row[0],
                "role": row[1], 
                "company": row[2],
                "intent": row[3],
                "score": int(row[4]) if row[4] is not None else 0,  # Ensure score is integer
                "reasoning": row[5] or ""  # Handle null reasoning
            }
            results.append(result)
        
        current_app.logger.info(f"Returning {len(results)} results for offer_id={offer_id}")
        return jsonify(results), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching results: {str(e)}", exc_info=True)
        return jsonify({
            "message": "Internal server error occurred",
            "error": str(e)
        }), 500


@score_blueprint.route("/score",methods=["POST"])
def score():
    request_data = request.get_json()
    offer_id = request_data.get("offer_id")
    if not offer_id:
        current_app.logger.error("offer_id not found in request")
        return  jsonify({"message":"offer_id not found in request"})
    
    try:
        database_manager = DatabaseManager(current_app.config['DATABASE_URL'])
        helper = Helper(current_app.config['GOOGLE_API_KEY'])
        join_query = '''SELECT 
            l.lead_id, l.name, l.role, l.company, l.industry, l.location, l.linkedin_bio,
            o.offer_id, o.name, o.value_props, o.ideal_use_cases
            FROM leads l
            JOIN offers o ON l.offer_id = o.offer_id
            WHERE o.offer_id = %s
        '''
        rows = database_manager.execute_query(join_query,(offer_id,),True)
        if not rows:
            current_app.logger.warning(f"No data found for offer_id={offer_id}")
            return jsonify({"message": "No leads found for this offer"}), 404
        
        current_app.logger.info(f"Fetched {len(rows)} rows for offer_id={offer_id}")

        for row in rows:
            lead = {
                "lead_id": row[0],
                "name": row[1],
                "role": row[2],
                "company": row[3],
                "industry": row[4],
                "location": row[5],
                "linkedin_bio": row[6],
            }
            #current_app.logger.info(f" lead is : {lead}")
            offer = {
                "offer_id": row[7],
                "name": row[8],
                "value_props": row[9],
                "ideal_use_cases": row[10],
            }
            current_app.logger.info(f" offer is : {offer}")
        
            rule_score = helper.calculate_rule_score(lead, offer)

            # AI score via Gemini
            ai_score, intent, reasoning = helper.get_ai_score(lead, offer)

       
             # Insert into scores table
            insert_query = """
                INSERT INTO scores (total_score, intent, reasoning, offer_id, lead_id)
                VALUES (%s, %s, %s, %s, %s);
            """
            database_manager.execute_query(
                insert_query,
                (rule_score+ai_score, intent, reasoning, offer["offer_id"], lead["lead_id"]),
                False
            )

        return jsonify({
            "message": "Scores inserted successfully",
        }), 201


    except Exception as e:
        current_app.logger.error("error in joining offer and lead")
        return  jsonify({"message":"unable to fetch offer and lead"})
    
