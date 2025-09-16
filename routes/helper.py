import google.generativeai as genai

class Helper:
    def __init__(self,google_api_key):
        self.google_api_key = google_api_key
        genai.configure(api_key=self.google_api_key)

    def calculate_rule_score(self,lead, offer):
        role = (lead.get("role") or "").lower()
        if "decision" in role:
            role_score = 20
        elif "influencer" in role:
            role_score = 10
        else:
            role_score = 0

        industry = lead.get("industry") or ""
        exact_icp = offer.get("ideal_use_cases", [])
        adjacent = offer.get("value_props", [])

        if industry in exact_icp:
            industry_score = 20
        elif industry in adjacent:
            industry_score = 10
        else:
            industry_score = 0

        completeness_score = 10 if all([
            lead.get("role"),
            lead.get("company"),
            lead.get("industry"),
            lead.get("location"),
            lead.get("linkedin_bio")
        ]) else 0

        return role_score + industry_score + completeness_score

    def get_ai_score(self,lead, offer):
        system_prompt = """You are an AI assistant that classifies B2B lead intent.
            You must respond with ONLY:
            -Intent: High / Medium / Low
            -Reasoning: 1–2 clear sentences
            Do not include anything else.
        """

        user_prompt = f"""
            Prospect details:
            - Name: {lead['name']}
            - Role: {lead['role']}
            - Company: {lead['company']}
            - Industry: {lead['industry']}
            - Location: {lead['location']}
            - LinkedIn Bio: {lead['linkedin_bio']}

            Offer details:
            - Name: {offer['name']}
            - Value Props: {offer['value_props']}
            - Ideal Use Cases: {offer['ideal_use_cases']}

             Classify intent (High / Medium / Low) and give reasoning.
        """

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content([system_prompt, user_prompt])
        content = response.text.strip()

        intent, ai_points = "Low", 10
        if "High" in content:
            intent, ai_points = "High", 50
        elif "Medium" in content:
            intent, ai_points = "Medium", 30
        elif "Low" in content:
            intent, ai_points = "Low", 10

        return ai_points, intent, content

