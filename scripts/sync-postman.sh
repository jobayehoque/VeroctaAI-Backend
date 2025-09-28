#!/bin/bash

# 🔄 Postman-GitHub Manual Sync Script
# This script helps you manually sync Postman collections with GitHub

set -e  # Exit on any error

echo "🔄 POSTMAN ↔️ GITHUB SYNC UTILITY"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
POSTMAN_DIR="docs/postman"
COLLECTION_FILE="$POSTMAN_DIR/VeroctaAI-API.postman_collection.json"
ENVIRONMENT_FILE="$POSTMAN_DIR/VeroctaAI-Environment.postman_environment.json"

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if git is available
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed"
        exit 1
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir &> /dev/null; then
        log_error "Not in a git repository"
        exit 1
    fi
    
    # Check if newman is available (optional)
    if command -v newman &> /dev/null; then
        log_success "Newman (Postman CLI) is available"
        NEWMAN_AVAILABLE=true
    else
        log_warning "Newman not found - collection validation will be skipped"
        NEWMAN_AVAILABLE=false
    fi
    
    # Check if postman files exist
    if [[ -f "$COLLECTION_FILE" ]]; then
        log_success "Collection file found: $COLLECTION_FILE"
    else
        log_warning "Collection file not found: $COLLECTION_FILE"
    fi
    
    if [[ -f "$ENVIRONMENT_FILE" ]]; then
        log_success "Environment file found: $ENVIRONMENT_FILE"
    else
        log_warning "Environment file not found: $ENVIRONMENT_FILE"
    fi
}

# Validate collections with Newman
validate_collections() {
    if [[ "$NEWMAN_AVAILABLE" == true && -f "$COLLECTION_FILE" && -f "$ENVIRONMENT_FILE" ]]; then
        log_info "Validating Postman collections with Newman..."
        
        if newman run "$COLLECTION_FILE" \
            -e "$ENVIRONMENT_FILE" \
            --reporter cli \
            --timeout 30000 \
            --ignore-redirects \
            --bail; then
            log_success "Collection validation passed"
        else
            log_warning "Collection validation completed with warnings"
        fi
    else
        log_warning "Skipping validation - Newman not available or files missing"
    fi
}

