data "aws_ami" "al2023" {
  owners=["137112412989"]; most_recent=true
  filter { name="name"; values=["al2023-ami-*-x86_64"] }
}
resource "aws_security_group" "sg" {
  vpc_id=data.aws_vpc.default.id
  ingress { from_port=80 to_port=80 protocol="tcp" cidr_blocks=["0.0.0.0/0"] }
  ingress { from_port=5000 to_port=5000 protocol="tcp" cidr_blocks=["0.0.0.0/0"] }
  ingress { from_port=9000 to_port=9000 protocol="tcp" cidr_blocks=["0.0.0.0/0"] }
  egress { from_port=0 to_port=0 protocol="-1" cidr_blocks=["0.0.0.0/0"] }
}
data "aws_vpc" "default" { default=true }
data "aws_subnets" "default" { filter { name="vpc-id" values=[data.aws_vpc.default.id] } }
resource "aws_instance" "app" {
  ami=data.aws_ami.al2023.id
  instance_type=var.instance_type
  subnet_id=data.aws_subnets.default.ids[0]
  vpc_security_group_ids=[aws_security_group.sg.id]
  user_data=templatefile("${path.module}/user_data.sh",{dockerhub_username=var.dockerhub_username,repo_url=var.repo_url})
}
