resource "aws_lb" "network_monitor_alb" {
  name               = "network-monitor-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.allow_sg.id]
  subnets            = [aws_subnet.private.id]

  enable_deletion_protection = false

  tags = {
    Name = "NetworkMonitorALB"
  }
}

resource "aws_lb_target_group" "network_monitor_target_group" {
  name     = "network-monitor-target-group"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.default.id

  health_check {
    protocol = "HTTP"
    path     = "/"
    port     = 5000
  }
}

resource "aws_lb_listener" "network_monitor_listener" {
  load_balancer_arn = aws_lb.network_monitor_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.network_monitor_target_group.arn
  }
}
