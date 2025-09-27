"""
Clone verification module for VeroctaAI
Provides project integrity checking functionality
"""

import os
import hashlib
import logging
from datetime import datetime

def verify_project_integrity():
    """
    Verify the integrity of the project files
    Returns a report of the verification status
    """
    # List of core project files that should exist
    core_files = [
        'app.py',
        'routes.py', 
        'auth.py',
        'database.py',
        'models.py',
        'health.py',
        'requirements.txt',
        'pyproject.toml'
    ]
    
    report = {
        'status': 'healthy',
        'message': 'Project integrity verified',
        'timestamp': datetime.utcnow().isoformat(),
        'files_checked': 0,
        'files_matched': 0,
        'files_modified': 0,
        'files_missing': 0,
        'deviations': []
    }
    
    try:
        # Check if core files exist
        for file_path in core_files:
            report['files_checked'] += 1
            
            if os.path.exists(file_path):
                report['files_matched'] += 1
                logging.debug(f"✅ File exists: {file_path}")
            else:
                report['files_missing'] += 1
                report['deviations'].append({
                    'type': 'missing',
                    'file': file_path,
                    'description': f'Core file {file_path} is missing'
                })
                logging.warning(f"❌ Missing file: {file_path}")
        
        # Check for additional project structure
        if os.path.exists('uploads'):
            logging.debug("✅ Uploads directory exists")
        else:
            logging.info("ℹ️ Uploads directory will be created on first use")
            
        if os.path.exists('outputs'):
            logging.debug("✅ Outputs directory exists")
        else:
            logging.info("ℹ️ Outputs directory will be created on first use")
        
        # Determine overall status
        if report['files_missing'] > 0:
            report['status'] = 'degraded'
            report['message'] = f"Project partially intact - {report['files_missing']} files missing"
        elif len(report['deviations']) > 0:
            report['status'] = 'degraded'
            report['message'] = f"Project has {len(report['deviations'])} deviations"
        else:
            report['status'] = 'healthy'
            report['message'] = "All core files present and accounted for"
            
    except Exception as e:
        report['status'] = 'error'
        report['message'] = f"Verification failed: {str(e)}"
        logging.error(f"Clone verification error: {e}")
    
    return report

def get_file_hash(file_path):
    """
    Calculate SHA-256 hash of a file
    """
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256()
            for chunk in iter(lambda: f.read(4096), b""):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating hash for {file_path}: {e}")
        return None