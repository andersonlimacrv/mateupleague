# 📋 Configuração de Deploy Automatizado com GitHub Actions

## 👤 STEP 1: Criar Usuário Deploy na VPS

**Execute como root no servidor:**

```bash
# Conectar como root
ssh root@XXX.XX.XX.XX

# Criar usuário deploy sem senha (apenas SSH)
adduser --disabled-password --gecos "" USER

# Adicionar ao grupo docker (se usar containers)
usermod -aG docker USER

# Criar diretório .ssh com permissões seguras
mkdir -p /home/USER/.ssh
chmod 700 /home/USER/.ssh
chown -R USER:USER /home/USER/.ssh
```

---

## 🔐 STEP 2: Gerar e Configurar Chaves SSH

### **Opção A: Usar Mesma Chave (Mais Simples)**
```bash
# Gerar uma única chave para tudo
sudo -u USER ssh-keygen -t ed25519 -f /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY -N ""

# Configurar authorized_keys com a chave pública
cat /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY.pub > /home/USER/.ssh/authorized_keys
chmod 600 /home/USER/.ssh/authorized_keys
chown USER:USER /home/USER/.ssh/authorized_keys
```

### **Opção B: Chaves Separadas (Mais Seguro)**
```bash
# Chave para acesso SSH à VPS
sudo -u USER ssh-keygen -t ed25519 -f /home/USER/.ssh/vps_access_key -N ""

# Chave para git pull no GitHub  
sudo -u USER ssh-keygen -t ed25519 -f /home/USER/.ssh/github_deploy_key -N ""

# Configurar authorized_keys apenas com a chave de acesso
cat /home/USER/.ssh/vps_access_key.pub > /home/USER/.ssh/authorized_keys
chmod 600 /home/USER/.ssh/authorized_keys
chown USER:USER /home/USER/.ssh/authorized_keys
```

**📝 Notas de Segurança:**
- `-t ed25519`: Algoritmo moderno e seguro
- `-N ""`: Sem senha para automação
- Permissões: `.ssh` (700), chaves privadas (600), authorized_keys (600)

---

## 🛠️ STEP 2.1: Configurar Permissões do Repositório Git

**⚠️ CRÍTICO: Se o repositório foi clonado como root, execute:**

```bash
# Dar permissão ao usuário deploy para acessar o repositório
chown -R USER:USER /home/USER/apps/your_project/.git
```

**Por que isso é necessário:**
- Evita erro: `error: cannot open '.git/FETCH_HEAD': Permission denied`
- Garante que o usuário deploy possa executar comandos git

---

## 🛠️ STEP 2.2: Configurar Permissões de Escrita do Projeto

**⚠️ CRÍTICO: Dar permissão completa ao usuário deploy no projeto**

```bash
# Dar ownership COMPLETO do projeto ao usuário deploy
chown -R USER:USER /home/USER/apps/your_project

# Garantir permissões de escrita em diretórios e arquivos
find /home/USER/apps/your_project -type d -exec chmod 755 {} \;
find /home/USER/apps/your_project -type f -exec chmod 644 {} \;
```

**🎯 POR QUE ESTE PASSO É ESSENCIAL:**
- Permite ao usuário deploy **criar/atualizar** arquivos durante o git pull
- Evita erros como:
  - `error: unable to create file .env.example: Permission denied`
  - `fatal: cannot create directory at '.github': Permission denied`
- Garante que o workflow consiga **escrever** no sistema de arquivos

---

## 🔗 STEP 3: Configurar Deploy Key no GitHub

1. **Acesse seu repositório** → **Settings** → **Deploy Keys**
2. **Clique em:** "Add deploy key"
3. **Configure:**
   - **Title:** `vps-deploy-key`
   - **Key:** Cole o conteúdo da chave pública:
     ```bash
     # Para chave única:
     cat /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY.pub
     
     # Para chaves separadas:
     cat /home/USER/.ssh/github_deploy_key.pub
     ```
   - **✓ Allow write access:** MARQUE esta opção

---

## ⚙️ STEP 4: Configurar GitHub Secrets

No repositório GitHub → **Settings** → **Secrets and variables** → **Actions**

### **Para Chave Única:**
| Secret | Valor | Como obter |
|--------|-------|------------|
| `SSH_PRIVATE_KEY` | Conteúdo da chave privada | `cat /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY` |
| `SSH_PRIVATE_KEY_NAME` | `name_of_file_SSH_PRIVATE_KEY` | Nome do arquivo |
| `PUB_GITHUB_KEY_NAME` | `name_of_file_SSH_PRIVATE_KEY` | Mesmo nome |
| `VPS_HOST` | `XXX.XX.XX.XX` | IP da VPS |
| `VPS_USER` | `USER` | Usuário deploy |
| `REPO_VPS` | `/destination/to/your/project` | Caminho do projeto |

