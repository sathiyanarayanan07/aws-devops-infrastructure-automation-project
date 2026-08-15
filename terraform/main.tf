resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16"


tags = {
    Name = "devops-project-vpc"
    }
}

resource "aws_subnet" "public" {
    vpc_id = aws_vpc.main.id
    cidr_block ="10.0.1.0/24"
    availability_zone = "ap-south-1a"
    map_public_ip_on_launch = true

    tags = {
        Name = "devops-public-subnet"
    }
}

resource "aws_internet_gateway" "main" {
    vpc_id = aws_vpc.main.id

    tags = {
        Name = "devops-project-igw"
    }
}

resource "aws_route_table" "public" {
    vpc_id = aws_vpc.main.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.main.id
    }

    tags = {
        Name = "devops-public-route-table"
    }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}


resource "aws_security_group" "app" {
    name = "devops-app-sg"
    description = "Allow SSH and application traffic"
    vpc_id = aws_vpc.main.id


    ingress {
        description = "SSH"
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        description = "flask application"
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

    tags = {
        name = "devops-app-sg"
    }
}

resource "aws_instance" "app" {
  ami           = "ami-01a00762f46d584a1"
  instance_type = "t2.micro"
  key_name = aws_key_pair.devops.key_name


  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.app.id]
  associate_public_ip_address = true

  tags = {
    Name = "devops-app-server"
  }
}

resource "aws_key_pair" "devops" {
    key_name = "devops-ec2-key"
    public_key = file("~/.ssh/devops-ec2.pub")

    tags = {
        Name = "devops-ec2-key"
    }
}

resource "local_file" "ansible_inventory" {
  filename = "${path.module}/../Ansible/inventory"
  content = templatefile("${path.module}/inventory.tftpl", {
    public_ip = aws_instance.app.public_ip
  })
}