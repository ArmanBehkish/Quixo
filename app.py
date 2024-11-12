from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/zbd-callback', methods=['POST'])
def handle_callback():
    data = request.json
    payment_status = data.get('status')
    internal_id = data.get('internalId')

    if payment_status == 'completed':
        # Handle completed payment
        print(f"Payment for internalId {internal_id} is completed.")
        # Update your database, grant access, etc.
    elif payment_status == 'failed':
        # Handle failed payment
        print(f"Payment for internalId {internal_id} has failed.")
        # Take appropriate actions

    return jsonify({"message": "Callback received"}), 200

if __name__ == '__main__':
    app.run(port=5000)
