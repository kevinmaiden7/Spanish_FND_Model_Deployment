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
                sudo apt install python3-pip python3-venv unrar -y
                EOF

    tags = {
        Name = "flask-web-app"
    }
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
        from_port = 5000
        to_port = 5000
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

output "instance_ip" {
  description = "The public ip for ssh access"
  value = aws_instance.ec2_instance.public_ip
}
