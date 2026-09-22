from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum
import boto3
from boto3.dynamodb.conditions import Key
import datetime

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/telemetry/{equipment_id}")
def get_data(equipment_id: str):
    response = table.query(
        KeyConditionExpression=Key('equipment_id').eq(equipment_id)
    )
    return response.get('Items', [])