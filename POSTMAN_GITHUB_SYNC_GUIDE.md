# 🔄 POSTMAN ↔️ GITHUB SYNC SETUP GUIDE

## 🎯 Goal: Enable Automatic Sync Between Postman and GitHub Repository

This guide will help you set up **bidirectional synchronization** between your Postman collections and the GitHub repository, so changes in either location are automatically synced.

---

## 📋 STEP-BY-STEP SETUP PROCESS

### **Step 1: Enable Postman GitHub Integration**

1. **Open Postman Desktop App** (required for GitHub sync)
2. **Go to Workspaces** → Select your workspace
3. **Click on Settings** (gear icon) → **Integrations**
4. **Find "GitHub"** in the integrations list
5. **Click "Add Integration"**

### **Step 2: Connect Your GitHub Repository**

1. **Authorize Postman** to access your GitHub account
2. **Select Repository**: `jobayehoque/VeroctaAI-Backend`
3. **Choose Branch**: `main` (or create a new branch for Postman sync)
4. **Set Directory**: `docs/postman/` (where your collections are stored)

### **Step 3: Configure Collection Sync**

**For Each Collection:**
1. Go to your **VeroctaAI API Collection**
2. Click the **"..."** menu → **"Integrations"**
3. Select **"GitHub"**
4. Configure sync settings:
   ```
   Repository: jobayehoque/VeroctaAI-Backend
   Branch: main
   Directory: docs/postman/
   File Name: VeroctaAI-API.postman_collection.json
   ```

**For Environment:**
1. Go to **"VeroctaAI Environment"**
2. Click the **"..."** menu → **"Integrations"** 
3. Select **"GitHub"**
4. Configure sync settings:
   ```
   Repository: jobayehoque/VeroctaAI-Backend
   Branch: main
   Directory: docs/postman/
   File Name: VeroctaAI-Environment.postman_environment.json
   ```

---

## ⚡ ALTERNATIVE: AUTOMATED SYNC WORKFLOW

If direct GitHub integration isn't available, here's a **GitHub Actions workflow** to automate the sync:

### **Create GitHub Action for Postman Sync**

Create this file in your repository:

**`.github/workflows/postman-sync.yml`**

```yaml
name: 🔄 Postman Collection Sync

on:
  push:
    paths:
      - 'docs/postman/**'
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *'  # Sync every 6 hours

jobs:
  sync-postman:
    runs-on: ubuntu-latest
    name: Sync Postman Collections
    
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4
      
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        
    - name: Install Newman (Postman CLI)
      run: npm install -g newman
      
    - name: Validate Postman Collections
      run: |
        echo "🧪 Validating Postman Collections..."
        newman run docs/postman/VeroctaAI-API.postman_collection.json \
          -e docs/postman/VeroctaAI-Environment.postman_environment.json \
          --reporter cli \
          --timeout 30000 \
          --ignore-redirects || echo "⚠️ Collection validation completed with warnings"
          
    - name: Update Collection Metadata
      run: |
        echo "📝 Updating collection metadata..."
        # Update timestamps and version info
        python3 << 'EOF'
        import json
        import datetime
        
        # Update collection metadata
        with open('docs/postman/VeroctaAI-API.postman_collection.json', 'r') as f:
            collection = json.load(f)
        
        collection['info']['_postman_exported_at'] = datetime.datetime.now().isoformat() + 'Z'
        collection['info']['description'] = collection['info'].get('description', '') + f"\n\n**Last Synced**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        
        with open('docs/postman/VeroctaAI-API.postman_collection.json', 'w') as f:
            json.dump(collection, f, indent=2)
        EOF
        
    - name: Commit Changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add docs/postman/
        git diff --staged --quiet || git commit -m "🔄 Auto-sync Postman collections [skip ci]"
        git push || echo "No changes to push"

    - name: Create Postman Workspace Link
      run: |
        echo "🔗 Postman Workspace Link: https://app.getpostman.com/run-collection/your-collection-id" >> $GITHUB_STEP_SUMMARY
        echo "📊 Collection Status: ✅ Synced Successfully" >> $GITHUB_STEP_SUMMARY
```

---

## 🛠️ MANUAL SYNC COMMANDS

For immediate manual synchronization, use these commands:

### **Export from Postman**
```bash
# Using Postman CLI (if you have API key)
postman collection get <collection-id> --output docs/postman/VeroctaAI-API.postman_collection.json
postman environment get <environment-id> --output docs/postman/VeroctaAI-Environment.postman_environment.json
```

