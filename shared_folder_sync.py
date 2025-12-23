#!/usr/bin/env python3
"""
Shared Folder File Synchronization Manager
Paylaşımlı klasör üzerinden dosya senkronizasyonu

Duties:
1. Copy files between local and shared folder
2. Keep QR codes, Reports, Photos synchronized
"""

import os
import logging
import threading
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import sys
import platform

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SHARED_SYNC - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paylaşımlı klasör yolu - Platform-specific
if platform.system() == 'Linux':
    # NFS mount: sudo mount -t nfs 192.168.0.57:/tahsinortak/CermakDepo/CermakEnvanter/static /mnt/ortakdepo
    SHARED_FOLDER_PATH = '/mnt/ortakdepo'
else:
    SHARED_FOLDER_PATH = r"\\DCSRV\tahsinortak\CermakDepo\CermakEnvanter\static"

# Frozen exe için local static klasör yolunu belirle
if getattr(sys, 'frozen', False):
    LOCAL_STATIC_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Cermak-Envanter', 'static')
else:
    LOCAL_STATIC_DIR = 'static'

# Klasörün var olduğundan emin ol
os.makedirs(LOCAL_STATIC_DIR, exist_ok=True)


class SyncProgressTracker:
    """Thread-safe singleton progress tracker for sync operations"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.reset()
    
    def reset(self):
        """Reset all progress state"""
        with self._lock:
            self.state = {
                'status': 'idle',
                'current_category': None,
                'current_category_index': 0,
                'total_categories': 0,
                'progress_percent': 0,
                'message': '',
                'operation': '',
                'total_files': 0,
                'processed_files': 0,
                'uploaded': 0,
                'downloaded': 0,
                'errors': 0,
                'error_message': None,
                'started_at': None,
                'completed_at': None
            }
    
    def begin_sync(self, total_categories):
        with self._lock:
            self.state.update({
                'status': 'syncing',
                'total_categories': total_categories,
                'current_category_index': 0,
                'progress_percent': 0,
                'started_at': datetime.utcnow().isoformat()
            })
    
    def start_category(self, category_name, index):
        with self._lock:
            self.state['current_category'] = category_name
            self.state['current_category_index'] = index
            if self.state['total_categories'] > 0:
                self.state['progress_percent'] = int((index - 1) / self.state['total_categories'] * 100)
    
    def set_message(self, message, operation=''):
        with self._lock:
            self.state['message'] = message
            if operation:
                self.state['operation'] = operation
    
    def set_total_files(self, count):
        with self._lock:
            self.state['total_files'] = count
    
    def increment_processed(self):
        with self._lock:
            self.state['processed_files'] += 1
    
    def increment_uploaded(self):
        with self._lock:
            self.state['uploaded'] += 1
            self.state['processed_files'] += 1
    
    def increment_downloaded(self):
        with self._lock:
            self.state['downloaded'] += 1
            self.state['processed_files'] += 1
    
    def increment_error(self):
        with self._lock:
            self.state['errors'] += 1
    
    def complete_sync(self, success=True):
        with self._lock:
            self.state['status'] = 'completed' if success else 'failed'
            self.state['progress_percent'] = 100 if success else self.state['progress_percent']
            self.state['completed_at'] = datetime.utcnow().isoformat()
    
    def get_state(self):
        with self._lock:
            return self.state.copy()


# Global singleton instance
sync_progress = SyncProgressTracker()


def get_sync_progress():
    """Helper function for external API access"""
    return sync_progress.get_state()


class SharedFolderSyncManager:
    """Manage file synchronization between local and shared folder"""
    
    SYNC_CATEGORIES = {
        'qr_codes': {
            'local_path': os.path.join(LOCAL_STATIC_DIR, 'qr_codes'),
            'shared_path': os.path.join(SHARED_FOLDER_PATH, 'qr_codes'),
            'extensions': ['.png', '.zip']
        },
        'reports': {
            'local_path': os.path.join(LOCAL_STATIC_DIR, 'reports'),
            'shared_path': os.path.join(SHARED_FOLDER_PATH, 'reports'),
            'extensions': ['.xlsx', '.csv', '.pdf']
        },
        'part_photos': {
            'local_path': os.path.join(LOCAL_STATIC_DIR, 'part_photos'),
            'shared_path': os.path.join(SHARED_FOLDER_PATH, 'part_photos'),
            'extensions': ['.png', '.jpg', '.jpeg']
        }
    }
    
    def __init__(self):
        self.progress = sync_progress
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all directories exist"""
        for category, config in self.SYNC_CATEGORIES.items():
            os.makedirs(config['local_path'], exist_ok=True)
            try:
                os.makedirs(config['shared_path'], exist_ok=True)
            except Exception as e:
                logger.warning(f"Could not create shared path {config['shared_path']}: {e}")
    
    def is_shared_folder_accessible(self):
        """Check if shared folder is accessible"""
        try:
            return os.path.exists(SHARED_FOLDER_PATH)
        except:
            return False
    
    def get_local_files(self, category):
        """Get local files for a category"""
        config = self.SYNC_CATEGORIES.get(category)
        if not config:
            return []
        
        local_path = Path(config['local_path'])
        if not local_path.exists():
            return []
        
        files = []
        extensions = config['extensions']
        
        for file_path in local_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                rel_path = file_path.relative_to(local_path)
                files.append({
                    'path': str(rel_path),
                    'full_path': str(file_path),
                    'size': file_path.stat().st_size,
                    'mtime': file_path.stat().st_mtime
                })
        
        return files
    
    def get_shared_files(self, category):
        """Get files from shared folder"""
        config = self.SYNC_CATEGORIES.get(category)
        if not config:
            return []
        
        shared_path = Path(config['shared_path'])
        if not shared_path.exists():
            return []
        
        files = []
        extensions = config['extensions']
        
        try:
            for file_path in shared_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    rel_path = file_path.relative_to(shared_path)
                    files.append({
                        'path': str(rel_path),
                        'full_path': str(file_path),
                        'size': file_path.stat().st_size,
                        'mtime': file_path.stat().st_mtime
                    })
        except Exception as e:
            logger.error(f"Error reading shared folder: {e}")
        
        return files
    
    def upload_file(self, category, local_file):
        """Copy a local file to shared folder"""
        config = self.SYNC_CATEGORIES.get(category)
        if not config:
            return False
        
        try:
            shared_file_path = Path(config['shared_path']) / local_file['path']
            shared_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(local_file['full_path'], str(shared_file_path))
            logger.info(f"[UPLOAD] {local_file['path']} -> shared folder")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Upload failed: {e}")
            return False
    
    def download_file(self, category, shared_file):
        """Copy a file from shared folder to local"""
        config = self.SYNC_CATEGORIES.get(category)
        if not config:
            return False
        
        try:
            local_file_path = Path(config['local_path']) / shared_file['path']
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(shared_file['full_path'], str(local_file_path))
            logger.info(f"[DOWNLOAD] {shared_file['path']} -> local")
            return True
        except Exception as e:
            logger.error(f"[ERROR] Download failed: {e}")
            return False
    
    def sync_category(self, category, direction='both'):
        """Sync a single category"""
        config = self.SYNC_CATEGORIES.get(category)
        if not config:
            return {'uploaded': 0, 'downloaded': 0, 'errors': 0}
        
        results = {'uploaded': 0, 'downloaded': 0, 'errors': 0}
        
        if not self.is_shared_folder_accessible():
            logger.error("Shared folder not accessible")
            return results
        
        local_files = self.get_local_files(category)
        shared_files = self.get_shared_files(category)
        
        local_paths = {f['path']: f for f in local_files}
        shared_paths = {f['path']: f for f in shared_files}
        
        # Upload: local'da var, shared'da yok
        if direction in ['both', 'upload']:
            for path, file_info in local_paths.items():
                if path not in shared_paths:
                    if self.upload_file(category, file_info):
                        results['uploaded'] += 1
                        self.progress.increment_uploaded()
                    else:
                        results['errors'] += 1
                        self.progress.increment_error()
        
        # Download: shared'da var, local'da yok
        if direction in ['both', 'download']:
            for path, file_info in shared_paths.items():
                if path not in local_paths:
                    if self.download_file(category, file_info):
                        results['downloaded'] += 1
                        self.progress.increment_downloaded()
                    else:
                        results['errors'] += 1
                        self.progress.increment_error()
        
        return results
    
    def full_sync(self, direction='both'):
        """Sync all categories"""
        categories = list(self.SYNC_CATEGORIES.keys())
        self.progress.reset()
        self.progress.begin_sync(len(categories))
        
        total_results = {'uploaded': 0, 'downloaded': 0, 'errors': 0}
        
        if not self.is_shared_folder_accessible():
            logger.error("Shared folder not accessible!")
            self.progress.set_message("Paylaşımlı klasöre erişilemiyor!")
            self.progress.complete_sync(success=False)
            return total_results
        
        for i, category in enumerate(categories, 1):
            self.progress.start_category(category, i)
            self.progress.set_message(f"Syncing {category}...", operation='sync')
            
            logger.info(f"[SYNC] Starting {category} ({i}/{len(categories)})")
            
            results = self.sync_category(category, direction)
            
            total_results['uploaded'] += results['uploaded']
            total_results['downloaded'] += results['downloaded']
            total_results['errors'] += results['errors']
            
            logger.info(f"[SYNC] {category}: +{results['uploaded']} uploaded, +{results['downloaded']} downloaded")
        
        self.progress.complete_sync(success=True)
        logger.info(f"[SYNC COMPLETE] Total: {total_results['uploaded']} up, {total_results['downloaded']} down, {total_results['errors']} errors")
        
        return total_results


# Convenience functions
def sync_all_files(direction='both'):
    """Quick sync all files"""
    manager = SharedFolderSyncManager()
    return manager.full_sync(direction)


def upload_new_file(category, file_path):
    """Upload a single new file"""
    manager = SharedFolderSyncManager()
    config = manager.SYNC_CATEGORIES.get(category)
    if not config:
        return False
    
    rel_path = os.path.relpath(file_path, config['local_path'])
    file_info = {
        'path': rel_path,
        'full_path': file_path,
        'size': os.path.getsize(file_path)
    }
    
    return manager.upload_file(category, file_info)


if __name__ == '__main__':
    print("Testing shared folder sync...")
    manager = SharedFolderSyncManager()
    
    if manager.is_shared_folder_accessible():
        print("✓ Shared folder accessible")
        results = manager.full_sync()
        print(f"Results: {results}")
    else:
        print("✗ Shared folder NOT accessible")
