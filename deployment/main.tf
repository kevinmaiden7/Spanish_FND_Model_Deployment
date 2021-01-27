provider "aws" {
    region = "us-east-1"
}

resource "aws_instance" "ec2_instance" {
    ami = "ami-0885b1f6bd170450c" // Ubuntu Server 20.04 LTS
    instance_type = "t2.medium"
    vpc_security_group_ids = [aws_security_group.sec_group.id]
    associate_public_ip_address = true
    key_name = "flask-web-app-ec2"

    // some commands to run on boot
    user_data = <<-EOF
                #!/bin/bash
                sudo apt update
                sudo apt install python3-pip python3-venv unrar nginx -y
                EOF

    tags = {
        Name = "flask-web-app"
    }
}

variable "elastic_ip_id" {}

resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.ec2_instance.id
  allocation_id = var.elastic_ip_id
}

resource "aws_security_group" "sec_group" {
    name = "flask-web-app-sec_group"

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
