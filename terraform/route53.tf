resource "aws_route53_record" "subdomain_record" {
  zone_id = "your-route53-hosted-zone-id"
  name    = # 하위 도메인 자리
  type    = "A"
  alias {
    name                   = aws_api_gateway_rest_api.network_api.id
    zone_id                = aws_api_gateway_rest_api.network_api.execution_arn
    evaluate_target_health = true
  }
}
