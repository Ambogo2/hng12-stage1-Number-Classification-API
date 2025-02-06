from flask import Flask, jsonify, request
import request

from flask_cors import CORS

app = Flask(__name__)

CORS(app)


def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is perfect (sum of divisors equals number)."""
    return n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_fun_fact(n):
    """Fetch a fun fact from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}?json")
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available.")
    except:
        return "No fun fact available."
    return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """API endpoint to classify a number."""
    number = request.args.get('number')

    # Validate input
    if not number or not number.isdigit():
        return jsonify({"number": number, "error": True}), 400

    number = int(number)
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 1:
        properties.append("odd")
    else:
        properties.append("even")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(number)),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
