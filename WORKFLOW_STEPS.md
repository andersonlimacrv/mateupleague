# 📋 Automated Deploy Setup with GitHub Actions

## Table of Contents

- [📋 Automated Deploy Setup with GitHub Actions](#-automated-deploy-setup-with-github-actions)
  - [Table of Contents](#table-of-contents)
- [👤 STEP 1: Create Deploy User on VPS](#-step-1-create-deploy-user-on-vps)
- [🔐 STEP 2: Generate and Configure SSH Keys](#-step-2-generate-and-configure-ssh-keys)
  - [Option A: Single Key (Simpler)](#option-a-single-key-simpler)
  - [Option B: Separate Keys (More Secure)](#option-b-separate-keys-more-secure)
- [🛠️ STEP 2.1: Configure Repository Permissions](#️-step-21-configure-repository-permissions)
- [🛠️ STEP 2.2: Configure Project Write Permissions](#️-step-22-configure-project-write-permissions)
- [🔗 STEP 3: Configure Deploy Key in GitHub](#-step-3-configure-deploy-key-in-github)
- [⚙️ STEP 4: Configure GitHub Secrets](#️-step-4-configure-github-secrets)
  - [For Single Key:](#for-single-key)
  - [For Separate Keys:](#for-separate-keys)
- [🔄 STEP 5: GitHub Actions Workflow](#-step-5-github-actions-workflow)
  - [Workflow for Single Key:](#workflow-for-single-key)
  - [Workflow for Separate Keys:](#workflow-for-separate-keys)
- [🧪 STEP 6: Testing the Configuration](#-step-6-testing-the-configuration)
  - [Manual Test on VPS:](#manual-test-on-vps)
  - [Local Test on PowerShell:](#local-test-on-powershell)
- [🔍 Detailed Troubleshooting](#-detailed-troubleshooting)
    - ["Permission denied (publickey)"](#permission-denied-publickey)
    - ["error: cannot open '.git/FETCH\_HEAD': Permission denied"](#error-cannot-open-gitfetch_head-permission-denied)
    - ["error: unable to create file .env.example: Permission denied"](#error-unable-to-create-file-envexample-permission-denied)
    - ["fatal: cannot create directory at '.github': Permission denied"](#fatal-cannot-create-directory-at-github-permission-denied)
    - ["fatal: detected dubious ownership"](#fatal-detected-dubious-ownership)
    - ["make: \*\*\* No rule to make target"](#make--no-rule-to-make-target)
    - ["Repository not found" or access denied](#repository-not-found-or-access-denied)
    - ["Host key verification failed"](#host-key-verification-failed)
- [✅ Validation Checklist](#-validation-checklist)

---

# 👤 STEP 1: Create Deploy User on VPS

**Run as root on the server:**

```bash
# Connect as root
ssh root@XXX.XX.XX.XX

# Create deploy user without password (SSH only)
adduser --disabled-password --gecos "" USER

# Add to docker group (if using containers)
usermod -aG docker USER

# Create .ssh directory with secure permissions
mkdir -p /home/USER/.ssh
chmod 700 /home/USER/.ssh
chown -R USER:USER /home/USER/.ssh
```

---

# 🔐 STEP 2: Generate and Configure SSH Keys

## Option A: Single Key (Simpler)

```bash
# Generate a single key for everything
sudo -u USER ssh-keygen -t ed25519 -f /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY -N ""

# Configure authorized_keys with the public key
cat /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY.pub > /home/USER/.ssh/authorized_keys
chmod 600 /home/USER/.ssh/authorized_keys
chown USER:USER /home/USER/.ssh/authorized_keys
```

## Option B: Separate Keys (More Secure)

```bash
# Key for SSH access to VPS
sudo -u USER ssh-keygen -t ed25519 -f /home/USER/.ssh/vps_access_key -N ""

# Key for git pull from GitHub
sudo -u USER ssh-keygen -t ed25519 -f /home/USER/.ssh/github_deploy_key -N ""

# Configure authorized_keys with access key only
cat /home/USER/.ssh/vps_access_key.pub > /home/USER/.ssh/authorized_keys
chmod 600 /home/USER/.ssh/authorized_keys
chown USER:USER /home/USER/.ssh/authorized_keys
```

**Security Notes:**

* `-t ed25519`: Modern secure algorithm
* `-N ""`: No passphrase for automation
* Permissions: `.ssh` (700), private keys (600), authorized_keys (600)

---

# 🛠️ STEP 2.1: Configure Repository Permissions

**If the repository was cloned as root, run:**

```bash
# Grant deploy user access to repository
chown -R USER:USER /home/USER/apps/your_project/.git
```

**Why this is required:**

* Prevents: `error: cannot open '.git/FETCH_HEAD': Permission denied`
* Ensures deploy user can run git commands

---

# 🛠️ STEP 2.2: Configure Project Write Permissions

**Grant full permissions to deploy user:**

```bash
# Give deploy user full ownership of project
chown -R USER:USER /home/USER/apps/your_project

# Ensure write permissions
find /home/USER/apps/your_project -type d -exec chmod 755 {} \;
find /home/USER/apps/your_project -type f -exec chmod 644 {} \;
```

**Why this is essential:**

* Allows deploy user to **create/update** files during git pull
* Prevents errors such as:

  * `error: unable to create file .env.example: Permission denied`
  * `fatal: cannot create directory at '.github': Permission denied`
* Ensures workflow can **write** to filesystem

---

# 🔗 STEP 3: Configure Deploy Key in GitHub

1. Open your repository → **Settings → Deploy Keys**
2. Click **Add deploy key**
3. Fill in:

   * **Title:** `vps-deploy-key`
   * **Key:** Insert public key:

     ```bash
     # Single key:
     cat /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY.pub

     # Separate keys:
     cat /home/USER/.ssh/github_deploy_key.pub
     ```
   * **✓ Allow write access**

---

# ⚙️ STEP 4: Configure GitHub Secrets

In repository → **Settings → Secrets and variables → Actions**

## For Single Key:

| Secret                 | Value                          | How to get                                         |
| ---------------------- | ------------------------------ | -------------------------------------------------- |
| `SSH_PRIVATE_KEY`      | Private key content            | `cat /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY` |
| `SSH_PRIVATE_KEY_NAME` | `name_of_file_SSH_PRIVATE_KEY` | File name                                          |
| `PUB_GITHUB_KEY_NAME`  | `name_of_file_SSH_PRIVATE_KEY` | Same name                                          |
| `VPS_HOST`             | `XXX.XX.XX.XX`                 | VPS IP                                             |
| `VPS_USER`             | `USER`                         | Deploy user                                        |
| `REPO_VPS`             | `/destination/to/your/project` | Project path                                       |

## For Separate Keys:

| Secret                 | Value                          | How to get                           |
| ---------------------- | ------------------------------ | ------------------------------------ |
| `SSH_PRIVATE_KEY`      | Private `vps_access_key`       | `cat /home/USER/.ssh/vps_access_key` |
| `SSH_PRIVATE_KEY_NAME` | `vps_access_key`               | Access key name                      |
| `PUB_GITHUB_KEY_NAME`  | `github_deploy_key`            | GitHub key name                      |
| `VPS_HOST`             | `XXX.XX.XX.XX`                 | VPS IP                               |
| `VPS_USER`             | `USER`                         | Deploy user                          |
| `REPO_VPS`             | `/destination/to/your/project` | Project path                         |

---

# 🔄 STEP 5: GitHub Actions Workflow

## Workflow for Single Key:

```yaml
name: 🚀 Deploy to VPS

on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy Application
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🔑 Setup SSH key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }}
          chmod 600 ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }}
          ssh-keyscan -H ${{ secrets.VPS_HOST }} >> ~/.ssh/known_hosts

      - name: 🚀Execute Deploy - via SSH
        run: |
          ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }} << 'EOF'
            set -e
            cd ${{ secrets.REPO_VPS }}

            export DOCKER_BUILDKIT=1
            export COMPOSE_DOCKER_CLI_BUILD=1

            GIT_SSH_COMMAND="ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} -o StrictHostKeyChecking=no" git pull origin main

            make test-make
          EOF
```

## Workflow for Separate Keys:

```yaml
name: 🚀 Deploy to VPS

on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy Application
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🔑 Setup SSH key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }}
          chmod 600 ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }}
          ssh-keyscan -H ${{ secrets.VPS_HOST }} >> ~/.ssh/known_hosts

      - name: 🚀 Execute Deploy - via SSH
        run: |
          ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }} << 'EOF'
            set -e
            cd ${{ secrets.REPO_VPS }}

            export DOCKER_BUILDKIT=1
            export COMPOSE_DOCKER_CLI_BUILD=1

            GIT_SSH_COMMAND="ssh -i ~/.ssh/${{ secrets.PUB_GITHUB_KEY_NAME }} -o StrictHostKeyChecking=no" git pull origin main

            make test-make
          EOF
```

---

# 🧪 STEP 6: Testing the Configuration

## Manual Test on VPS:

```bash
# GitHub authentication test
sudo -u USER ssh -i /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY -T git@github.com

# Configure safe directory
sudo -u USER git config --global --add safe.directory /destination/to/your/project

# Git pull test
sudo -u USER bash -c '
  cd /destination/to/your/project
  GIT_SSH_COMMAND="ssh -i ~/.ssh/name_of_file_SSH_PRIVATE_KEY -o StrictHostKeyChecking=no" git pull origin main
'
```

## Local Test on PowerShell:

```powershell
# Test SSH connection
ssh -i ~/.ssh/name_of_file_SSH_PRIVATE_KEY USER@XXX.XX.XX.XX "echo '✅ SSH connected' && whoami"

# Test project directory
ssh -i ~/.ssh/name_of_file_SSH_PRIVATE_KEY USER@XXX.XX.XX.XX "cd /destination/to/your/project && pwd && ls -la"
```

---

# 🔍 Detailed Troubleshooting

### "Permission denied (publickey)"

```bash
ls -la /home/USER/.ssh/
cat /home/USER/.ssh/authorized_keys
chmod 700 /home/USER/.ssh
chmod 600 /home/USER/.ssh/*
chown -R USER:USER /home/USER/.ssh
```

### "error: cannot open '.git/FETCH_HEAD': Permission denied"

```bash
chown -R USER:USER /home/USER/apps/your_project/.git
```

### "error: unable to create file .env.example: Permission denied"

```bash
chown -R USER:USER /home/USER/apps/your_project
find /home/USER/apps/your_project -type d -exec chmod 755 {} \;
find /home/USER/apps/your_project -type f -exec chmod 644 {} \;
```

### "fatal: cannot create directory at '.github': Permission denied"

```bash
chown -R USER:USER /home/USER/apps/your_project
find /home/USER/apps/your_project -type d -exec chmod 755 {} \;
```

### "fatal: detected dubious ownership"

```bash
git config --global --add safe.directory /destination/to/your/project
```

### "make: *** No rule to make target"

```bash
ls -la Makefile
make --help
```

### "Repository not found" or access denied

* Check if public key is in GitHub Deploy Keys
* Ensure **Allow write access** is enabled
* Confirm repository is private and the key has access

### "Host key verification failed"

```bash
ssh-keyscan -H github.com >> ~/.ssh/known_hosts
```

---

# ✅ Validation Checklist

* [ ] Deploy user created without password
* [ ] `.ssh` directory has correct permissions (700)
* [ ] SSH keys generated
* [ ] authorized_keys configured
* [ ] `.git` permissions fixed
* [ ] Project write permissions set
* [ ] Deploy Key added to GitHub
* [ ] All GitHub Secrets configured
* [ ] safe.directory configured
* [ ] Manual SSH test successful
* [ ] Manual git pull successful

---

