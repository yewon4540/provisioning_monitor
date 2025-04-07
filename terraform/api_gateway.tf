resource "aws_api_gateway_rest_api" "network_api" {
  name        = "network-api"
  description = "API to handle network alerts"
}

resource "aws_api_gateway_resource" "alerts_resource" {
  rest_api_id = aws_api_gateway_rest_api.network_api.id
  parent_id   = aws_api_gateway_rest_api.network_api.root_resource_id
  path_part   = "alerts"
}

resource "aws_api_gateway_method" "alerts_method" {
  rest_api_id   = aws_api_gateway_rest_api.network_api.id
  resource_id   = aws_api_gateway_resource.alerts_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "alerts_response" {
  rest_api_id = aws_api_gateway_rest_api.network_api.id
  resource_id = aws_api_gateway_resource.alerts_resource.id
  http_method = aws_api_gateway_method.alerts_method.http_method
  status_code = "200"
}

resource "aws_api_gateway_integration" "alerts_integration" {
  rest_api_id             = aws_api_gateway_rest_api.network_api.id
  resource_id             = aws_api_gateway_resource.alerts_resource.id
  http_method             = aws_api_gateway_method.alerts_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.network_alert_lambda.invoke_arn
}

resource "aws_api_gateway_method_settings" "alerts_method_settings" {
  rest_api_id = aws_api_gateway_rest_api.network_api.id
  stage_name  = "$default"
  method_path = "alerts/POST"

  settings {
    ip_address_source = "0.0.0.0/0" # 제한 범위 지정
  }
}
