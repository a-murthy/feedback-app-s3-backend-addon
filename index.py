import os
import json
import boto3
from datetime import datetime

# Initialize the AWS NLP, Systems Manager, and Storage clients natively
comprehend = boto3.client('comprehend', region_name='us-east-1')
ssm        = boto3.client('ssm', region_name='us-east-1')
s3         = boto3.client('s3', region_name='us-east-1')

PARAMETER_NAME = "/platform/maintenance_mode"
BUCKET_NAME    = os.environ.get('ARCHIVE_BUCKET_NAME')

def get_maintenance_state():
    try:
        response = ssm.get_parameter(Name=PARAMETER_NAME)
        return str(response['Parameter']['Value']).strip().lower() == 'true'
    except Exception as e:
        print(f"SSM Parameter Read Block (Defaulting to Normal Operations): {str(e)}")
        return False

def handler(event, context):
    print("--- DUAL-TIER DURABLE STORAGE & AI ADD-ON INVOCATION DETECTED ---")
    
    # 1. Extract the deterministic HTTP method from the AWS proxy wrapper context
    http_method = event.get('requestContext', {}).get('http', {}).get('method', '')
    if not http_method and isinstance(event, dict):
        http_method = event.get('httpMethod', event.get('requestContext', {}).get('stage', 'POST'))

    # 2. BULLETPROOF UNPACKING: Flatten event data cleanly across proxy and direct activations
    payload_data = {}
    
    if isinstance(event, dict) and event.get('body'):
        try:
            payload_data = json.loads(event['body'])
        except Exception:
            pass
            
    if not payload_data and isinstance(event, dict):
        payload_data = event

    if not isinstance(payload_data, dict):
        payload_data = {}

    # ==============================================================================
    # 🚨 LIFECYCLE ROUTE 1: DAY 2 PLATFORM MAINTENANCE TOGGLE (HCP UI Actions)
    # ==============================================================================
    if "maintenance_mode" in payload_data:
        flag = str(payload_data.get("maintenance_mode", "false")).lower().strip()
        ssm.put_parameter(Name=PARAMETER_NAME, Value=flag, Type='String', Overwrite=True)
        is_active = (flag == 'true')
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'status': 'SUCCESS',
                'maintenance_mode': 'true' if is_active else 'false',
                'maintenance_mode_active': is_active
            })
        }

    # ==============================================================================
    # 🚨 LIFECYCLE ROUTE 2: IN-BAND RUNTIME OVERLAYS (Flask Traffic Channeling)
    # ==============================================================================
    
    # A. Page Loads (HTTP GET Check)
    if str(http_method).upper() == 'GET':
        current_lockout_state = get_maintenance_state()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'maintenance_mode': 'true' if current_lockout_state else 'false'})
        }

    # B. Form Submissions (HTTP POST Check - Evaluates AI & Streams to S3 simultaneously)
    text_to_analyze = str(payload_data.get("text", "")).strip()
    if not text_to_analyze:
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'status': 'SUCCESS', 'sentiment': '🟡 NEUTRAL'})
        }

    # Parallel Execution Track 1: Natural Language Sentiment Analysis
    try:
        comprehend_response = comprehend.detect_sentiment(Text=text_to_analyze, LanguageCode='en')
        detected_sentiment = comprehend_response.get('Sentiment', 'NEUTRAL')
        
        mapped_badge = f"🟡 {detected_sentiment}"
        if detected_sentiment == "POSITIVE": mapped_badge = "🟢 POSITIVE"
        if detected_sentiment == "NEGATIVE": mapped_badge = "🔴 NEGATIVE"
    except Exception as e:
        print(f"Amazon Comprehend API Exception: {str(e)}")
        mapped_badge = "🟡 NEUTRAL"

    # Parallel Execution Track 2: Real-time Immutable S3 Payload Archive Injection
    try:
        if BUCKET_NAME:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"feedback_records/archive_{timestamp}.json",
                Body=json.dumps({
                    "application_origin": os.environ.get('APP_NAME', 'feedback-app'),
                    "captured_at": timestamp,
                    "feedback_data": text_to_analyze,
                    "status": "ARCHIVED_SUCCESSFULLY"
                }, indent=2),
                ContentType='application/json'
            )
    except Exception as s3_err:
        print(f"S3 Compliance Archival Stream Failure: {str(s3_err)}")

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'status': 'SUCCESS', 'sentiment': mapped_badge})
    }
