resource "aws_iam_role" "lambda_role" {
  name = "lambda-sns-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "sns_policy" {
  name        = "sns-policy"
  description = "Allow SNS Publish actions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "sns:Publish"
        Effect   = "Allow"
        Resource = aws_sns_topic.network_alerts.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_sns_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.sns_policy.arn
}

resource "aws_lambda_function" "network_alert_lambda" {
  function_name = "network-alert-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.8"

  s3_bucket = "your-bucket"
  s3_key    = "lambda/network-alerts.zip"
}
