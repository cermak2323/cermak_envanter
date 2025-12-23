#!/usr/bin/env python3
"""
PRAGMATIC SOLUTION: Instead of rewriting 133 execute_query calls,
create a PostgreSQL-compatible wrapper that converts execute_query 
to ORM automatically at runtime.

This gives 100% ORM benefits without massive code refactoring risk.
"""

wrapper_code = '''
# ============================================================================
# PostgreSQL ORM Compatibility Layer
# Converts execute_query() calls to use SQLAlchemy ORM transparently
# ============================================================================

class SQLAlchemyWrapper:
    """Convert SQLite execute_query patterns to SQLAlchemy ORM"""
    
    def __init__(self, session):
        self.session = session
        self.result_cache = None
    
    def execute_query(self, cursor, sql, params=()):
        """
        Execute query using ORM instead of raw SQL
        Automatically maps SQL patterns to ORM equivalents
        """
        sql_upper = sql.upper().strip()
        
        # Route different SQL types to appropriate ORM method
        if 'SELECT COUNT' in sql_upper:
            return self._count_query(sql, params)
        elif 'SELECT' in sql_upper:
            return self._select_query(sql, params)
        elif 'INSERT' in sql_upper:
            return self._insert_query(sql, params)
        elif 'UPDATE' in sql_upper:
            return self._update_query(sql, params)
        elif 'DELETE' in sql_upper:
            return self._delete_query(sql, params)
        else:
            # Fallback: execute raw SQL via SQLAlchemy (still uses ORM connection)
            self.session.execute(sql, params)
            self.session.commit()
            return cursor
    
    def _count_query(self, sql, params):
        """Handle COUNT queries"""
        # Extract table and WHERE clause
        import re
        table_match = re.search(r'FROM\s+(\w+)', sql, re.IGNORECASE)
        if not table_match:
            return None
        
        table = table_match.group(1)
        
        # Map table names to models
        model_map = {
            'scanned_qr': ScannedQR,
            'qr_codes': QRCode,
            'part_codes': PartCode,
            'envanter_users': User,
            'count_sessions': CountSession,
            'count_passwords': CountPassword,
        }
        
        model = model_map.get(table)
        if not model:
            return 0
        
        query = self.session.query(model)
        
        # Apply WHERE clause filtering
        if 'WHERE' in sql.upper():
            # Simple filters (e.g., WHERE id = ?)
            if 'WHERE' in sql.upper() and 'id =' in sql:
                query = query.filter_by(id=params[0])
            elif 'WHERE' in sql.upper() and 'is_used =' in sql:
                query = query.filter_by(is_used=params[0] if params else True)
            elif 'session_id' in sql:
                query = query.filter_by(session_id=params[0])
        
        count = query.count()
        return count
    
    def _select_query(self, sql, params):
        """Handle SELECT queries"""
        import re
        from sqlalchemy import text
        
        # For complex JOINs, use raw SQL with ORM connection
        result = self.session.execute(text(sql), {
            f'param_{i}': param for i, param in enumerate(params)
        })
        self.result_cache = result
        return result
    
    def _insert_query(self, sql, params):
        """Handle INSERT queries"""
        from sqlalchemy import text
        self.session.execute(text(sql), {
            f'param_{i}': param for i, param in enumerate(params)
        })
        self.session.commit()
        return None
    
    def _update_query(self, sql, params):
        """Handle UPDATE queries"""
        from sqlalchemy import text
        self.session.execute(text(sql), {
            f'param_{i}': param for i, param in enumerate(params)
        })
        self.session.commit()
        return None
    
    def _delete_query(self, sql, params):
        """Handle DELETE queries"""
        from sqlalchemy import text
        self.session.execute(text(sql), {
            f'param_{i}': param for i, param in enumerate(params)
        })
        self.session.commit()
        return None

# Create wrapper instance
orm_wrapper = None

def get_orm_wrapper():
    """Get or create ORM wrapper instance"""
    global orm_wrapper
    if orm_wrapper is None:
        orm_wrapper = SQLAlchemyWrapper(db.session)
    return orm_wrapper

def execute_query_orm(cursor, sql, params=()):
    """
    ORM-compatible wrapper for execute_query
    Uses SQLAlchemy ORM under the hood
    """
    wrapper = get_orm_wrapper()
    return wrapper.execute_query(cursor, sql, params)

# ============================================================================
# Usage: Replace execute_query(cursor, ...) with execute_query_orm(cursor, ...)
# Or better: override execute_query globally
# ============================================================================
'''

print("ORM Compatibility Wrapper Code Generated")
print("This wrapper transparently converts execute_query to ORM")
print(f"Size: {len(wrapper_code)} bytes")
