from flask import Flask, request, jsonify
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="railway",
    user="postgres",
    password="ZHpeDgxheUQGJeUTurZYZFoPhUlzLtsf",
    host="shuttle.proxy.rlwy.net",
    port="49961"
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensors (
        id INT PRIMARY KEY,
        nume TEXT,
        tip TEXT,
        valoare INT,
        unitate TEXT,
        locatie TEXT,
        time TEXT
    )
""")
conn.commit()


app = Flask(__name__)
#lista senzori
senzori = [] #{"id": 1, "nume": "DHT", "tip": "temperatura", "valoare": 22, "unitate": "°C", "locatie": "Romania", "time": "2025-04-02 19:16:10"}
senzori_filtrati = []
#cautam toti senzorii
@app.route("/senzori", methods=["GET"])
def get_sensors():
    try:
        cursor.execute("SELECT * FROM sensors")
        rows = cursor.fetchall()
        sensors = []
        for row in rows:
            sensors.append({
                "id": row[0],
                "nume": row[1],
                "tip": row[2],
                "valoare": row[3],
                "unitate": row[4],
                "locatie": row[5],
                "time": row[6],
            })
        return jsonify(sensors), 200
    except Exception as e:
        conn.rollback()  # IMPORTANT: Reset transaction state
        return jsonify({"error": str(e)}), 400
    
#filtram dupa id
@app.route("/senzori/<int:id>", methods=["GET"])
def get_sensor_id(id):
    cursor.execute("SELECT * FROM sensors WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row:
        return jsonify({
            "id": row[0],
            "nume": row[1],
            "tip": row[2],
            "valoare": row[3],
            "unitate": row[4],
            "locatie": row[5],
            "time": row[6],
        }), 200
    return jsonify({"message": "Senzor invalid"}), 401   
    
#filtram dupa nume
@app.route("/senzori/<string:nume>", methods=["GET"])
def get_sensor_nume(nume):

    cursor.execute("SELECT * FROM sensors WHERE nume = %s", (nume,))
    rows = cursor.fetchall()
    if rows:
        sensors = []
        for row in rows:
            sensors.append({
                "id": row[0],
                "nume": row[1],
                "tip": row[2],
                "valoare": row[3],
                "unitate": row[4],
                "locatie": row[5],
                "time": row[6],
            })
        return jsonify(sensors), 200
    return jsonify({"message": "Senzor invalid"}), 401
      

#filtram dupa tip
@app.route("/senzori/tip/<string:tip>", methods=["GET"])
def get_sensor_tip(tip):
    # for senzor in senzori:
    #     if senzor["tip"] == tip: 
    #         return jsonify(senzor), 200 
    # return jsonify("senzor invalid"), 401         

    cursor.execute("SELECT * FROM sensors WHERE nume = %s", (tip,))
    rows = cursor.fetchall()
    if rows:
        sensors = []
        for row in rows:
            sensors.append({
                "id": row[0],
                "nume": row[1],
                "tip": row[2],
                "valoare": row[3],
                "unitate": row[4],
                "locatie": row[5],
                "time": row[6],
            })
        return jsonify(sensors), 200
    return jsonify({"message": "Senzor invalid"}), 401

#filtram dupa valoare
# @app.route("/senzori/val/<int:max>:<int:min>", methods=["GET"])
# def get_sensor_valoare(max, min):
#     # for senzor in senzori:
#     #     if ((senzor["valoare"] <= max) and (senzor["valoare"] >= min)):
#     #         return jsonify(senzor), 200 
#     # return jsonify("senzor invalid"), 401       

#     senzori_filtrati = [senzor for senzor in senzori if (senzor["valoare"] >= min) and (senzor["valoare"] >= min)]

#     if senzori_filtrati:
#         return jsonify(senzori_filtrati), 200
#     else:
#         return jsonify({"mesaj": "Senzor invalid"}), 401


#------------------------------------------------------------------#

#adaugam senzor nou
@app.route("/senzori", methods=["POST"])
def add_sensor():
    data = request.json
    cursor.execute("""
        INSERT INTO sensors (id, nume, tip, valoare, unitate, locatie, time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (data["id"], data["nume"], data["tip"], data["valoare"],
          data["unitate"], data["locatie"], data["time"]))
    conn.commit()
    return jsonify({"message": "Senzor adăugat"}), 201

#actualizam senzor
@app.route("/senzori/<int:id>", methods=["PUT"])
def update_sensor(id):
    data = request.json
    cursor.execute("""
        UPDATE sensors 
        SET nume = %s, tip = %s, valoare = %s, unitate = %s, locatie = %s, time = %s 
        WHERE id = %s
    """, (data["nume"], data["tip"], data["valoare"], data["unitate"],
          data["locatie"], data["time"], id))
    conn.commit()
    return jsonify({"message": "Senzor actualizat"}), 203

##stergem
@app.route("/senzori/<int:id>", methods=["DELETE"])
def delete_sensor(id):
    cursor.execute("DELETE FROM sensors WHERE id = %s", (id,))
    conn.commit()
    return jsonify({"message": "Senzor șters"}), 202

    
if __name__ == "__main__":
    app.run(debug=True)

#senzor adaugat -- 201
#senzor sters -- 202
#senzor actualizat -- 203
#senzor invalid -- 401
#senzon negasit -- 404