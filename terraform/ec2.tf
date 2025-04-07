resource "aws_instance" "network_monitor" {
  ami           = "ami-xxxxxxxxxx"  
  instance_type = "t2.medium"       
  subnet_id     = aws_subnet.private.id
  security_group = aws_security_group.allow_sg.id
  key_name      = "your-ssh-key-name"  

  tags = {
    Name = "NetworkMonitor"
  }

  # user_data 추가 필요
}
