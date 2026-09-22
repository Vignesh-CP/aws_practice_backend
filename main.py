from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import boto3
import datetime

app = FastAPI()
handler = Mangum(app)

# 1. Connect to our DynamoDB table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EquipmentTelemetry')

# 2. Define the expected incoming JSON data format
class TelemetryData(BaseModel):
    equipment_id: str
    temperature: int
    status: str

# 3. Create the POST endpoint
@app.post("/telemetry")
def receive_data(data: TelemetryData):
    # Generate a current timestamp
    current_time = datetime.datetime.utcnow().isoformat()
    
    # 4. Save the record to the database
    table.put_item(
        Item={
            'equipment_id': data.equipment_id,
            'timestamp': current_time,
            'temperature': data.temperature,
            'status': data.status
        }
    )
    
    return {"message": "Data saved successfully", "equipment_id": data.equipment_id}