### **Para Chaves Separadas:**
| Secret | Valor | Como obter |
|--------|-------|------------|
| `SSH_PRIVATE_KEY` | Conteúdo de `vps_access_key` | `cat /home/USER/.ssh/vps_access_key` |
| `SSH_PRIVATE_KEY_NAME` | `vps_access_key` | Nome da chave de acesso |
| `PUB_GITHUB_KEY_NAME` | `github_deploy_key` | Nome da chave GitHub |
| `VPS_HOST` | `XXX.XX.XX.XX` | IP da VPS |
| `VPS_USER` | `USER` | Usuário deploy |
| `REPO_VPS` | `/destination/to/your/project` | Caminho do projeto |

---

## 🔄 STEP 5: Workflow GitHub Actions

### **Workflow para Chave Única:**
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
            
            # Usa mesma chave para git pull
            GIT_SSH_COMMAND="ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} -o StrictHostKeyChecking=no" git pull origin main
            
            make test-make
          EOF
```

### **Workflow para Chaves Separadas:**
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
            
            # Usa chave específica para GitHub
            GIT_SSH_COMMAND="ssh -i ~/.ssh/${{ secrets.PUB_GITHUB_KEY_NAME }} -o StrictHostKeyChecking=no" git pull origin main
            
            make test-make
          EOF
```

---

## 🧪 STEP 6: Testar a Configuração

### **Teste Manual na VPS:**
```bash
# Testar autenticação GitHub
sudo -u USER ssh -i /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY -T git@github.com
# Saída esperada: Hi username/repo! You've successfully authenticated...

# Configurar safe directory
sudo -u USER git config --global --add safe.directory /destination/to/your/project

# Testar git pull
sudo -u USER bash -c '
  cd /destination/to/your/project
  GIT_SSH_COMMAND="ssh -i ~/.ssh/name_of_file_SSH_PRIVATE_KEY -o StrictHostKeyChecking=no" git pull origin main
'
```

### **Teste Local no PowerShell:**
```powershell
# Testar conexão SSH
ssh -i ~/.ssh/name_of_file_SSH_PRIVATE_KEY USER@XXX.XX.XX.XX "echo '✅ SSH conectado' && whoami"

# Testar diretório do projeto
ssh -i ~/.ssh/name_of_file_SSH_PRIVATE_KEY USER@XXX.XX.XX.XX "cd /destination/to/your/project && pwd && ls -la"
```

---

## 🔍 Troubleshooting Detalhado

### ❌ "Permission denied (publickey)"
```bash
# Verificar authorized_keys
ls -la /home/USER/.ssh/
cat /home/USER/.ssh/authorized_keys

# Corrigir permissões
chmod 700 /home/USER/.ssh
chmod 600 /home/USER/.ssh/*
chown -R USER:USER /home/USER/.ssh
```

### ❌ "error: cannot open '.git/FETCH_HEAD': Permission denied"
```bash
# Corrigir permissões do .git
chown -R USER:USER /home/USER/apps/your_project/.git
```

### ❌ "error: unable to create file .env.example: Permission denied"
```bash
# Corrigir permissões do projeto completo
chown -R USER:USER /home/USER/apps/your_project
find /home/USER/apps/your_project -type d -exec chmod 755 {} \;
find /home/USER/apps/your_project -type f -exec chmod 644 {} \;
```

### ❌ "fatal: cannot create directory at '.github': Permission denied"
```bash
# Corrigir permissões do projeto completo
chown -R USER:USER /home/USER/apps/your_project
find /home/USER/apps/your_project -type d -exec chmod 755 {} \;
```

### ❌ "fatal: detected dubious ownership"
```bash
# Configurar safe directory
git config --global --add safe.directory /destination/to/your/project
```

### ❌ "make: *** No rule to make target"
```bash
# Verificar se Makefile existe e tem os targets
ls -la Makefile
make --help
```

### ❌ "Repository not found" ou acesso negado
- Verificar se a **chave pública** está nas **Deploy Keys** do GitHub
- Confirmar que **"Allow write access"** está marcado
- Verificar se o repositório é privado e a chave tem acesso

### ❌ "Host key verification failed"
```bash
# No VPS, executar:
ssh-keyscan -H github.com >> ~/.ssh/known_hosts
```

---

## ✅ Checklist de Validação

- [ ] Usuário deploy criado sem senha
- [ ] Diretório .ssh com permissões corretas (700)
- [ ] Chaves SSH geradas (pública e privada)
- [ ] authorized_keys configurado com chave pública
- [ ] **Permissões do .git configuradas para o usuário deploy**
- [ ] **Permissões de escrita do projeto configuradas para o usuário deploy**
- [ ] Deploy Key adicionada no GitHub
- [ ] Todas as Secrets configuradas no GitHub
- [ ] Git safe.directory configurado
- [ ] Teste manual de conexão SSH bem-sucedido
- [ ] Teste manual de git pull funcionando

---