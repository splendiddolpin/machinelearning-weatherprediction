from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load model dan kolom
model = joblib.load("model/weather_model.pkl")
columns = joblib.load("model/model_columns.pkl")

@app.route("/")
def landing():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def main():
    prediction = None
    error = None
    form_data = {}

    if request.method == "POST":
        try:
            humidity = request.form["humidity"]
            pressure = request.form["pressure"]
            temp = request.form["temp"]
            wind = request.form["wind"]
            raintoday = request.form["raintoday"]

            # Simpan ke form_data (STRING dulu, aman)
            form_data = {
                "humidity": humidity,
                "pressure": pressure,
                "temp": temp,
                "wind": wind,
                "raintoday": raintoday
            }

            # Konversi untuk model
            humidity_f = float(humidity)
            pressure_f = float(pressure)
            temp_f = float(temp)
            wind_f = float(wind)
            raintoday_i = int(raintoday)

            # Validasi
            if not (0 <= humidity_f <= 100):
                error = "Humidity harus 0–100%"
            elif not (900 <= pressure_f <= 1100):
                error = "Pressure harus 900–1100 hPa"
            elif not (-10 <= temp_f <= 60):
                error = "Temperature harus -10–60 °C"
            elif wind_f < 0:
                error = "Wind speed harus ≥ 0"

            if error is None:
                input_df = pd.DataFrame(
                    [[humidity_f, pressure_f, temp_f, wind_f, raintoday_i]],
                    columns=columns
                )

                result = model.predict(input_df)[0]
                prediction = "🌧️ HUJAN" if result == 1 else "☀️ TIDAK HUJAN"

        except ValueError:
            error = "Input tidak valid."

    return render_template(
        "main.html",
        prediction=prediction,
        error=error,
        form_data=form_data
    )

if __name__ == "__main__":
    app.run(debug=True)