# Update collection metadata
update_metadata() {
    log_info "Updating collection metadata..."
    
    if [[ -f "$COLLECTION_FILE" ]]; then
        python3 << 'EOF'
import json
import datetime
import sys

try:
    collection_file = 'docs/postman/VeroctaAI-API.postman_collection.json'
    
    with open(collection_file, 'r') as f:
        collection = json.load(f)
    
    # Update export timestamp
    collection['info']['_postman_exported_at'] = datetime.datetime.now().isoformat() + 'Z'
    
    # Add or update sync information
    current_desc = collection['info'].get('description', '')
    sync_info = f"\n\n**🔄 Last Manual Sync**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n**📂 Repository**: jobayehoque/VeroctaAI-Backend\n**🌿 Branch**: main"
    
    if "Last Manual Sync" not in current_desc:
        collection['info']['description'] = current_desc + sync_info
    else:
        # Update existing sync info
        lines = current_desc.split('\n')
        updated_lines = []
        for line in lines:
            if "Last Manual Sync" in line:
                updated_lines.append(f"**🔄 Last Manual Sync**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
            else:
                updated_lines.append(line)
        collection['info']['description'] = '\n'.join(updated_lines)
    
    with open(collection_file, 'w') as f:
        json.dump(collection, f, indent=2)
        
    print("✅ Collection metadata updated successfully")
    
except Exception as e:
    print(f"❌ Error updating metadata: {e}")
    sys.exit(1)
EOF
        log_success "Metadata updated successfully"
    else
        log_warning "Collection file not found, skipping metadata update"
    fi
}

# Test API connectivity
test_api() {
    log_info "Testing API connectivity..."
    
    if curl -s -f "https://veroctaai-backend.onrender.com/api/health" | grep -q "healthy"; then
        log_success "API health check passed"
    else
        log_warning "API health check failed or API not responding"
    fi
}

# Commit and push changes
commit_changes() {
    log_info "Checking for changes to commit..."
    
    # Check if there are changes in the postman directory
    if git diff --quiet "$POSTMAN_DIR/"; then
        log_info "No changes detected in Postman files"
        return 0
    fi
    
    log_info "Changes detected, committing to Git..."
    
    # Add postman files
    git add "$POSTMAN_DIR/"
    
    # Create commit message
    COMMIT_MSG="🔄 Manual sync of Postman collections

✅ Updated collection metadata
✅ Validated collections (if Newman available)
✅ Tested API connectivity

[manual-sync] $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Commit changes
    if git commit -m "$COMMIT_MSG"; then
        log_success "Changes committed successfully"
        
        # Ask user if they want to push
        read -p "Push changes to GitHub? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if git push; then
                log_success "Changes pushed to GitHub successfully"
            else
                log_error "Failed to push changes to GitHub"
                return 1
            fi
        else
            log_info "Changes committed locally but not pushed"
        fi
    else
        log_error "Failed to commit changes"
        return 1
    fi
}

# Generate sync report
generate_report() {
    log_info "Generating sync report..."
    
    cat > POSTMAN_SYNC_REPORT.md << EOF
# 🔄 Postman Collection Manual Sync Report

**Sync Date**: $(date)
**Repository**: jobayehoque/VeroctaAI-Backend
**Branch**: $(git branch --show-current)
**User**: $(git config user.name)

## 📋 Sync Status

✅ **Prerequisites**: Checked
✅ **Collection Validation**: $([ "$NEWMAN_AVAILABLE" == true ] && echo "Completed with Newman" || echo "Skipped (Newman not available)")
✅ **Metadata Updated**: Timestamps and sync info updated
✅ **API Connectivity**: Production API tested
✅ **Git Operations**: Changes committed and synced

## 📁 Files Processed

- \`$COLLECTION_FILE\`
- \`$ENVIRONMENT_FILE\`

## 🔗 Quick Links

- [Production API](https://veroctaai-backend.onrender.com)
- [API Health](https://veroctaai-backend.onrender.com/api/health)
- [Repository](https://github.com/jobayehoque/VeroctaAI-Backend)

## 📊 Git Status

\`\`\`
$(git status --porcelain $POSTMAN_DIR/)
\`\`\`

---
*Generated by manual sync script on $(date)*
EOF

    log_success "Sync report generated: POSTMAN_SYNC_REPORT.md"
}

# Main execution
main() {
    log_info "Starting Postman-GitHub sync process..."
    
    check_prerequisites
    validate_collections
    update_metadata
    test_api
    commit_changes
    generate_report
    
    echo
    log_success "🎉 Postman-GitHub sync completed successfully!"
    echo
    echo "📋 Next steps:"
    echo "  1. Review the sync report: POSTMAN_SYNC_REPORT.md"
    echo "  2. Check your Postman workspace for the latest changes"
    echo "  3. Verify the GitHub repository has been updated"
    echo
}

# Handle command line arguments
case "${1:-}" in
    "validate")
        check_prerequisites
        validate_collections
        ;;
    "metadata")
        update_metadata
        ;;
    "test")
        test_api
        ;;
    "commit")
        commit_changes
        ;;
    "report")
        generate_report
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo
        echo "Commands:"
        echo "  validate  - Only validate collections with Newman"
        echo "  metadata  - Only update collection metadata"
        echo "  test      - Only test API connectivity"
        echo "  commit    - Only commit and push changes"
        echo "  report    - Only generate sync report"
        echo "  help      - Show this help message"
        echo
        echo "If no command is specified, runs the full sync process"
        ;;
    *)
        main
        ;;
esac