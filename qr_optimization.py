"""
⚡ QR SCANNING OPTIMIZATION MODULE
Multi-device support ve performans optimizasyonları
"""

import time
from datetime import datetime
from functools import lru_cache
import threading

# ⚡ QR SCANNING QUEUE - Batch processing for multi-device support
scan_queue = []
scan_queue_lock = threading.Lock()
BATCH_SIZE = 10
BATCH_TIMEOUT = 1.0  # 1 saniye içinde batch'le

class ScanBatch:
    """QR taramaları batch olarak işle"""
    
    def __init__(self, db_connection, logger):
        self.db = db_connection
        self.logger = logger
        self.pending_scans = []
        self.last_batch_time = time.time()
    
    def add_scan(self, qr_id, session_id, part_code, user_id):
        """Taramayı kuyruğa ekle"""
        scan_record = {
            'qr_id': qr_id,
            'session_id': str(session_id),
            'part_code': part_code,
            'user_id': user_id,
            'scanned_at': datetime.now()
        }
        
        with scan_queue_lock:
            self.pending_scans.append(scan_record)
        
        # Batch ready?
        if len(self.pending_scans) >= BATCH_SIZE or (time.time() - self.last_batch_time) > BATCH_TIMEOUT:
            return self.flush()
        
        return None
    
    def flush(self):
        """Bekleyen taramaları veritabanına yaz"""
        if not self.pending_scans:
            return []
        
        results = []
        cursor = self.db.cursor()
        
        try:
            # Batch insert - 1 query yerine 10 query (veya daha fazla)
            # INSERT VALUES (...), (...), (...) formatında
            
            for scan in self.pending_scans:
                cursor.execute('''
                    INSERT INTO scanned_qr (qr_id, session_id, part_code, scanned_by, scanned_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (scan['qr_id'], scan['session_id'], scan['part_code'], 
                      scan['user_id'], scan['scanned_at']))
                results.append(scan)
            
            # Single commit for all
            self.db.commit()
            self.logger.info(f"✅ Batch processed: {len(results)} scans")
            
        except Exception as e:
            self.logger.error(f"❌ Batch error: {e}")
            self.db.rollback()
            results = []
        
        finally:
            self.pending_scans = []
            self.last_batch_time = time.time()
        
        return results


# ⚡ OPTIMIZED QR LOOKUP - Cache frequently accessed parts
@lru_cache(maxsize=2000)
def get_part_info_cached(part_code):
    """Parça bilgisini cache'le (2000 part)"""
    # Actual lookup happens in app.py, this is just cache layer
    pass


# ⚡ DUPLICATE DETECTION - Session-based deduplication
class DuplicateDetector:
    """QR tekrar tarama tespiti"""
    
    def __init__(self):
        self.scanned_in_session = {}  # {session_id: {qr_id, qr_id, ...}}
        self.lock = threading.Lock()
    
    def is_duplicate(self, qr_id, session_id):
        """QR bu session'da zaten tarandı mı?"""
        session_id = str(session_id)
        with self.lock:
            if session_id not in self.scanned_in_session:
                return False
            return qr_id in self.scanned_in_session[session_id]
    
    def mark_scanned(self, qr_id, session_id):
        """QR'ı tarandı olarak işaretle"""
        session_id = str(session_id)
        with self.lock:
            if session_id not in self.scanned_in_session:
                self.scanned_in_session[session_id] = set()
            self.scanned_in_session[session_id].add(qr_id)
    
    def clear_session(self, session_id):
        """Session temizle (seansa bitince)"""
        session_id = str(session_id)
        with self.lock:
            if session_id in self.scanned_in_session:
                del self.scanned_in_session[session_id]


# ⚡ RESPONSE TIME CACHE - Hızlı cevap için sık sorgular cache'le
class QueryCache:
    """Sık yapılan sorguların sonuçlarını cache'le"""
    
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl
        self.lock = threading.Lock()
    
    def get(self, key):
        """Cache'den al"""
        with self.lock:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    return value
                else:
                    del self.cache[key]
        return None
    
    def set(self, key, value):
        """Cache'e yaz"""
        with self.lock:
            self.cache[key] = (value, time.time())
    
    def invalidate_like(self, pattern):
        """Pattern eşleşen keys'i sil"""
        with self.lock:
            to_delete = [k for k in self.cache if pattern in k]
            for k in to_delete:
                del self.cache[k]


# ⚡ MULTI-DEVICE SESSION LOCK - Concurrent session access protection
class SessionLock:
    """Session'ı aynı anda birden fazla cihazdan değiştirme koruması"""
    
    def __init__(self):
        self.session_locks = {}  # {session_id: lock}
        self.main_lock = threading.Lock()
    
    def acquire(self, session_id, timeout=5):
        """Session lock'u al"""
        session_id = str(session_id)
        
        with self.main_lock:
            if session_id not in self.session_locks:
                self.session_locks[session_id] = threading.Lock()
            lock = self.session_locks[session_id]
        
        return lock.acquire(timeout=timeout)
    
    def release(self, session_id):
        """Session lock'u bırak"""
        session_id = str(session_id)
        with self.main_lock:
            if session_id in self.session_locks:
                self.session_locks[session_id].release()


# ⚡ DATABASE CONNECTION POOL HEALTH CHECK
class PoolHealthCheck:
    """Connection pool'un sağlığını kontrol et"""
    
    @staticmethod
    def check_pool(engine):
        """Pool duruşunu rapor et"""
        pool = engine.pool
        return {
            'pool_size': pool.size(),
            'checkedout': pool.checkedout(),
            'overflow': pool.overflow(),
            'total': pool.size() + pool.overflow()
        }


# ⚡ SCANNER CHARACTER NORMALIZATION
class ScannerCharacterFix:
    """Scanner cihazları çeşitli karakterleri yanlış okuyor - düzelt"""
    
    # Bazı scanner'lar:
    # - * (42) yerine - (45) okuyor
    # - ? (63) yerine _ (95) okuyor
    # - \ (92) yerine / (47) okuyor
    
    CHAR_MAP = {
        ord('*'): '-',   # * → -
        ord('?'): '_',   # ? → _
        ord('\\'): '/',  # \ → /
        ord('|'): '_',   # | → _
    }
    
    @staticmethod
    def normalize(qr_id):
        """QR ID'yi normalize et"""
        if not qr_id:
            return qr_id
        
        # Scanner fix
        normalized = qr_id.translate(ScannerCharacterFix.CHAR_MAP)
        
        # Whitespace trim
        normalized = normalized.strip()
        
        return normalized


# ⚡ CONCURRENT ACCESS COUNTER
class ConcurrentAccessCounter:
    """Concurrent access sayısını say ve threshold kontrol et"""
    
    def __init__(self, max_concurrent=50):
        self.active_requests = 0
        self.max_concurrent = max_concurrent
        self.lock = threading.Lock()
        self.peak_concurrent = 0
    
    def enter(self):
        """Request başladı"""
        with self.lock:
            self.active_requests += 1
            if self.active_requests > self.peak_concurrent:
                self.peak_concurrent = self.active_requests
            return self.active_requests
    
    def exit(self):
        """Request bitti"""
        with self.lock:
            self.active_requests = max(0, self.active_requests - 1)
            return self.active_requests
    
    def is_overloaded(self):
        """Sistem aşırı yüklü mü?"""
        with self.lock:
            return self.active_requests >= self.max_concurrent
    
    def get_stats(self):
        """İstatistikleri getir"""
        with self.lock:
            return {
                'active': self.active_requests,
                'peak': self.peak_concurrent,
                'max': self.max_concurrent,
                'utilization': (self.active_requests / self.max_concurrent) * 100
            }


# Initialize global instances
duplicate_detector = DuplicateDetector()
query_cache = QueryCache(ttl=300)  # 5 min cache
session_lock = SessionLock()
concurrent_counter = ConcurrentAccessCounter(max_concurrent=100)
scanner_fix = ScannerCharacterFix()

