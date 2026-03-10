#!/usr/bin/env python
"""
Seed script: Add sample DevOps issues to Supabase

Usage:
    python seed_issues.py

Make sure to set SUPABASE_URL and SUPABASE_KEY in .env first
"""

import sys
from datetime import datetime

def seed_issues():
    """Add sample DevOps issues to Supabase"""
    
    try:
        import supabase_db
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Ensure supabase_db.py is available.")
        return False
    
    issues = [
        {
            "title": "Essential Linux Commands for DevOps Engineers",
            "content": """
# Essential Linux Commands for DevOps Engineers

## System Information
```bash
# Check system info
uname -a
lsb_release -a
cat /etc/os-release

# CPU and Memory
top
htop
free -h
df -h
```

## User & Permission Management
```bash
# Create user
sudo useradd -m -s /bin/bash username

# Add to sudo group
sudo usermod -aG sudo username

# Change permissions
chmod 755 filename
chown user:group filename

# Check sudo access
sudo -l
```

## Service Management
```bash
# Systemctl (systemd)
sudo systemctl start service_name
sudo systemctl stop service_name
sudo systemctl restart service_name
sudo systemctl status service_name
sudo systemctl enable service_name  # Auto-start
sudo systemctl disable service_name

# View logs
sudo journalctl -u service_name
sudo journalctl -u service_name -f  # Follow
```

## Network Commands
```bash
# Check ports
netstat -tuln
ss -tuln
lsof -i :8080

# DNS
nslookup example.com
dig example.com

# Network diagnostic
ping example.com
traceroute example.com
curl -I https://example.com
```

## File Operations
```bash
# Search
grep -r "pattern" /path
find /path -name "*.txt"
find /path -type f -mtime -7  # Modified last 7 days

# Archive
tar -czf backup.tar.gz /path
tar -xzf backup.tar.gz

# Copy over network
scp file user@host:/path
rsync -avz /source /dest
```

## Disk Usage
```bash
# Check disk space
du -sh /path
du -sh /* | sort -h

# Find large files
find / -type f -size +1G

# Clean up
sudo apt-get clean
sudo journalctl --vacuum=7d
```

---

**Pro Tips:**
- Use `man command` for help
- Combine commands with pipes `|` and redirects `>`
- Use aliases for frequently used commands: `alias ll='ls -la'`
- Always backup before making system changes
            """
        },
        {
            "title": "Docker Cheat Sheet for Container Management",
            "content": """
# Docker Cheat Sheet

## Basic Commands
```bash
# Check Docker version
docker --version

# View images
docker images
docker images --all

# View running containers
docker ps
docker ps -a  # All containers

# View container logs
docker logs container_id
docker logs -f container_id  # Follow
```

## Image Management
```bash
# Build image
docker build -t image_name:tag .
docker build -t myapp:1.0 --no-cache .

# Pull image
docker pull ubuntu:20.04
docker pull myregistry.com/myimage:latest

# Push image
docker tag myapp:1.0 myregistry.com/myapp:1.0
docker push myregistry.com/myapp:1.0

# Remove image
docker rmi image_name:tag
docker rmi image_id

# Image info
docker inspect image_id
docker history image_name
```

## Container Operations
```bash
# Run container
docker run -d -p 8080:80 --name my_container nginx

# Options explained:
# -d: Detached mode (background)
# -p: Port mapping (host:container)
# --name: Give container a name
# -e: Environment variable (-e KEY=value)
# -v: Volume mount (-v /host/path:/container/path)

# Enter container
docker exec -it container_name bash
docker exec -it container_name sh

# Copy files
docker cp container_name:/path/file ./local/path
docker cp ./local/file container_name:/path

# Stop/Start/Restart
docker stop container_name
docker start container_name
docker restart container_name

# Remove container
docker rm container_name
docker rm $(docker ps -aq)  # Remove all

# Container info
docker inspect container_name
docker stats container_name  # Resource usage
```

## Docker Compose
```bash
# Run services
docker-compose up -d

# View services
docker-compose ps

# View logs
docker-compose logs -f service_name

# Stop services
docker-compose down

# Rebuild images
docker-compose up -d --build
```

## Networking
```bash
# Create network
docker network create my_network

# Connect container to network
docker network connect my_network container_name

# View networks
docker network ls

# Inspect network
docker network inspect my_network
```

## Registry & Private Images
```bash
# Login to registry
docker login
docker login registry.example.com

# Logout
docker logout

# Tag and push
docker tag myapp:latest myregistry.com/myapp:latest
docker push myregistry.com/myapp:latest
```

---

**Pro Tips:**
- Use `.dockerignore` to exclude files (like `.gitignore`)
- Keep images small — remove unnecessary packages
- Use health checks: `HEALTHCHECK CMD curl --fail http://localhost/`
- Use multi-stage builds for smaller final images
            """
        },
        {
            "title": "Kubernetes (kubectl) Essential Commands",
            "content": """
# Kubernetes kubectl Commands

## Cluster Information
```bash
# Cluster info
kubectl cluster-info
kubectl version
kubectl get nodes
kubectl describe node node_name

# Current context
kubectl config current-context
kubectl config get-contexts
kubectl config use-context context_name
```

## Pods
```bash
# List pods
kubectl get pods
kubectl get pods -n namespace
kubectl get pods -o wide  # Detailed

# Pod details
kubectl describe pod pod_name
kubectl logs pod_name
kubectl logs pod_name -c container_name  # Specific container
kubectl logs pod_name -f  # Follow

# Execute command in pod
kubectl exec -it pod_name -- bash
kubectl exec -it pod_name -- sh -c "command"

# Port forward
kubectl port-forward pod_name 8080:80

# Create pod
kubectl run nginx --image=nginx:latest
```

## Deployments
```bash
# List deployments
kubectl get deployments
kubectl get deploy -o wide

# Create deployment
kubectl create deployment my_app --image=myapp:1.0

# Apply YAML
kubectl apply -f deployment.yaml

# Update deployment
kubectl set image deployment/my_app my_app=myapp:2.0
kubectl rollout restart deployment/my_app

# Scale deployment
kubectl scale deployment my_app --replicas=3

# Check rollout status
kubectl rollout status deployment/my_app
kubectl rollout history deployment/my_app
kubectl rollout undo deployment/my_app  # Rollback
```

## Services
```bash
# List services
kubectl get services
kubectl get svc

# Service details
kubectl describe service service_name

# Expose deployment
kubectl expose deployment my_app --type=LoadBalancer --port=80 --target-port=8080
```

## ConfigMaps & Secrets
```bash
# Create ConfigMap
kubectl create configmap my_config --from-literal=key=value

# Create Secret
kubectl create secret generic my_secret --from-literal=password=secret123

# View ConfigMaps
kubectl get configmap
kubectl describe configmap my_config

# View Secrets
kubectl get secrets
kubectl describe secret my_secret
```

## Namespaces
```bash
# List namespaces
kubectl get namespaces

# Create namespace
kubectl create namespace my_namespace

# Use namespace by default
kubectl config set-context --current --namespace=my_namespace

# Delete namespace
kubectl delete namespace my_namespace
```

## Debugging
```bash
# Pod events
kubectl describe pod pod_name

# Check pod status
kubectl get pod pod_name -o yaml

# View resource usage
kubectl top nodes
kubectl top pods

# Get events
kubectl get events

# Tail logs
kubectl logs pod_name --tail=100
kubectl logs pod_name --since=1h
```

## Cleanup
```bash
# Delete pod
kubectl delete pod pod_name

# Delete deployment
kubectl delete deployment deployment_name

# Delete all in namespace
kubectl delete all --all -n my_namespace

# Delete with selector
kubectl delete pods -l app=my_app
```

---

**Pro Tips:**
- Use `kubectl alias k='kubectl'` for faster typing
- Use `-n namespace` to work with specific namespaces
- Use `--dry-run=client -o yaml` to preview changes
- Read YAML outputs with `-o yaml` for debugging
            """
        },
        {
            "title": "Git Commands Every Developer Needs",
            "content": """
# Git Commands Cheat Sheet

## Setup & Configuration
```bash
# Global configuration
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# View config
git config --list
git config user.name
```

## Basic Workflow
```bash
# Clone repository
git clone https://github.com/user/repo.git
git clone --depth 1 https://github.com/user/repo.git  # Shallow

# Check status
git status
git status -s  # Short format

# Add changes
git add filename
git add .  # Add all

# Commit
git commit -m "commit message"
git commit -am "commit message"  # Stage & commit tracked files

# Push to remote
git push origin branch_name
git push -u origin branch_name  # Set upstream
```

## Branching
```bash
# List branches
git branch
git branch -a  # All (local + remote)
git branch -v  # With last commit

# Create branch
git branch new_branch
git checkout -b new_branch  # Create & switch

# Switch branch
git checkout branch_name
git switch branch_name  # Newer syntax

# Delete branch
git branch -d branch_name
git branch -D branch_name  # Force delete

# Rename branch
git branch -m old_name new_name
```

## Viewing History
```bash
# View commits
git log
git log --oneline  # Compact
git log --graph --oneline --all  # Visual graph
git log -n 5  # Last 5 commits
git log --author="name"
git log --since="2 weeks ago"

# View changes
git diff
git diff branch1 branch2
git show commit_hash

# View file history
git log -- filename
git blame filename  # Who changed what
```

## Undoing Changes
```bash
# Discard local changes
git checkout -- filename
git restore filename  # Newer syntax

# Unstage file
git reset filename
git reset HEAD filename  # Older syntax

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert commit (create new commit)
git revert commit_hash

# Stash changes
git stash
git stash list
git stash pop
```

## Merging & Rebasing
```bash
# Merge branch
git merge branch_name

# Rebase
git rebase branch_name

# Interactive rebase
git rebase -i HEAD~3  # Last 3 commits

# Abort rebase
git rebase --abort
```

## Remote Operations
```bash
# View remotes
git remote
git remote -v  # Verbose

# Add remote
git remote add origin https://github.com/user/repo.git

# Remove remote
git remote remove origin

# Fetch from remote
git fetch origin

# Pull (fetch + merge)
git pull origin branch_name

# Push specific branch
git push origin branch_name

# Delete remote branch
git push origin --delete branch_name
```

## Tagging
```bash
# Create tag
git tag v1.0.0

# Annotated tag
git tag -a v1.0.0 -m "Release 1.0.0"

# List tags
git tag

# Push tag
git push origin tag_name
git push origin --tags  # All tags

# Delete tag
git tag -d tag_name
git push origin --delete tag_name
```

## Advanced
```bash
# Cherry-pick commit
git cherry-pick commit_hash

# Amend last commit
git commit --amend

# Search commits
git log -S "search_text"

# Bisect (find bad commit)
git bisect start
git bisect bad
git bisect good commit_hash
git bisect reset

# Ignore tracked file
git rm --cached filename
git update-index --skip-worktree filename
```

---

**Pro Tips:**
- Write clear commit messages (present tense, describe what changed)
- Pull before push to avoid conflicts
- Create branches for features/fixes
- Commit frequently with logical, atomic changes
- Use `.gitignore` to exclude unnecessary files
            """
        },
        {
            "title": "AWS CLI Essential Commands",
            "content": """
# AWS CLI Quick Reference

## Setup & Configuration
```bash
# Configure AWS credentials
aws configure

# View configuration
aws configure list

# Set profile
export AWS_PROFILE=my_profile
aws ec2 describe-instances --profile my_profile

# Check credentials
aws sts get-caller-identity
```

## EC2 (Compute)
```bash
# List instances
aws ec2 describe-instances
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]'

# Start/Stop instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Reboot instance
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# Terminate instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Create security group
aws ec2 create-security-group --group-name my_group --description "My security group"

# Authorize security group
aws ec2 authorize-security-group-ingress --group-id sg-12345678 --protocol tcp --port 80 --cidr 0.0.0.0/0
```

## S3 (Storage)
```bash
# List buckets
aws s3 ls

# List contents
aws s3 ls s3://my-bucket/

# Upload file
aws s3 cp my_file.txt s3://my-bucket/

# Download file
aws s3 cp s3://my-bucket/my_file.txt ./

# Sync directory
aws s3 sync ./local_dir s3://my-bucket/remote_dir
aws s3 sync s3://my-bucket/remote_dir ./local_dir

# Remove object
aws s3 rm s3://my-bucket/my_file.txt

# Create bucket
aws s3 mb s3://my-new-bucket

# Delete bucket
aws s3 rb s3://my-bucket --force
```

## RDS (Database)
```bash
# List RDS instances
aws rds describe-db-instances

# Get instance details
aws rds describe-db-instances --db-instance-identifier my-db

# Create RDS instance
aws rds create-db-instance --db-instance-identifier my-db --db-instance-class db.t2.micro --engine mysql --master-username admin

# Start instance
aws rds start-db-instance --db-instance-identifier my-db

# Stop instance
aws rds stop-db-instance --db-instance-identifier my-db

# Create snapshot
aws rds create-db-snapshot --db-snapshot-identifier my-snapshot --db-instance-identifier my-db
```

## CloudWatch (Monitoring)
```bash
# List alarms
aws cloudwatch describe-alarms

# Get metrics
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --start-time 2024-01-01T00:00:00Z --end-time 2024-01-02T00:00:00Z --period 3600 --statistics Average

# Get logs
aws logs describe-log-groups
aws logs tail /aws/lambda/my-function --follow
```

## IAM (Access)
```bash
# List users
aws iam list-users

# List policies
aws iam list-policies

# Get user info
aws iam get-user --user-name my_user

# Create access key
aws iam create-access-key --user-name my_user

# Attach policy
aws iam attach-user-policy --user-name my_user --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
```

## CloudFormation
```bash
# List stacks
aws cloudformation list-stacks

# Create stack
aws cloudformation create-stack --stack-name my-stack --template-body file://template.yaml

# Update stack
aws cloudformation update-stack --stack-name my-stack --template-body file://template.yaml

# Delete stack
aws cloudformation delete-stack --stack-name my-stack

# Get stack status
aws cloudformation describe-stacks --stack-name my-stack
```

## Lambda
```bash
# List functions
aws lambda list-functions

# Get function
aws lambda get-function --function-name my-function

# Invoke function
aws lambda invoke --function-name my-function response.json

# Update code
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip

# Get logs
aws logs tail /aws/lambda/my-function --follow
```

---

**Pro Tips:**
- Use `--query` and `--output` for filtering results
- Set AWS_DEFAULT_REGION to avoid specifying region repeatedly
- Use `aws s3 sync` instead of individual cp for bulk operations
- Use IAM roles instead of hardcoded credentials
- Regular snapshots for databases and important data
            """
        }
    ]
    
    try:
        print("🌱 Seeding DevOps issues to Supabase...\n")
        
        supabase_db.init_database()
        client = supabase_db.get_client()
        
        for i, issue in enumerate(issues, 1):
            try:
                result = client.table("issues").insert({
                    "title": issue["title"],
                    "content": issue["content"],
                    "published_date": datetime.now().strftime("%B %d, %Y"),
                    "created_at": datetime.now().isoformat()
                }).execute()
                
                if result.data:
                    print(f"  ✅ Issue {i}: {issue['title']}")
                else:
                    print(f"  ⚠️  Issue {i} may have failed")
            except Exception as e:
                print(f"  ❌ Issue {i} failed: {e}")
        
        print(f"\n✅ Seeded {len(issues)} DevOps issues!")
        print("\n📝 Next steps:")
        print("   1. Go to your app and check Latest Article page")
        print("   2. Browse Archive to see all issues")
        print("   3. Issues are now live in your Supabase database")
        
        return True
    
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = seed_issues()
    sys.exit(0 if success else 1)
