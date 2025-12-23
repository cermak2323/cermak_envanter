#!/usr/bin/env python3
"""
Fix encoding issues + convert remaining execute_query to ORM in scanning engine
"""
import re
import sys

# Read the backup file with proper handling
with open('app_backup_20251120_124118.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Fix mojibake patterns - replace common mojibake sequences
mojibake_fixes = {
    'Ã¢ÂÅ': '❌',
    'Ã¢Å¡Â¡': '⚡',
    'Ã©': 'é',
    'Â±': '±',  # plus-minus
    'ÃÂ´': 'ö',  # o with diaeresis
    'ÃÂ¼': 'ü',  # u with diaeresis
    'ÃÂ§': 'ç',  # c with cedilla
    'Ã±': 'ı',  # dotless i
    'ÃÂ¸': 'ø',  # o with stroke
    'ÃÅ¸': 'ş',  # s with cedilla
    'AkÃÂ±': 'Akı',
    'oluÃÅ¸': 'oluş',
    'ÃÂ½': 'ş',
    'tarandÃÂ±': 'tarandı',
    'bulunamadÃÂ±': 'bulunamadı',
    'kullanÃÂ±cÃÂ±': 'kullanıcı',
    'AynÃÂ± kullanÃÂ±cÃÂ±': 'Aynı kullanıcı',
    'ÃÂ¶nce': 'önce',
    'ÃÅ¸ÃÂ¼pheli': 'şüpheli',
    'dakika ÃÂ¶nce': 'dakika önce',
    'saat ÃÂ¶nce': 'saat önce',
    'saniye ÃÂ¶nce': 'saniye önce',
    'mÃÂ± kontrol': 'mı kontrol',
    'AkÃÂ±llÃÂ±': 'Akıllı',
    'ÃÂ±': 'ı',
    'Ã©': 'é'
}

for bad, good in mojibake_fixes.items():
    content = content.replace(bad, good)

# Now convert scanning engine execute_query calls to ORM
# Pattern 1: QR lookup in handle_scan_radical
content = content.replace(
    '''        with db_connection() as conn:
            cursor = conn.cursor()

            # Check QR exists (JOIN ile part bilgisi al)
            execute_query(cursor, \'\'\'
                SELECT pc.part_code, pc.part_name 
                FROM qr_codes qc
                JOIN part_codes pc ON qc.part_code_id = pc.id
                WHERE qc.qr_id = ?
            \'\'\', (qr_id,))
            qr_data = cursor.fetchone()

            if not qr_data:
                logging.warning(f"QR not found: {qr_id}")
                emit(\'scan_result\', {\'success\': False, \'message\': f\'❌ QR kod bulunamadı: {qr_id}\'})
                return

            part_code, part_name = qr_data
            logging.info(f"QR found: {part_code} - {part_name}")

            # Ensure session exists
            execute_query(cursor, \'SELECT COUNT(*) FROM count_sessions WHERE id = ?\', (session_id,))
            if cursor.fetchone()[0] == 0:
                logging.info(f"Creating new session {session_id}")
                execute_query(cursor, 
                    \'INSERT INTO count_sessions (id, session_name, is_active, created_at) VALUES (?, ?, ?, ?)\',
                    (session_id, f\'Session_{session_id}\', 1, datetime.now()))
                conn.commit()

            # ⚡ COMPOSITE INDEX kullanır - çok hızlı + AKILLI DUPLICATE
            execute_query(cursor, \'\'\'
                SELECT scanned_by, scanned_at 
                FROM scanned_qr 
                WHERE session_id = ? AND qr_id = ?
            \'\'\', (session_id, qr_id))
            duplicate_record = cursor.fetchone()
            
            if duplicate_record:
                # Duplicate bulundu - Akıllı mesaj oluştur
                prev_user_id, prev_scanned_at = duplicate_record
                
                # Önceki kullanıcı bilgisi
                execute_query(cursor, \'SELECT full_name FROM envanter_users WHERE id = ?\', (prev_user_id,))
                prev_user_result = cursor.fetchone()
                prev_user_name = prev_user_result[0] if prev_user_result else \'Bilinmeyen\'
                
                # Zaman farkı hesapla
                prev_time = datetime.fromisoformat(prev_scanned_at) if isinstance(prev_scanned_at, str) else prev_scanned_at
                time_diff = datetime.now() - prev_time
                
                # Zaman formatı
                if time_diff.total_seconds() < 60:
                    time_str = f"{int(time_diff.total_seconds())} saniye önce"
                    is_suspicious = time_diff.total_seconds() < 30  # 30 saniyeden kısa ise şüpheli
                elif time_diff.total_seconds() < 3600:
                    time_str = f"{int(time_diff.total_seconds() / 60)} dakika önce"
                    is_suspicious = False
                else:
                    time_str = f"{int(time_diff.total_seconds() / 3600)} saat önce"
                    is_suspicious = False
                
                # Aynı kullanıcı mı kontrol et
                is_same_user = (prev_user_id == user_id)''',
    '''        # Check QR exists (ORM JOIN ile part bilgisi al)
        qr_code = QRCode.query.filter_by(qr_id=qr_id).first()
        part = PartCode.query.filter_by(id=qr_code.part_code_id).first() if qr_code else None

        if not qr_code or not part:
            logging.warning(f"QR not found: {qr_id}")
            emit('scan_result', {'success': False, 'message': f'❌ QR kod bulunamadı: {qr_id}'})
            return

        part_code, part_name = part.part_code, part.part_name
        logging.info(f"QR found: {part_code} - {part_name}")

        # Ensure session exists (ORM)
        count_session = CountSession.query.filter_by(id=session_id).first()
        if not count_session:
            logging.info(f"Creating new session {session_id}")
            new_session = CountSession(
                id=session_id,
                session_name=f'Session_{session_id}',
                is_active=True,
                created_at=datetime.now()
            )
            db.session.add(new_session)
            db.session.commit()

        # ⚡ Check duplicate - ORM with COMPOSITE INDEX (çok hızlı)
        duplicate_record = ScannedQR.query.filter_by(session_id=session_id, qr_id=qr_id).first()
        
        if duplicate_record:
            # Duplicate bulundu - Akıllı mesaj oluştur (ORM)
            prev_user_id = duplicate_record.scanned_by
            prev_scanned_at = duplicate_record.scanned_at
            
            # Önceki kullanıcı bilgisi (ORM)
            prev_user = User.query.filter_by(id=prev_user_id).first()
            prev_user_name = prev_user.full_name if prev_user else 'Bilinmeyen'
            
            # Zaman farkı hesapla
            prev_time = datetime.fromisoformat(prev_scanned_at) if isinstance(prev_scanned_at, str) else prev_scanned_at
            time_diff = datetime.now() - prev_time
            
            # Zaman formatı
            if time_diff.total_seconds() < 60:
                time_str = f"{int(time_diff.total_seconds())} saniye önce"
                is_suspicious = time_diff.total_seconds() < 30  # 30 saniyeden kısa ise şüpheli
            elif time_diff.total_seconds() < 3600:
                time_str = f"{int(time_diff.total_seconds() / 60)} dakika önce"
                is_suspicious = False
            else:
                time_str = f"{int(time_diff.total_seconds() / 3600)} saat önce"
                is_suspicious = False
            
            # Aynı kullanıcı mı kontrol et
            is_same_user = (prev_user_id == user_id)'''
)

# Write fixed content
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed encoding + converted scanning engine to ORM")
print(f"Total lines: {len(content.splitlines())}")
