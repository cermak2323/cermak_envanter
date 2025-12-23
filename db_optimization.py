"""
⚡ DATABASE OPTIMIZATION - Indexes ve WAL Mode
Multi-device support için gerekli optimizasyonlar
"""

def optimize_database(db_connection):
    """Veritabanını optimize et - indexes ekle, WAL mode aç"""
    cursor = db_connection.cursor()
    
    try:
        # ⚡ PRAGMA OPTIMIZATIONS - SQLite performance tuning
        
        # WAL Mode - Better concurrent writes
        cursor.execute('PRAGMA journal_mode=WAL;')
        print("✅ WAL Mode enabled for better concurrent access")
        
        # Synchronous mode - Balanced safety/performance
        cursor.execute('PRAGMA synchronous=NORMAL;')
        print("✅ Synchronous mode set to NORMAL")
        
        # Cache size - More memory for faster queries
        cursor.execute('PRAGMA cache_size=10000;')
        print("✅ Cache size increased to 10000 pages")
        
        # Temp store - Use memory for temp tables
        cursor.execute('PRAGMA temp_store=MEMORY;')
        print("✅ Temp store set to MEMORY")
        
        # Foreign keys - Enable referential integrity
        cursor.execute('PRAGMA foreign_keys=ON;')
        print("✅ Foreign keys enabled")
        
        # Automatic vacuum
        cursor.execute('PRAGMA auto_vacuum=INCREMENTAL;')
        cursor.execute('PRAGMA incremental_vacuum(10000);')
        print("✅ Automatic vacuum enabled")
        
        # ⚡ CREATE MISSING INDEXES
        
        # Index 1: scanned_qr - Most important! (Sayım export sırasında)
        try:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_scanned_qr_session 
                ON scanned_qr(session_id)
            ''')
            print("✅ Index created: scanned_qr(session_id)")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
        
        # Index 2: scanned_qr - Part code lookup
        try:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_scanned_qr_part 
                ON scanned_qr(part_code)
            ''')
            print("✅ Index created: scanned_qr(part_code)")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
        
        # Index 3: count_sessions - Time-based queries
        try:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_count_sessions_created 
                ON count_sessions(created_at DESC)
            ''')
            print("✅ Index created: count_sessions(created_at)")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
        
        # Index 4: qr_codes - QR lookup optimization
        try:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_qr_codes_qr_id 
                ON qr_codes(qr_id)
            ''')
            print("✅ Index created: qr_codes(qr_id)")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
        
        # Index 5: part_codes - Part lookup
        try:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_part_codes_part_code 
                ON part_codes(part_code)
            ''')
            print("✅ Index created: part_codes(part_code)")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
        
        # Index 6: scanned_qr - Duplicate detection
        try:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_scanned_qr_duplicate 
                ON scanned_qr(session_id, qr_id)
            ''')
            print("✅ Index created: scanned_qr(session_id, qr_id) - Duplicate detection")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
        
        # Index 7: envanter_users - User lookups
        try:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_envanter_users_id 
                ON envanter_users(id)
            ''')
            print("✅ Index created: envanter_users(id)")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
        
        db_connection.commit()
        
        # ⚡ ANALYZE - Update statistics for query optimizer
        try:
            cursor.execute('ANALYZE;')
            print("✅ Database statistics analyzed")
        except Exception as e:
            print(f"⚠️ Analyze warning: {e}")
        
        db_connection.commit()
        print("\n✅ DATABASE OPTIMIZATION COMPLETE")
        
    except Exception as e:
        print(f"❌ Database optimization error: {e}")
        db_connection.rollback()
        raise


def get_database_stats(db_connection):
    """Veritabanı istatistiklerini al"""
    cursor = db_connection.cursor()
    stats = {}
    
    try:
        # Table sizes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            stats[table_name] = {'rows': count}
        
        # Index count
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'")
        stats['indexes'] = cursor.fetchone()[0]
        
        # DB size
        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        stats['size_mb'] = (page_count * page_size) / (1024 * 1024)
        
        # WAL mode
        cursor.execute("PRAGMA journal_mode")
        stats['journal_mode'] = cursor.fetchone()[0]
        
    except Exception as e:
        print(f"⚠️ Stats error: {e}")
    
    return stats


if __name__ == '__main__':
    # Test locally
    import sqlite3
    from pathlib import Path
    
    db_path = Path('instance/envanter_local.db')
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        optimize_database(conn)
        
        stats = get_database_stats(conn)
        print("\n📊 Database Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        conn.close()
    else:
        print(f"Database not found at {db_path}")
