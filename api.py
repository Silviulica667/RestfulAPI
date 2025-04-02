from flask import Flask, request, jsonify

app = Flask(__name__)

#lista senzori
senzori = [] #{"id": 1, "nume": "DHT", "tip": "temperatura", "valoare": 22, "unitate": "°C", "locatie": "Romania", "time": "2025-04-02 19:16:10"}

#cautam toti senzorii
@app.route("/senzori", methods=["GET"])
def get_sensors():
    return jsonify(senzori), 200

#filtram dupa id
@app.route("/senzori/<int:id>", methods=["GET"])
def get_sensor_id(id):
    for senzor in senzori:
        if senzor["id"] == id: 
            return jsonify(senzor), 200 
    return jsonify("senzor invalid"), 400      
    
#filtram dupa nume
@app.route("/senzori/<string:nume>", methods=["GET"])
def get_sensor_nume(nume):
    for senzor in senzori:
        if senzor["nume"] == nume: 
            return jsonify(senzor), 200 
    return jsonify("senzor invalid"), 400       

#filtram dupa tip
@app.route("/senzori/tip/<string:tip>", methods=["GET"])
def get_sensor_tip(tip):
    for senzor in senzori:
        if senzor["tip"] == tip: 
            return jsonify(senzor), 200 
    return jsonify("senzor invalid"), 400         

#filtram dupa valoare
@app.route("/senzori/val/<int:max>:<int:min>", methods=["GET"])
def get_sensor_valoare(max, min):
    for senzor in senzori:
        if ((senzor["valoare"] <= max) and (senzor["valoare"] >= min)):
            return jsonify(senzor), 200 
    return jsonify("senzor invalid"), 400       


#adaugam senzor nou
@app.route("/senzori", methods=["POST"])
def add_sensor():
    data = request.json

    for senzor in senzori:
        if senzor["id"] == data["id"]: 
            senzor.update(data)
            return jsonify({"message": "Senzor actualizat"}), 200

    senzori.append(data) 
    return jsonify({"message": "Senzor adăugat"}), 201

#actualizam senzor
@app.route("/senzori/<int:id>", methods=["PUT"])
def update_sensor(sensor_id):

    data = request.json 

    for senzor in senzori:
        if senzor["id"] == sensor_id:
            senzor.update(data) 
            return jsonify({"message": "Senzor actualizat"}), 200  
    return jsonify({"error": "Senzorul nu a fost găsit"}), 404

##stergem
@app.route("/senzori/<int:id>", methods=["DELETE"])
def delete_sensor(id):
    global senzori
    senzori = [s for s in senzori if s["id"] != id]
    return jsonify({"message": "Senzor șters"}), 200


if __name__ == "__main__":
    app.run(debug=True)
