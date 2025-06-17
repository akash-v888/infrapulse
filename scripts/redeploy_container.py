import subprocess
import json
import os
import sys

TERRAFORM_DIR = "../terraform"
DOCKER_IMAGE = "aviswa/infrapulse:latest"
CONTAINER_NAME = "infra_pulse"
REMOTE_USER = "ec2-user"
DEFAULT_PORT = "80:5000"

def get_instance_ip():
    print("Fetching EC2 instance public IP from Terraform output...")
    result = subprocess.run(
        ["terraform", "output", "-json"],
        cwd=TERRAFORM_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Terraform output failed:\n{result.stderr}")
        sys.exit(1)

    try:
        outputs = json.loads(result.stdout)
        return outputs["instance_public_ip"]["value"]
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Failed to parse Terraform output: {e}")
        sys.exit(1)

def ssh_and_deploy(ip_address, key_path, user=REMOTE_USER):
    print(f"🚀 Connecting to {ip_address} and deploying container `{CONTAINER_NAME}`...")

    if not os.path.exists(key_path):
        print(f"SSH key not found: {key_path}")
        sys.exit(1)

    commands = [
        "sudo yum update -y",
        "sudo service docker start",
        f"sudo docker stop {CONTAINER_NAME} || true",
        f"sudo docker rm {CONTAINER_NAME} || true",
        f"sudo docker pull {DOCKER_IMAGE}",
        f"sudo docker run -d -p {DEFAULT_PORT} --name {CONTAINER_NAME} {DOCKER_IMAGE}"
    ]

    full_command = " && ".join(commands)
    ssh_command = ["ssh", "-i", key_path, f"{user}@{ip_address}", full_command]

    result = subprocess.run(ssh_command)

    if result.returncode == 0:
        print("Deployment successful.")
    else:
        print("Deployment failed. Check SSH connectivity and Docker state.")

if __name__ == "__main__":
    key_path = input("Enter path to your SSH private key (.pem): ").strip()
    public_ip = get_instance_ip()
    ssh_and_deploy(public_ip, key_path)
