"""nums =list(range(5))
for iter in nums:
    print(iter)

servers ={"server1","server2","server3","server4"}    
#servers =["server1","server2","server3","server4"]
for server in servers:
    print(f"deploying server: {server}")

squaring = [x*x for x in range(5)]
print(squaring)

matrix =[[1,2],[3,4]]
print(matrix)

config ={"host":"local host","port":30,"NameFirstchar":'a'}

print(config["NameFirstchar"])
print(config)

inventory ={ "webs":{"count":3},"db":{"count":2}}
print(inventory["webs"])

evens ={x for x in range(10) if x%2 ==0}
print(evens)

from collections import defaultdict
log_count = defaultdict(int)
log_count["error"] += 1
log_count["info"] +=3

print(log_count)
""" 


file_path ='log_content'
output_log_path ='summarylog.txt'
error_count =0
warning_count =0
info_count =0

def read_log_file(file_path):
    #Reads the server log file and returns the lines as a list.
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def summarize_logs(log_lines):
    #Summarizes INFO, WARNING, and ERROR counts from the logs.
    summary = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    
    for line in log_lines:
        line = line.strip()
        if line.startswith("INFO"):
            summary["INFO"] += 1
        elif line.startswith("WARNING"):
            summary["WARNING"] += 1
        elif line.startswith("ERROR"):
            summary["ERROR"] += 1
    
    return summary

def print_summary(summary):
    #Prints the summarized log information.
    print("\nLog Summary Report")
    print("===================")
    for key, value in summary.items():
        print(f"{key}: {value}")

def write_summary_to_file(summary, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write("Log Summary Report\n")
            file.write("===================\n")
            for key, value in summary.items():
                file.write(f"{key}: {value}\n")
        print(f"Summary written to {output_file}")
    except Exception as e:
        print(f"Failed to write summary: {e}")


# Usage Example:
#log_summary = {"INFO": 4, "WARNING": 2, "ERROR": 3}


if __name__ == "__main__":
    log_file_path = "server.log"
    log_lines = read_log_file(log_file_path)
    log_summary = summarize_logs(log_lines)
    print_summary(log_summary)
    write_summary_to_file(log_summary, "summary.txt")

with open("summary.txt" ,"r") as file:
    contentsummary =file.read()
print("open file summary.txt ->content")
print(contentsummary)   

"""
✅ Theory: Where & How Python is Used in DevOps in Real IT Companies
🔧 Why Python for DevOps?
Python is widely adopted in DevOps because it's:

Simple & readable (good for automation)

Rich ecosystem (Ansible, Fabric, Boto3, Requests, etc.)

Easily integrates with cloud platforms (AWS, Azure, GCP)

Supports APIs, CLI automation, log processing, monitoring, etc.

📌 Where DevOps Engineers Use Python:
🔥 DevOps Task	✅ How Python Helps (Real Industry Use)
Infrastructure Automation	Write custom scripts for provisioning, scaling, etc. (Ansible, Terraform integrations)
Configuration Management	Automate OS, services setup (ssh, subprocess, paramiko)
CI/CD Pipelines	Automate testing, build pipelines (Jenkins, GitHub Actions, GitLab CI integrations via APIs)
Cloud Operations (AWS/GCP/Azure)	Automate resources (Boto3 for AWS, google-cloud-python)
Monitoring & Alerts	Custom monitoring scripts (Logs, APIs, Metrics collection)
Log Analysis & Reporting	Parsing logs, error detection, generating reports (File I/O, Regex, JSON)
Networking Automation	Automate network device configs (Netmiko, NAPALM)
Security Automation (DevSecOps)	Scan vulnerabilities, patching reports (API, requests)
Container Orchestration	Write utilities for Kubernetes, Docker (client libraries)
Backup & Disaster Recovery	Automate backups, storage management (file ops, boto3)
ChatOps / Notifications	Send messages to Slack, MS Teams (webhooks, APIs)

🎯 Strategic DevOps + Python Learning Syllabus (Industry Aligned)
🛠️ Phase 1: Python Fundamentals (Strong Foundation)
📅 Duration: 1 Month

Topics	Focus
Variables, Data Types	Lists, Dicts, Sets, Tuples
Loops, Conditionals	Control Flow
Functions	Lambda, Scope
File I/O	CSV, JSON, Log files
Exception Handling	Error handling best practices
OOP Basics	Classes for Tooling / Scripts

⚙️ Phase 2: DevOps Core Tools (Toolchain Knowledge)
📅 Duration: 1-1.5 Months

Category	Tools You Must Learn
Version Control	Git, GitHub / GitLab
CI/CD	Jenkins, GitHub Actions, GitLab CI
Containers	Docker, Docker Compose
Orchestration	Kubernetes (kubectl, Helm, manifests)
Infra as Code	Terraform, Ansible (Python extensions)
Monitoring	Prometheus, Grafana, ELK Stack
Artifact Mgmt	Nexus, Artifactory

☁️ Phase 3: Python + Cloud (Industry Standard Practices)
📅 Duration: 1 Month

Cloud Provider	Key Python Libraries	Practical Automation Examples
AWS	boto3	EC2, S3, CloudWatch automation
Azure	azure SDK	VMs, Blob, Networking
GCP	google-cloud-storage	Compute Engine, Buckets

🔗 Phase 4: Real-World DevOps Python Projects
📅 Duration: 1-1.5 Months

Project Type	Skills Practiced
Log Analyzer	File I/O, Regex, Reporting
Health Check API Monitor	Requests, APIs, Alerts via Slack / Email
Automated Backup	Scheduling, File Ops, Cloud Storage
Container Cleanup Utility	Docker SDK, subprocess, Automation
Pipeline Custom Script	Jenkins API, GitHub API
Cloud Infra Reports	AWS Boto3, CSV reports of infra status

🔒 Phase 5: DevSecOps + Security Automation (Optional But Important)
📅 Duration: 1 Month

Security Focus	Python Use
Vulnerability Scanning	Automate nmap, openvas, qualys reports parsing
Dependency Checks	Automate safety, bandit, trivy output parsing
Alerting & Reporting	Python scripts for generating dashboards / alerts

🏁 Deliverables at the End:
Portfolio of 5+ Practical Automation Projects

Hands-on with CI/CD, Cloud, Monitoring

Python skills aligned to DevOps Engineer expectations

Ready to answer real-world scenario-based interviews

🚀 Industry-Ready DevOps + Python Schema (Visual Flow)
plaintext
Copy
Edit
Python Basics 
    └── File / OS Automation (I/O, logs)
        └── DevOps Tools (Git, Jenkins, Docker, K8s)
            └── Cloud Ops (AWS, Azure, GCP + Python SDK)
                └── Monitoring, Metrics, Security Scripting
                    └── Real-World Automation Projects (CI/CD, Infra, Alerts)
📚 Final Advice:
Theory alone is useless — Build projects continuously.

Focus on automation mindset — think scripts over manual work.

Be ready for scenario-based interviews (e.g., "How will you automate logs cleanup on 100 servers?").

If you'd like, I can prepare this as:

A PDF study plan

A detailed daily/week-wise roadmap

A project checklist

Tell me what format helps you best.
"""

server_log =("192.168.1.10",22)

host,port =server_log
print(server_log.__contains__(host)) 
print(server_log.__class_getitem__(host)) 
print(f"COnnecting to {host} on port:{port} secure: (SSH)")
