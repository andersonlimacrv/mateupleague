# 📋 Guia Completo: Configuração de Deploy Automatizado com GitHub Actions

## 🎯 Objetivo
Configurar um usuário dedicado na VPS para deploy automatizado via GitHub Actions, usando chaves SSH específicas e seguras.

---

## 🔐 PASSO 1: Criar Chave SSH no VPS para GitHub

**Execute no servidor como root:**

```bash
# Conectar como root primeiro
ssh -i sua_chave_root root@seu_server

# Criar chave SSH específica para deploy no GitHub
sudo -u deploy ssh-keygen -t ed25519 -f /home/deploy/.ssh/github_actions_deploy -N ""

# Verificar a chave pública gerada
cat /home/deploy/.ssh/github_actions_deploy.pub

# Configurar permissões de segurança
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/github_actions_deploy
chmod 644 /home/deploy/.ssh/github_actions_deploy.pub
chmod 644 /home/deploy/.ssh/known_hosts 2>/dev/null || true
```

**📝 Notas:**
- `-t ed25519`: Algoritmo mais moderno e seguro
- `-f /home/deploy/.ssh/github_actions_deploy`: Nome descritivo da chave
- `-N ""`: Senha vazia (para automação)
- Permissões corretas são **CRUCIAIS** para funcionamento do SSH

---

## 🔗 PASSO 2: Configurar Deploy Key no GitHub

1. **Acesse seu repositório no GitHub**
2. **Vá em:** Settings → Deploy Keys
3. **Clique em:** "Add deploy key"
4. **Configure:**
   - **Title:** `vps-deploy-key`
   - **Key:** Cole o conteúdo de `/home/deploy/.ssh/github_actions_deploy.pub`
   - **✓ Allow write access:** MARQUE esta opção

---

## ⚙️ PASSO 3: Configurar Secrets no GitHub

No seu repositório GitHub → **Settings** → **Secrets and variables** → **Actions**

### **Adicione estas Secrets:**

| Nome da Secret | Valor | Descrição |
|----------------|-------|-----------|
| `SSH_PRIVATE_KEY` | Conteúdo da chave **privada** de acesso à VPS | ` cat /home/deploy/.ssh/github_actions_deploy` |
| `SSH_PRIVATE_KEY_NAME` | `github_actions_deploy` | Nome do arquivo da chave |
| `VPS_HOST` | `XXX.XX.XX.XX` | IP/domínio da sua VPS |
| `VPS_USER` | `deploy` | Usuário de deploy na VPS |
| `REPO_VPS` | `/caminho/para/seu/projeto` | Caminho absoluto do projeto na VPS |
| `PUB_GITHUB_KEY` | Conteúdo de `github_actions_deploy` (privada) | Chave para git pull no VPS |

---

## 🔄 PASSO 4: Arquivo GitHub Actions

Crie o arquivo `.github/workflows/deploy.yml`:

```yaml
name: 🚀 Deploy to VPS

on:
  push:
    branches:
      - main
    paths-ignore:
      - '**.md'
      - '.gitignore'
      - 'README.md'

jobs:
  deploy:
    name: 🎯 Deploy Application
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4

      - name: 🔑 Setup SSH for VPS connection
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }}
          chmod 600 ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }}
          ssh-keyscan -H ${{ secrets.VPS_HOST }} >> ~/.ssh/known_hosts

      - name: 🔧 Setup GitHub Deploy Key on VPS
        run: |
          ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }} << 'EOF'
            set -e  # Exit on error
            mkdir -p ~/.ssh
            echo "${{ secrets.GITHUB_DEPLOY_KEY }}" > ~/.ssh/github_actions_deploy
            chmod 600 ~/.ssh/github_actions_deploy
            
            # Adicionar GitHub aos known_hosts
            ssh-keyscan -H github.com >> ~/.ssh/known_hosts 2>/dev/null
            
            echo "✅ GitHub deploy key configured successfully"
          EOF

      - name: 🚀 Execute Deploy
        run: |
          ssh -i ~/.ssh/${{ secrets.SSH_PRIVATE_KEY_NAME }} ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }} << 'EOF'
            set -e  # Exit on any error
            
            echo "📁 Navigating to project directory..."
            cd ${{ secrets.REPO_VPS }}
            
            echo "🔧 Configuring Git SSH..."
            export GIT_SSH_COMMAND="ssh -i ~/.ssh/github_actions_deploy -o StrictHostKeyChecking=no"
            
            echo "📥 Pulling latest changes..."
            git fetch origin
            git reset --hard origin/main
            
            echo "🐳 Deploying with Docker..."
            make down || echo "⚠️ Make down failed, continuing..."
            make up
            make deploy
            
            echo "🧹 Cleaning up..."
            unset GIT_SSH_COMMAND
            
            echo "✅ Deploy completed successfully!"
          EOF

      - name: ✅ Deployment Success
        run: echo "🎉 Deployment completed successfully!"
```

---

## 🛡️ PASSO 5: Configurações de Segurança (Opcional)

**Para maior segurança no VPS:**

```bash
# Restringir usuário deploy (opcional)
sudo usermod -s /bin/rbash deploy

# Criar diretório binário restrito
sudo mkdir /home/deploy/bin
sudo ln -s /usr/bin/git /home/deploy/bin/git
sudo ln -s /usr/bin/make /home/deploy/bin/make
sudo ln -s /usr/bin/docker /home/deploy/bin/docker
sudo ln -s /usr/bin/docker-compose /home/deploy/bin/docker-compose

# Configurar PATH restrito
echo 'PATH=/home/deploy/bin' >> /home/deploy/.bashrc
```

---

## 🧪 PASSO 6: Teste a Configuração

**Teste manualmente no VPS:**
```bash
sudo -u deploy ssh -i /home/deploy/.ssh/github_actions_deploy -T git@github.com
```
**Saída esperada:** `Hi username/repo! You've successfully authenticated...`

**Teste o deploy manualmente:**
```bash
sudo -u deploy bash
cd $REPO_VPS
GIT_SSH_COMMAND="ssh -i ~/.ssh/github_actions_deploy" git pull origin main
```

---

## 🔍 Troubleshooting Comum

### ❌ Erro: "Permission denied (publickey)"
- Verifique permissões do diretório `.ssh` (deve ser 700)
- Verifique permissões da chave privada (deve ser 600)
- Confirme se a chave pública está na Deploy Keys do GitHub

### ❌ Erro: "Host key verification failed"
- Execute manualmente no VPS: `ssh-keyscan -H github.com >> ~/.ssh/known_hosts`

### ❌ Erro: "Could not resolve hostname"
- Verifique se `VPS_HOST` está correto nas GitHub Secrets

---



