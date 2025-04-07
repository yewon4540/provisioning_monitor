provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_vpc" "default" {
  # 기존 VPC 지정
}

resource "aws_subnet" "private" {
  # 기존 서브넷 지정
}

resource "aws_security_group" "allow_sg" {
  # 기존 보안 그룹 지정
}
