#!/usr/bin/env python3
"""
QR Code Folder Synchronization Manager
Local folder structure management and monitoring
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - QR_SYNC - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QRSyncManager:
    """Manage QR code folder structure and synchronization"""
    
    def __init__(self):
        """Initialize QR sync manager"""
        self.local_qr_dir = Path('static/qr_codes')
        self.backup_dir = Path('backups')
        
        if not self.local_qr_dir.exists():
            self.local_qr_dir.mkdir(parents=True, exist_ok=True)
            logger.warning(f"Created QR directory: {self.local_qr_dir}")
    
    def get_qr_range_from_database(self):
        """Get QR code ranges from database"""
        try:
            from app import app, db, QRCode
            
            with app.app_context():
                # Get all QR codes with their IDs
                qr_codes = db.session.query(QRCode.qr_id).all()
                ranges = {}
                
                for (qr_id,) in qr_codes:
                    if qr_id:
                        # Extract numeric part from QR ID
                        # Example: 00072-24017 -> extract first 5 digits
                        parts = qr_id.split('-')
                        if len(parts) > 0:
                            try:
                                first_num = int(parts[0])
                                # Determine range folder
                                if first_num <= 50000:
                                    range_folder = '00001-50000'
                                elif first_num <= 100000:
                                    range_folder = '50001-100000'
                                else:
                                    range_folder = '100001-150000'
                                
                                ranges[range_folder] = ranges.get(range_folder, 0) + 1
                            except ValueError:
                                # Non-numeric QR ID
                                ranges['OTHER'] = ranges.get('OTHER', 0) + 1
                
                return ranges
        except Exception as e:
            logger.error(f"[ERROR] Getting QR ranges from DB: {e}")
            return {}
    
    def get_local_structure(self):
        """Get local folder structure"""
        if not self.local_qr_dir.exists():
            logger.warning(f"Local QR dir not found: {self.local_qr_dir}")
            return {}
        
        structure = {}
        
        for range_folder in self.local_qr_dir.iterdir():
            if range_folder.is_dir():
                files = list(range_folder.glob('*.png'))
                structure[range_folder.name] = {
                    'count': len(files),
                    'files': sorted([f.name for f in files]),
                    'size_mb': sum(f.stat().st_size for f in files) / (1024 * 1024)
                }
        
        logger.info(f"[OK] Local structure: {len(structure)} range folders")
        return structure
    
    def ensure_folders_exist(self, required_ranges):
        """Create missing range folders"""
        created = 0
        
        for range_name in required_ranges.keys():
            range_path = self.local_qr_dir / range_name
            if not range_path.exists():
                range_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"[CREATE] Folder: {range_name}")
                created += 1
        
        return created
    
    def verify_folder_structure(self):
        """Verify and report folder structure health"""
        local_struct = self.get_local_structure()
        db_ranges = self.get_qr_range_from_database()
        
        logger.info("\n" + "="*70)
        logger.info("QR CODE FOLDER STRUCTURE VERIFICATION")
        logger.info("="*70)
        
        print("\nLocal Folder Structure:")
        print("-"*70)
        total_files = 0
        total_size = 0
        
        for folder, data in sorted(local_struct.items()):
            print(f"  {folder:20} | {data['count']:4} files | {data['size_mb']:8.2f} MB")
            total_files += data['count']
            total_size += data['size_mb']
        
        print("-"*70)
        print(f"  {'TOTAL':20} | {total_files:4} files | {total_size:8.2f} MB")
        
        print("\n\nDatabase QR Code Ranges:")
        print("-"*70)
        for range_name, count in sorted(db_ranges.items()):
            local_count = local_struct.get(range_name, {}).get('count', 0)
            match = '[OK]' if local_count > 0 else '[WARNING]'
            print(f"  {match} {range_name:20} | DB: {count:4} | Local: {local_count:4}")
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"  Local folders: {len(local_struct)}")
        print(f"  Total QR files: {total_files:,}")
        print(f"  Total size: {total_size:.2f} MB")
        print(f"  Database QR codes: {sum(db_ranges.values())}")
        print("="*70 + "\n")
        
        return {
            'local_folders': len(local_struct),
            'total_files': total_files,
            'total_size_mb': total_size,
            'db_qr_count': sum(db_ranges.values())
        }
    
    def backup_to_backup_dir(self):
        """Backup QR codes to backup directory"""
        try:
            backup_qr_dir = self.backup_dir / 'qr_codes'
            backup_qr_dir.mkdir(parents=True, exist_ok=True)
            
            copied_count = 0
            
            for range_folder in self.local_qr_dir.iterdir():
                if range_folder.is_dir():
                    backup_folder = backup_qr_dir / range_folder.name
                    backup_folder.mkdir(parents=True, exist_ok=True)
                    
                    for png_file in range_folder.glob('*.png'):
                        backup_file = backup_folder / png_file.name
                        
                        # Only copy if newer or missing
                        if not backup_file.exists() or png_file.stat().st_mtime > backup_file.stat().st_mtime:
                            shutil.copy2(png_file, backup_file)
                            copied_count += 1
            
            if copied_count > 0:
                logger.info(f"[BACKUP] Copied {copied_count} QR files to {backup_qr_dir}")
            
            return copied_count
            
        except Exception as e:
            logger.error(f"[ERROR] Backing up QR codes: {e}")
            return 0


if __name__ == '__main__':
    try:
        manager = QRSyncManager()
        
        # Verify structure
        report = manager.verify_folder_structure()
        
        # Backup to local backup directory
        backup_count = manager.backup_to_backup_dir()
        
        sys.exit(0)
    except Exception as e:
        logger.error(f"[FATAL] {e}")
        sys.exit(1)
