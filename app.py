from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Load the trained model and scaler
with open("random_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

# Dummy user database (Replace with real database later)
users = {"admin": "password123"}

@app.route("/")
@app.route("/main")
def main():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("main.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("main"))
        else:
            return "Invalid username or password. Try again."

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password == confirm_password:
            users[username] = password  # Save new user
            return redirect(url_for("login"))
        else:
            return "Passwords do not match!"

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "user" not in session:
            return redirect(url_for("login"))

        input_data = [
            float(request.form["age"]),
            float(request.form["total_bilirubin"]),
            float(request.form["direct_bilirubin"]),
            float(request.form["alkaline_phosphotase"]),
            float(request.form["sgpt"]),
            float(request.form["sgot"]),
            float(request.form["total_proteins"]),
            float(request.form["albumin"]),
            float(request.form["albumin_globulin_ratio"]),
            int(request.form["gender"]),
        ]

        input_data = np.array(input_data).reshape(1, -1)
        scaled_data = scaler.transform(input_data)

        prediction = model.predict(scaled_data)[0]
        result = "Liver Disorder Detected" if prediction == 1 else "No Liver Disorder"

        return render_template("result.html", prediction=result)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
