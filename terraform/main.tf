
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "infra_pulse_app" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 AMI (HVM), SSD Volume Type
  instance_type = "t2.micro"
  key_name      = "infrapulse-key"

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -a -G docker ec2-user
              docker run -d -p 80:5000 public.ecr.aws/docker/library/hello-world
              EOF

  tags = {
    Name = "InfraPulse-Flask-Server"
  }
}
