from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def hava_durumu(lat, lon):
    API = "28a803c33accc36ae8a251bbec3ee8fc"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = f"{BASE_URL}lat={lat}&lon={lon}&appid={API}"
    gelen_veri = requests.get(URL)
    gelen_veri_JSON = gelen_veri.json()

    if gelen_veri_JSON["cod"] != "404":
        temp_kelvin = gelen_veri_JSON["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15
        description = gelen_veri_JSON["weather"][0]["description"]
        country = gelen_veri_JSON["sys"]["country"]
        city_name = gelen_veri_JSON["name"]
        return temp_celsius, description, country, city_name
    else:
        return

@app.route('/weather_api/<float:lat>/<float:lon>', methods=['GET'])
def weather_api(lat, lon):
    sonuc = hava_durumu(lat, lon)
    if sonuc:
        temp, description, country, city_name = sonuc
        return jsonify({
            "Şehir": city_name,
            "Sıcaklık": f"{temp:.2f}°C",
            "Açıklama": description,
            "Ülke": country
        })
    else:
        return jsonify({"Hata": "Şehir bulunamadı."})

if __name__ == '__main__':
    app.run(debug=True)