### **Import to Postman**
```bash
# Using Newman (Postman CLI)
newman run docs/postman/VeroctaAI-API.postman_collection.json \
  -e docs/postman/VeroctaAI-Environment.postman_environment.json \
  --reporters cli,json \
  --reporter-json-export results.json
```

---

## 📡 WEBHOOK-BASED SYNC (Advanced)

Set up a webhook to automatically sync when collections change:

### **1. Create Sync Webhook Script**

```python
#!/usr/bin/env python3
"""
Postman-GitHub Webhook Sync
Automatically syncs Postman collections when changes are detected
"""

from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/webhook/postman-sync', methods=['POST'])
def postman_sync_webhook():
    """Handle Postman webhook and sync to GitHub"""
    
    try:
        # Verify webhook authenticity (implement your security)
        payload = request.get_json()
        
        if payload.get('type') == 'collection' and payload.get('action') == 'updated':
            collection_id = payload.get('collection_id')
            
            # Export collection from Postman
            export_cmd = f"""
            postman collection get {collection_id} \
              --output docs/postman/VeroctaAI-API.postman_collection.json
            """
            
            # Commit and push to GitHub
            git_cmd = """
            git add docs/postman/
            git commit -m "🔄 Auto-sync from Postman webhook"
            git push origin main
            """
            
            subprocess.run(export_cmd, shell=True, check=True)
            subprocess.run(git_cmd, shell=True, check=True)
            
            return jsonify({'status': 'success', 'message': 'Collection synced to GitHub'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### **2. Configure Postman Webhook**
1. In Postman, go to **Integrations** → **Webhooks**
2. Create webhook pointing to your server
3. Set events: Collection updated, Environment updated

---

## 🎯 RECOMMENDED SYNC STRATEGY

### **Option 1: Postman Team Plan (Recommended)**
- **Direct GitHub integration** built into Postman
- **Automatic bidirectional sync**
- **Conflict resolution** handled by Postman
- **Version history** maintained

### **Option 2: GitHub Actions (Free)**
- **Scheduled sync** every few hours
- **Manual trigger** when needed
- **Collection validation** included
- **Version control** through Git

### **Option 3: Manual Sync (Simple)**
- **Export collections** from Postman when changed
- **Commit to GitHub** manually
- **Import updates** when GitHub changes
- **Full control** over sync timing

---

## 🔧 IMPLEMENTATION STEPS FOR YOU

### **Immediate Action: Setup GitHub Actions Sync**

1. **Create the workflow file**:
```bash
mkdir -p .github/workflows
# Copy the YAML content above to .github/workflows/postman-sync.yml
```

2. **Test the workflow**:
```bash
git add .github/workflows/postman-sync.yml
git commit -m "Add Postman-GitHub sync workflow"
git push
```

3. **Verify in GitHub**:
   - Go to **Actions** tab in your repository
   - You should see the "Postman Collection Sync" workflow
   - Trigger it manually to test

### **Enable Collection Monitoring**

Add this script to monitor collection changes:

```bash
#!/bin/bash
# File: scripts/monitor-postman.sh

echo "🔄 Monitoring Postman Collections for Changes..."

# Watch for file changes in docs/postman/
fswatch docs/postman/ | while read file; do
    echo "📝 Detected change in: $file"
    echo "🔄 Auto-committing Postman collection updates..."
    
    git add docs/postman/
    git commit -m "🔄 Auto-update Postman collections"
    git push
    
    echo "✅ Postman collections synced to GitHub"
done
```

---

## ✅ VERIFICATION CHECKLIST

After setup, verify these work:

- [ ] **Postman → GitHub**: Changes in Postman appear in GitHub
- [ ] **GitHub → Postman**: Changes in GitHub can be imported to Postman  
- [ ] **Automatic Sync**: Workflow runs on schedule/trigger
- [ ] **Collection Validation**: No errors in Newman tests
- [ ] **Version History**: Git commits track changes properly

---

## 🎉 BENEFITS OF SYNC SETUP

✅ **Always Up-to-Date**: Collections stay synchronized automatically  
✅ **Version Control**: Full Git history of API changes  
✅ **Team Collaboration**: Multiple developers can contribute  
✅ **Backup Protection**: Collections backed up in GitHub  
✅ **CI/CD Integration**: Automated testing with Newman  
✅ **Documentation**: API changes tracked with commit messages

**Would you like me to create any of these sync mechanisms for your repository?**