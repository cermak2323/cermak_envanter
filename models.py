"""
SQLAlchemy ORM Modelleri - EnvanterQR Sistemi
Lokal ve Production ortamları destekler
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()


class PartCode(db.Model):
    """Parça Kodları - Sabit, değişmez"""
    __tablename__ = 'part_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    part_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    part_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Paket bilgileri
    is_package = db.Column(db.Boolean, default=False)
    package_items = db.Column(db.Text)  # JSON formatında item listesi
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    qr_codes = db.relationship('QRCode', backref='part', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PartCode {self.part_code}>'


class QRCode(db.Model):
    """QR Kodlar - Lokal dosya sisteminde, asla değişmez"""
    __tablename__ = 'qr_codes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qr_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    part_code_id = db.Column(db.Integer, db.ForeignKey('part_codes.id'), nullable=False)
    
    # Kullanım izleyici
    is_used = db.Column(db.Boolean, default=False)
    used_count = db.Column(db.Integer, default=0)
    first_used_at = db.Column(db.DateTime)
    last_used_at = db.Column(db.DateTime)
    
    # Durumu
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Index
    __table_args__ = (
        db.Index('idx_qr_part', 'qr_id', 'part_code_id'),
    )
    
    def __repr__(self):
        return f'<QRCode {self.qr_id}>'


class CountSession(db.Model):
    """Sayım Oturumları"""
    __tablename__ = 'count_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(255))
    session_password = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('envanter_users.id'))
    is_active = db.Column(db.Boolean, default=True)  # true = active, false = completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    description = db.Column(db.Text)
    # Summary counts
    total_expected = db.Column(db.Integer, default=0)
    total_scanned = db.Column(db.Integer, default=0)
    # Excel report file path
    report_file_path = db.Column(db.Text)
    
    # İlişkiler
    scanned_items = db.relationship('ScannedQR', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CountSession {self.id}>'


class ScannedQR(db.Model):
    """Taranmış QR Kodlar - İşlem Kayıtları"""
    __tablename__ = 'scanned_qr'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('count_sessions.id'), nullable=False)
    qr_id = db.Column(db.String(255), nullable=False)
    part_code = db.Column(db.String(255))
    scanned_by = db.Column(db.Integer, db.ForeignKey('envanter_users.id'))
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler (backref zaten CountSession'da tanımlı)
    user = db.relationship('User', backref='scans')
    
    def __repr__(self):
        return f'<ScannedQR {self.qr_id} at {self.scanned_at}>'


class User(db.Model):
    """
    EnvanterQR Kullanıcıları - Kendi ayrı table'ında
    
    Ayrı table: envanter_users
    (cermakservis uygulaması kendi users table'ını kullanıyor)
    
    Kolonlar:
    - Core: id, username, password, password_hash, full_name, role, created_at
    - Extended: email, real_name, job_title, title, work_position, user_group, user_role
    - Files: signature_path, profile_image_path
    - Status: is_active_user, can_mark_used
    - 2FA: email_2fa_enabled, email_2fa_code, email_2fa_expires, email_2fa_attempts, email_2fa_locked_until
    - Security: tc_number, last_password_change, force_password_change, force_tutorial
    - Login: first_login_completed, last_login
    - Approvals: terms_accepted
    - Timestamps: updated_at
    
    Toplam: 31 kolon
    """
    __tablename__ = 'envanter_users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Core (her zaman var)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255))  # Backward compat
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')  # admin, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Extended (cermakservis compatibility)
    real_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    job_title = db.Column(db.String(120))
    title = db.Column(db.String(120))
    work_position = db.Column(db.String(120))
    user_group = db.Column(db.String(120))
    user_role = db.Column(db.String(120))
    
    # Files
    signature_path = db.Column(db.String(500))
    profile_image_path = db.Column(db.String(500))
    
    # Status
    is_active_user = db.Column(db.Boolean, default=True)
    can_mark_used = db.Column(db.Boolean, default=False)
    
    # 2FA
    email_2fa_enabled = db.Column(db.Boolean, default=False)
    email_2fa_code = db.Column(db.String(6))
    email_2fa_expires = db.Column(db.DateTime)
    email_2fa_attempts = db.Column(db.Integer, default=0)
    email_2fa_locked_until = db.Column(db.DateTime)
    
    # Security
    tc_number = db.Column(db.String(20))
    last_password_change = db.Column(db.DateTime)
    force_password_change = db.Column(db.Boolean, default=False)
    force_tutorial = db.Column(db.Boolean, default=False)
    
    # Login
    first_login_completed = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    
    # Approvals
    terms_accepted = db.Column(db.Boolean, default=False)
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'


class CountPassword(db.Model):
    """Sayım Şifreleri"""
    __tablename__ = 'count_passwords'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('count_sessions.id'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('envanter_users.id'))
    
    def __repr__(self):
        return f'<CountPassword {self.id}>'


# ============================================================
# TAKEUCHI PARÇA SİPARİŞ MODÜLÜ - AYRIŞTIRILMIŞ TABLOLAR
# ============================================================

class TakeuchiPartOrder(db.Model):
    """
    Takeuchi Parça Siparişleri - Admin tarafından oluşturulan resmi siparişler
    Sipariş Kodu Formatı: CER2025001, CER2025002, vb.
    """
    __tablename__ = 'takeuchi_part_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_code = db.Column(db.String(50), unique=True, nullable=False, index=True)  # CER2025001
    order_name = db.Column(db.String(255))  # Admin tarafından verilen isim
    
    # Durum
    status = db.Column(db.String(50), default='pending')  # pending, completed
    
    # Tarihler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('envanter_users.id'))
    completed_at = db.Column(db.DateTime)  # Tüm parçalar teslim alındığında
    
    # Notlar
    notes = db.Column(db.Text)
    
    # İlişkiler
    items = db.relationship('TakeuchiOrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<TakeuchiPartOrder {self.order_code}>'


class TakeuchiOrderItem(db.Model):
    """
    Takeuchi Siparişindeki Parçalar
    Her parça için: sipariş miktarı, teslim miktarı, teslim durumu
    """
    __tablename__ = 'takeuchi_order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('takeuchi_part_orders.id'), nullable=False)
    
    # Parça bilgileri
    part_code = db.Column(db.String(50), nullable=False, index=True)
    part_name = db.Column(db.String(255))
    
    # Miktarlar
    ordered_quantity = db.Column(db.Integer, nullable=False)  # Sipariş edilen adet
    received_quantity = db.Column(db.Integer, default=0)  # Teslim alınan adet
    
    # Durum: partial, completed (ordered_quantity == received_quantity ise completed)
    status = db.Column(db.String(50), default='pending')  # pending, partial, completed
    
    # Tarihler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    first_received_at = db.Column(db.DateTime)  # İlk teslim tarihi
    fully_received_at = db.Column(db.DateTime)  # Tamamen teslim alındığı tarih
    
    # Notlar
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<TakeuchiOrderItem {self.part_code} in Order {self.order_id}>'


class TakeuchiTempOrder(db.Model):
    """
    Takeuchi Geçici Sipariş Listesi
    Kullanıcı tarafından oluşturulan, henüz resmi hale getirilmemiş parça listesi
    Admin bu listeyi seçip resmi sipariş (TakeuchiPartOrder) oluşturur
    """
    __tablename__ = 'takeuchi_temp_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Her session için benzersiz ID
    
    # Kim tarafından oluşturuldu
    created_by = db.Column(db.Integer, db.ForeignKey('envanter_users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    items = db.relationship('TakeuchiTempOrderItem', backref='temp_order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<TakeuchiTempOrder {self.session_id}>'


class TakeuchiTempOrderItem(db.Model):
    """
    Takeuchi Geçici Sipariş Kalemleri
    Kullanıcı tarafından eklenen, henüz resmi sipariş olmayan parçalar
    """
    __tablename__ = 'takeuchi_temp_order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    temp_order_id = db.Column(db.Integer, db.ForeignKey('takeuchi_temp_orders.id'), nullable=False)
    
    # Parça bilgileri
    part_code = db.Column(db.String(50), nullable=False)
    part_name = db.Column(db.String(255))
    
    # Miktar
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Tarih
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TakeuchiTempOrderItem {self.part_code}>'


class TakeuchiPart(db.Model):
    """
    Takeuchi Parça Katalogु
    Admin tarafından Excel'den yüklenen parçalar
    TAMAMEN İZOLE - Mevcut envanter sisteminden AYRR!
    """
    __tablename__ = 'takeuchi_parts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Temel bilgiler
    part_code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    part_name = db.Column(db.String(255), nullable=False)
    
    # Alternatif bilgiler
    alternative_code = db.Column(db.String(100))  # Değişen parça kodu
    build_out = db.Column(db.String(255))  # Build Out bilgisi
    
    # Maliyet
    cost_price = db.Column(db.Float, default=0.0)  # Geliş fiyatı
    
    # Durumu
    is_active = db.Column(db.Boolean, default=True)
    
    # Tarihler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('envanter_users.id'))
    
    # Notlar
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<TakeuchiPart {self.part_code}>'
