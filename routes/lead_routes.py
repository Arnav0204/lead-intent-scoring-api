from flask import Blueprint,jsonify,request,current_app
from routes.dto.lead_dto import LeadDTO
from database_manager import DatabaseManager
from pydantic import ValidationError
import io,csv


lead_blueprint = Blueprint("lead_blueprint",__name__)

@lead_blueprint.route("/leads/upload",methods=["POST"])
def create_leads():

    if "file" not in request.files:
        current_app.logger.error("csv file missing in request")
        return jsonify({"error": "CSV file is required"}), 404
    
    file = request.files["file"]
    offer_id = request.args.get("offer_id") or request.form.get("offer_id")

    if not offer_id:
        return jsonify({"error": "offer_id is required"}), 404
    
    try:
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        reader = csv.DictReader(stream)

        inserted, errors = [], []
        database_manager = DatabaseManager(current_app.config['DATABASE_URL'])
        for idx, row in enumerate(reader, start=1):
            try:
                lead = LeadDTO(**row)  

                query = """
                    INSERT INTO leads (name, role, company, industry, location, linkedin_bio, offer_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING lead_id
                """
                params = (
                    lead.name,
                    lead.role,
                    lead.company,
                    lead.industry,
                    lead.location,
                    lead.linkedin_bio,
                    offer_id
                )

                result = database_manager.execute_query(query, params, fetch=True)
                lead_id = result[0][0] if result else None
                inserted.append({"row": idx, "lead_id": lead_id})

            except ValidationError as ve:
                errors.append({"row": idx, "errors": ve.errors()})
        
        return jsonify({
            "message": "CSV processed",
            "inserted": inserted,
            "errors": errors
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    


