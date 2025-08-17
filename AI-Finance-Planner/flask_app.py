from google import genai
from flask import Flask, render_template, request
import re

app = Flask(__name__)
client = genai.Client(api_key="AIzaSyCYvL7_3gqLx_OxfII0_j-gcv-P1AJt650")  # Replace with your actual API key


@app.route('/', methods=['GET', 'POST'])
def finance_planner():
    if request.method == "GET":
        return render_template("front.html")  # Your finance planner form page
    elif request.method == "POST":
        # Get form inputs
        profession = request.form["incomeType"]
        monthly_income = request.form["monthlyIncome"]
        age = request.form["age"]
        risk_appetite = request.form["riskAppetite"]

        user_prompt = f"""
        Generate a comprehensive financial plan in HTML format for:
        - Profession: {profession}
        - Monthly Income: ₹{monthly_income}
        - Age: {age}
        - Risk Appetite: {risk_appetite}

        Include these sections with detailed calculations:
        1. Monthly Budget Allocation (as percentages and amounts):
           - Essentials (housing, food, utilities)
           - Savings (emergency fund, short-term goals)
           - Insurance (health, life)
           - Investments (breakdown by risk level)
           

        2. Investment Portfolio Recommendation:
           - Equity (stocks, mutual funds)
           - Debt (bonds, fixed deposits)
           - Alternative (gold, real estate)
           - Crypto (if high risk)

        3. Long-term Projections:
           - Retirement corpus at age 60
           - Wealth growth at 5/10/20 years
           - Emergency fund target

        all these 4 section shoulbe explained in more lines or deep information
        Use Indian financial context with ₹ currency formatting.
        Include visual elements like progress bars for allocations.
        Return ONLY clean HTML without markdown or code blocks.
        """

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_prompt
        )

        # Clean the response (same as original)
        html_content = response.text
        html_content = re.sub(r'^\s*(```html|```|HTML)\s*', '', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'\s*(```|HTML)\s*$', '', html_content, flags=re.IGNORECASE)
        html_content = html_content.replace('"""', '')

        return render_template("back.html", display=html_content)


if __name__ == "__main__":
    app.run(debug=True)