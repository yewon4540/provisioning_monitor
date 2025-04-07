import json
import boto3

# SNS 클라이언트 생성
sns = boto3.client('sns')

def lambda_handler(event, context):
    # 메시지 작성 부분 -> 커스텀 필요 시 여기서 하거나, SNS에서 작성
    # message = event.get("message", "No message provided")
    
    # SNS 토픽 ARN
    topic_arn = 'arn:aws:sns:ap-northeast-2:123456789012:network-alert-topic'
    
    try:
        # SNS로 메시지 발송
        response = sns.publish(
            TopicArn=topic_arn,
            # Message=message,
            Subject='[경고] 네트워크 상태 이상 발생!'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Alert sent successfully')
        }
        
    except Exception as e:
        print(f"[❌] Error sending alert: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Failed to send alert: {e}")
        }
