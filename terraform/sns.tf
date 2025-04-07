resource "aws_sns_topic" "network_alerts" {
  name = "network-alerts"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.network_alerts.arn
  protocol  = "email"
  endpoint  = "your-email@example.com"  # 이메일 주소 설정
}
