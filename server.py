from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

app = Flask(__name__)

# Initialize game history and chips balances
game_history = []
players = {"player1": 10000, "player2": 15000}  # Example balances

# LSTM Model Definition
model = Sequential()
model.add(LSTM(50, activation="relu", input_shape=(10, 1)))
model.add(Dense(1))
model.compile(optimizer="adam", loss="mse")

# Train LSTM Model with historical data
def train_model(data):
    data = np.array(data).reshape(-1, 1)
    generator = TimeseriesGenerator(data, data, length=10, batch_size=1)
    model.fit(generator, epochs=50, verbose=0)

# Route to train the model
@app.route("/train", methods=["POST"])
def train():
    data = request.json.get("history")
    if len(data) >= 10:
        train_model(data)
        return jsonify({"status": "Model trained successfully"})
    return jsonify({"error": "Insufficient data"}), 400

# Route to predict the next result
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("history")
    if len(data) < 10:
        return jsonify({"error": "Insufficient data for prediction"}), 400
    input_data = np.array(data[-10:]).reshape(1, 10, 1)
    prediction = model.predict(input_data)
    return jsonify({"result": int(prediction[0][0])})

# Route to simulate a spin
@app.route("/spin", methods=["POST"])
def spin():
    global game_history
    new_result = np.random.randint(0, 37)  # Replace with PRNG logic if needed
    game_history.append(new_result)
    if len(game_history) > 10:
        game_history.pop(0)
    return jsonify({"result": new_result, "history": game_history})

# Route to get player balance
@app.route("/balance", methods=["GET"])
def balance():
    return jsonify(players)

# Route to update player balance
@app.route("/update_balance", methods=["POST"])
def update_balance():
    data = request.json
    player = data.get("player")
    amount = data.get("amount")
    if player in players:
        players[player] += amount
        return jsonify({"balance": players[player]})
    return jsonify({"error": "Player not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
