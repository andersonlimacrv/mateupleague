# 📋 Guia Completo: Configuração de Deploy Automatizado com GitHub Actions

## 🎯 Objetivo
Configurar deploy automatizado seguro usando GitHub Actions para fazer deploy em VPS, com usuário dedicado e chaves SSH separadas para maior segurança.

---

## 👤 PASSO 1: Criar Usuário Deploy na VPS

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

## 🔐 PASSO 2: Gerar e Configurar Chaves SSH

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

## 🔗 PASSO 3: Configurar Deploy Key no GitHub

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

## ⚙️ PASSO 4: Configurar GitHub Secrets

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

## 🔄 PASSO 5: Workflow GitHub Actions

### **Workflow para Chave Única:**
```yaml
name: 🚀 Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy Application
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🔑 Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }}
          chmod 600 ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }}
          ssh-keyscan -H ${{ secrets.VPS_HOST }} >> ~/.ssh/known_hosts

      - name: 🚀 Execute Deploy
        run: |
          ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }} << 'EOF'
            set -e
            cd ${{ secrets.REPO_VPS }}

            # Configurar git safe directory
            git config --global --add safe.directory $PWD

            export DOCKER_BUILDKIT=1
            export COMPOSE_DOCKER_CLI_BUILD=1
            
            # Usa mesma chave para git pull
            GIT_SSH_COMMAND="ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} -o StrictHostKeyChecking=no" \
            git pull origin main
            
            make test-make
          EOF
```

### **Workflow para Chaves Separadas:**
```yaml
# ... (mesmos steps iniciais)

      - name: 🚀 Execute Deploy
        run: |
          ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }} << 'EOF'
            set -e
            cd ${{ secrets.REPO_VPS }}

            git config --global --add safe.directory $PWD

            export DOCKER_BUILDKIT=1
            export COMPOSE_DOCKER_CLI_BUILD=1
            
            # Usa chave específica para GitHub
            GIT_SSH_COMMAND="ssh -i ~/.ssh/${{ secrets.PUB_GITHUB_KEY_NAME }} -o StrictHostKeyChecking=no" \
            git pull origin main
            
            make test-make
          EOF
```

---

## 🧪 PASSO 6: Testar a Configuração

### **Teste Manual na VPS:**
```bash
# Testar autenticação GitHub
sudo -u USER ssh -i /home/USER/.ssh/name_of_file_SSH_PRIVATE_KEY -T git@github.com
# Saída esperada: Hi username/repo! You've successfully authenticated...

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

### ❌ "fatal: detected dubious ownership"
```bash
# No VPS, executar:
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
- [ ] Deploy Key adicionada no GitHub
- [ ] Todas as Secrets configuradas no GitHub
- [ ] Git safe.directory configurado
- [ ] Teste manual de conexão SSH bem-sucedido
- [ ] Teste manual de git pull funcionando

---