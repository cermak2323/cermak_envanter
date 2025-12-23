#!/usr/bin/env python3
"""
Comprehensive QR Code Synchronization Job
- Local folder structure management
- B2 synchronization (when credentials available)
- Backup and verification
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def run_qr_sync_job():
    """
    Scheduled job to sync QR codes
    Called by APScheduler
    """
    try:
        logger.info("\n" + "="*70)
        logger.info("QR CODE SYNCHRONIZATION JOB STARTED")
        logger.info("="*70)
        
        from qr_sync_manager import QRSyncManager
        
        manager = QRSyncManager()
        
        # 1. Verify local structure
        logger.info("\n[STEP 1] Verifying local QR folder structure...")
        report = manager.verify_folder_structure()
        
        # 2. Backup to local backup directory
        logger.info("\n[STEP 2] Backing up QR codes to backup directory...")
        backup_count = manager.backup_to_backup_dir()
        
        # 3. B2 sync (if available)
        logger.info("\n[STEP 3] Attempting B2 synchronization...")
        b2_sync_result = None
        try:
            b2_available = os.getenv('USE_B2_STORAGE', 'False').lower() == 'true'
            if b2_available:
                from b2_sync_manager import B2SyncManager
                b2_manager = B2SyncManager()
                b2_sync_result = b2_manager.sync()
                logger.info(f"   [OK] B2 sync completed: {b2_sync_result}")
            else:
                logger.info("   [INFO] B2 storage disabled (USE_B2_STORAGE=False)")
        except Exception as e:
            logger.warning(f"   [WARNING] B2 sync not available: {e}")
        
        # Summary
        logger.info("\n" + "="*70)
        logger.info("QR SYNC JOB COMPLETED")
        logger.info("="*70)
        logger.info(f"  Local folders verified: {report['local_folders']}")
        logger.info(f"  Total QR files: {report['total_files']:,}")
        logger.info(f"  Total size: {report['total_size_mb']:.2f} MB")
        logger.info(f"  Files backed up: {backup_count}")
        if b2_sync_result:
            logger.info(f"  B2 uploaded: {b2_sync_result.get('uploaded', 0)}")
            logger.info(f"  B2 downloaded: {b2_sync_result.get('downloaded', 0)}")
        logger.info("="*70 + "\n")
        
        return {
            'success': True,
            'local_folders': report['local_folders'],
            'total_files': report['total_files'],
            'backup_count': backup_count,
            'b2_sync': b2_sync_result
        }
        
    except Exception as e:
        logger.error(f"[ERROR] QR Sync job failed: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == '__main__':
    # Direct execution for testing
    run_qr_sync_job()
