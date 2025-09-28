# 🔄 Postman Collection Sync Setup

Your Postman collections are now fully integrated with GitHub! Here's how to use the sync functionality:

## 🚀 Quick Setup (What You Need to Do)

### **1. Commit the Sync Infrastructure**
```bash
git add .github/workflows/postman-sync.yml scripts/sync-postman.sh POSTMAN_GITHUB_SYNC_GUIDE.md
git commit -m "🔄 Add Postman-GitHub sync infrastructure"
git push
```

### **2. Enable GitHub Actions**
- Go to your repository on GitHub
- Click **"Actions"** tab
- You'll see the **"🔄 Postman Collection Sync"** workflow
- It will run automatically every 6 hours or when you push changes to `docs/postman/`

### **3. Test Manual Sync**
```bash
# Run the manual sync script
./scripts/sync-postman.sh

# Or run specific operations
./scripts/sync-postman.sh validate  # Just validate collections
./scripts/sync-postman.sh test      # Just test API connectivity
```

## 🔄 How It Works

### **Automatic Sync (Recommended)**
- **Triggers**: Every 6 hours, on file changes, or manual trigger
- **Actions**: Validates collections, updates metadata, tests API, commits changes
- **Benefits**: Hands-off, always up-to-date, includes validation

### **Manual Sync**
- **Command**: `./scripts/sync-postman.sh`
- **Control**: Full control over when and what to sync
- **Benefits**: Immediate sync, troubleshooting, selective operations

## 📋 Sync Process

1. **Validates** collections with Newman (if available)
2. **Updates** metadata with sync timestamps
3. **Tests** production API connectivity
4. **Commits** changes to Git with descriptive messages
5. **Generates** sync reports for tracking

## 🛠️ Postman Workspace Integration

### **Option A: Direct GitHub Integration (Team Plan)**
1. In Postman, go to your workspace
2. Click **Integrations** → **GitHub**
3. Connect to `jobayehoque/VeroctaAI-Backend`
4. Set sync path to `docs/postman/`
5. Enable bidirectional sync

### **Option B: Manual Export/Import**
1. **Export from Postman**:
   - Right-click collection → Export
   - Save to `docs/postman/VeroctaAI-API.postman_collection.json`
   - Right-click environment → Export
   - Save to `docs/postman/VeroctaAI-Environment.postman_environment.json`

2. **Run sync script**:
   ```bash
   ./scripts/sync-postman.sh
   ```

3. **Import to Postman**:
   - Use the files from GitHub when you want to import updates

## 📊 Monitoring & Reports

### **GitHub Actions Dashboard**
- View workflow runs at: `https://github.com/jobayehoque/VeroctaAI-Backend/actions`
- See sync status, validation results, and error logs

### **Sync Reports**
- Generated automatically: `POSTMAN_SYNC_REPORT.md`
- Contains sync status, file changes, API health, and timestamps

### **Collection Metadata**
- Collections include sync timestamps in their descriptions
- Version history tracked through Git commits

## 🔧 Troubleshooting

### **Sync Fails**
1. Check GitHub Actions logs
2. Verify API is accessible: `curl https://veroctaai-backend.onrender.com/api/health`
3. Run manual sync: `./scripts/sync-postman.sh`

### **Collection Validation Errors**
1. Install Newman: `npm install -g newman`
2. Test locally: `newman run docs/postman/VeroctaAI-API.postman_collection.json`
3. Fix collection issues in Postman

### **Git Conflicts**
1. Pull latest changes: `git pull`
2. Resolve conflicts in collection files
3. Re-run sync: `./scripts/sync-postman.sh`

## 🎯 Best Practices

### **For Development**
- Make changes in Postman
- Export and sync regularly
- Test with Newman before committing
- Use descriptive commit messages

### **For Team Collaboration**
- Always pull before making changes
- Communicate collection updates to team
- Use branches for major collection changes
- Review sync reports regularly

### **For Production**
- Keep production environment separate
- Test collections against staging first
- Monitor API health in sync process
- Backup collections regularly

## ✅ Success Indicators

Your sync is working correctly when you see:

- [ ] ✅ GitHub Actions workflow runs successfully
- [ ] ✅ Collection metadata shows recent sync timestamps
- [ ] ✅ API health checks pass in workflow logs
- [ ] ✅ Sync reports generate without errors
- [ ] ✅ Changes in Postman appear in GitHub (and vice versa)

## 🎉 You're All Set!

Your Postman collections are now fully integrated with GitHub version control. Any changes you make in Postman can be synced to GitHub, and updates in GitHub can be imported back to Postman.

**Next steps:**
1. Commit the sync infrastructure (command above)
2. Make a test change in Postman
3. Export and run `./scripts/sync-postman.sh`
4. Verify the change appears in GitHub
5. Enjoy automated collection management! 🚀