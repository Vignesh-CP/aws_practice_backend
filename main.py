from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import boto3
from boto3.dynamodb.conditions import Key
import datetime

app = FastAPI()
handler = Mangum(app)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EquipmentTelemetry')

class TelemetryData(BaseModel):
    equipment_id: str
    temperature: int
    status: str

@app.post("/telemetry")
def receive_data(data: TelemetryData):
    current_time = datetime.datetime.utcnow().isoformat()
    table.put_item(
        Item={
            'equipment_id': data.equipment_id,
            'timestamp': current_time,
            'temperature': data.temperature,
            'status': data.status
        }
    )
    return {"message": "Data saved successfully", "equipment_id": data.equipment_id}

# NEW: GET endpoint to fetch data for a specific equipment
@app.get("/telemetry/{equipment_id}")
def get_data(equipment_id: str):
    # We use 'query' instead of 'scan' because it is much faster and cheaper 
    # when looking up a specific partition key (equipment_id)
    response = table.query(
        KeyConditionExpression=Key('equipment_id').eq(equipment_id)
    )
    return response.get('Items', [])