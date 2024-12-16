from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database
users = []
expenses = []

# Helper functions
def calculate_balances():
    balances = {}
    for expense in expenses:
        amount_per_person = expense['amount'] / len(expense['shared_with'])
        for user in expense['shared_with']:
            balances[user] = balances.get(user, 0) - amount_per_person
        balances[expense['paid_by']] = balances.get(expense['paid_by'], 0) + expense['amount']
    return balances

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    user_name = data.get("name")
    if user_name in users:
        return jsonify({"error": "User already exists."}), 400
    users.append(user_name)
    return jsonify({"message": "User added successfully."}), 201

@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    paid_by = data.get("paid_by")
    amount = data.get("amount")
    shared_with = data.get("shared_with")

    if paid_by not in users or any(user not in users for user in shared_with):
        return jsonify({"error": "Invalid user(s) in the expense."}), 400

    expense = {
        "paid_by": paid_by,
        "amount": amount,
        "shared_with": shared_with
    }
    expenses.append(expense)
    return jsonify({"message": "Expense added successfully."}), 201

@app.route("/balances", methods=["GET"])
def get_balances():
    balances = calculate_balances()
    return jsonify(balances)

@app.route("/reset", methods=["POST"])
def reset():
    global users, expenses
    users = []
    expenses = []
    return jsonify({"message": "Data reset successfully."}), 200

if __name__ == "__main__":
    app.run(debug=True)
