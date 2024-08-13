from flask import Flask, render_template, request, jsonify
import openai
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Set your API key
api_key = "Your_api_key_here"
openai.api_key = api_key

# Load the dataset
file_path = 'Bank Data.csv'
data = pd.read_csv(file_path)

# Function to prepare the user data for the API call
def prepare_user_data(row):
    user_data = {
        "Name": row['Name'],  # Include the customer's name
        "Age": row['Age'],
        "Annual Income": row['Annual_Income'],
        "Credit Score": "N/A",  # Assuming Credit Score is not directly available in the dataset
        "Number of Bank Accounts": row['Num_Bank_Accounts'],
        "Number of Credit Cards": row['Num_Credit_Card'],
        "Interest Rate on Loans": row['Interest_Rate'],
        "Number of Loans": row['Num_of_Loan'],
        "Credit Utilization Ratio": row['Credit_Utilization_Ratio'],
        "Outstanding Debt": row['Outstanding_Debt'],
        "Number of Delayed Payments": row['Num_of_Delayed_Payment'],
        "Credit Mix": row['Credit_Mix'],
        "Monthly Balance": row['Monthly_Balance'],
        "Total EMI per month": row['Total_EMI_per_month'],
        "Amount Invested Monthly": row['Amount_invested_monthly'],
        "Payment Behavior": row['Payment_Behaviour'],
        "Changed Credit Limit": row['Changed_Credit_Limit'],
        "Num of Credit Inquiries": row['Num_Credit_Inquiries'],
        "Occupation": row['Occupation'],
        "Type of Loan": row['Type_of_Loan'],
        "Credit History Age": row['Credit_History_Age'],
    }
    return user_data


# Function to assess financial risk using ChatGPT
def assess_financial_risk(user_data):
    prompt = (
        "You are a financial expert. Analyze the following user's financial history, "
        "credit score, and other relevant factors to assess the risk associated with offering "
        "financial services to this user. Provide a comprehensive risk assessment.\n\n"
        "User Data:\n"
    )
    for key, value in user_data.items():
        prompt += f"{key}: {value}\n"
    
    prompt += "\nBased on the data above, what is the risk level of offering financial services to this user?"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert financial analyst."},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message['content']

# Function to generate a response from the ChatGPT API for general queries
def chat_with_customer(user_data, customer_query):
    customer_name = user_data.get("Name", "Customer")  # Use the name from the data, or default to "Customer"
    
    prompt = (
        f"You are a financial expert and customer service representative. "
        f"The customer, {customer_name}, has provided the following details:\n\n"
    )
    for key, value in user_data.items():
        prompt += f"{key}: {value}\n"
    
    prompt += f"\nCustomer Query: {customer_query}\n"
    prompt += "Provide a concise, helpful, and informal response directly addressing the customer's query. Do not include any formal closing, signature, or placeholders like '[Your Name]'."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial expert and customer service representative."},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message['content']



# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-chat', methods=['POST'])
def start_chat():
    try:
        data_request = request.json
        customer_id = data_request.get('Customer_ID')

        if not customer_id:
            return jsonify({"response": "Customer ID is required."}), 400

        customer_data = data[data['Customer_ID'] == customer_id]

        if customer_data.empty:
            return jsonify({"response": f"No data found for Customer ID: {customer_id}"}), 404

        user_data = prepare_user_data(customer_data.iloc[0])

        risk_assessment = assess_financial_risk(user_data)
        return jsonify({"response": risk_assessment}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "An error occurred while processing your request."}), 500


@app.route('/chat', methods=['POST'])
def chat():
    data_request = request.json
    customer_id = data_request['Customer_ID']
    customer_query = data_request['query']
    
    customer_data = data[data['Customer_ID'] == customer_id]

    if customer_data.empty:
        return jsonify({"response": f"No data found for Customer ID: {customer_id}"}), 404
    
    user_data = prepare_user_data(customer_data.iloc[0])
    
    response = chat_with_customer(user_data, customer_query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)