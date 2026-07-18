from flask import Flask, request, jsonify
from flask_cors import CORS
from celery import Celery
import os
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

mongo_client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
db = mongo_client['vyaapar_drishti_db']

@celery.task(bind=True)
def process_ledger_async(self, file_name):
    self.update_state(state='PROCESSING', meta={'status': 'Extracting ledger text...'})
    
    extracted_data = {
        "vendor_id": "VEND-9912",
        "monthly_inflow": 45000,
        "monthly_outflow": 32000,
        "risk_flags": ["Seasonal Drought Alert", "High Credit Concentration"]
    }
    
    net_flow = extracted_data["monthly_inflow"] - extracted_data["monthly_outflow"]
    risk_score = 75 if net_flow < 15000 else 30
    
    db.ledger_insights.insert_one({
        "task_id": self.request.id,
        "extracted_data": extracted_data,
        "risk_score": risk_score,
        "status": "COMPLETED"
    })
    
    return {'status': 'Success', 'risk_score': risk_score, 'flags': extracted_data["risk_flags"]}

@app.route('/api/upload', methods=['POST'])
def upload_ledger():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
        
    file = request.files['image']
    file_name = file.filename
    
    task = process_ledger_async.delay(file_name)
    
    return jsonify({"message": "File received. Processing started.", "task_id": task.id}), 202

@app.route('/api/status/<task_id>', methods=['GET'])
def get_status(task_id):
    result = db.ledger_insights.find_one({"task_id": task_id}, {"_id": 0})
    if result:
        return jsonify(result), 200
        
    task = process_ledger_async.AsyncResult(task_id)
    return jsonify({"status": task.state, "info": task.info}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
