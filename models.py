from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Approval System
    active = db.Column(db.Integer, default=0, nullable=False)  # 0 = pending, 1 = approved
    approved_at = db.Column(db.DateTime, nullable=True)
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Access Control (1 = approved, 0 = pending/rejected)
    can_view_dashboard = db.Column(db.Integer, default=0, nullable=False)
    can_view_reports = db.Column(db.Integer, default=0, nullable=False)
    can_export_data = db.Column(db.Integer, default=0, nullable=False)
    can_manage_users = db.Column(db.Integer, default=0, nullable=False)
    
    # Access Request Tracking
    dashboard_requested = db.Column(db.Integer, default=0, nullable=False)  # 1 = requested, 0 = not requested
    dashboard_request_date = db.Column(db.DateTime, nullable=True)
    dashboard_approved_date = db.Column(db.DateTime, nullable=True)
    
    reports_requested = db.Column(db.Integer, default=0, nullable=False)
    reports_request_date = db.Column(db.DateTime, nullable=True)
    reports_approved_date = db.Column(db.DateTime, nullable=True)
    
    export_requested = db.Column(db.Integer, default=0, nullable=False)
    export_request_date = db.Column(db.DateTime, nullable=True)
    export_approved_date = db.Column(db.DateTime, nullable=True)
    
    # Self-referential relationship for approver (only one direction)
    approver = db.relationship('User', remote_side=[id], foreign_keys=[approved_by_id], 
                              backref='approved_users', cascade='all')
    
    # Relationships
    project_inspections = db.relationship('ProjectInspection', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and store the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class ProjectInspection(db.Model):
    """Project Inspection model - Main table with all basic information"""
    __tablename__ = 'project_inspections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # SCREEN 1: Project Information
    project_name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    gps_latitude = db.Column(db.Float, nullable=True)
    gps_longitude = db.Column(db.Float, nullable=True)
    
    # SCREEN 1: Building Details
    building_type = db.Column(db.String(255), nullable=True)
    primary_use = db.Column(db.String(255), nullable=True)
    gross_built_area = db.Column(db.Float, nullable=True)
    number_of_floors = db.Column(db.Integer, nullable=True)
    
    # SCREEN 1: Dates & Timeline
    last_renovation_date = db.Column(db.Date, nullable=True)
    fm_contractor = db.Column(db.String(500), nullable=True)
    current_year = db.Column(db.Integer, nullable=True)
    construction_year = db.Column(db.Integer, nullable=True)
    estimated_life_time = db.Column(db.Integer, nullable=True)
    planned_retirement_year = db.Column(db.Integer, nullable=True)
    system_threshold = db.Column(db.Float, nullable=True)
    inspection_date = db.Column(db.Date, nullable=True)
    
    # SCREEN 2: Life & Aging Metrics
    total_economic_life = db.Column(db.Integer, nullable=True)
    chronological_age = db.Column(db.Integer, nullable=True)
    estimated_effective_age = db.Column(db.Integer, nullable=True)
    estimated_remaining_life = db.Column(db.Integer, nullable=True)
    
    # SCREEN 3: Assessment Results
    inspection_result = db.Column(db.String(100), nullable=True)
    building_score = db.Column(db.Float, nullable=True)
    high_priority_classified = db.Column(db.Integer, nullable=True, default=0)
    fm_performance = db.Column(db.Float, nullable=True)
    government_compliance = db.Column(db.String(50), nullable=True)
    
    # SCREEN 2: Fire & Life Safety Summary
    fire_life_safety = db.Column(db.Float, nullable=True)
    
    # Additional Metadata
    notes = db.Column(db.Text, nullable=True)
    inspection_status = db.Column(db.String(50), default='draft')  # draft, completed, reviewed
    inspection_by = db.Column(db.String(255), nullable=True)
    reviewed_by = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to inspection systems (21 systems per inspection)
    systems = db.relationship('InspectionSystem', backref='inspection', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ProjectInspection {self.id} - {self.project_name}>'


class InspectionSystem(db.Model):
    """Building System Performance - Detail table with one row per system (21 systems per inspection)"""
    __tablename__ = 'inspection_systems'
    
    id = db.Column(db.Integer, primary_key=True)
    project_inspection_id = db.Column(db.Integer, db.ForeignKey('project_inspections.id', ondelete='CASCADE'), 
                                     nullable=False, index=True)
    
    # System Information
    system_name = db.Column(db.String(255), nullable=False)  # Fire_LifeSafety, Electrical, etc.
    item_count = db.Column(db.Integer, nullable=True)
    score_percentage = db.Column(db.Float, nullable=True)  # e.g., 54, 73, 78
    weight = db.Column(db.Float, nullable=True)  # e.g., 17.00, 10.00, 2.00
    weighted_score = db.Column(db.Float, nullable=True)  # e.g., 9, 7, 2
    status = db.Column(db.String(50), nullable=True)  # Critical, Warning, Good
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<InspectionSystem {self.id} - {self.system_name}>'


class UserProfile(db.Model):
    """User profile information for dashboard access and personal data management"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    # Profile Information
    department = db.Column(db.String(255), nullable=True)
    job_title = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    office_location = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), default='user')  # user, admin, manager
    
    # Permissions
    can_view_dashboard = db.Column(db.Integer, default=0)  # 0 = no, 1 = yes
    can_view_reports = db.Column(db.Integer, default=0)
    dashboard_access_approved_at = db.Column(db.DateTime, nullable=True)
    
    # Preferences
    theme = db.Column(db.String(50), default='light')  # light, dark
    notifications_enabled = db.Column(db.Integer, default=1)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='profile', uselist=False)
    
    def __repr__(self):
        return f'<UserProfile {self.user_id}>'


class DashboardAccessRequest(db.Model):
    """Track requests for dashboard access with admin approval workflow"""
    __tablename__ = 'dashboard_access_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='dashboard_requests')
    approved_by = db.relationship('User', foreign_keys=[approved_by_id])
    
    def __repr__(self):
        return f'<DashboardAccessRequest {self.id} - User {self.user_id}>'


class ProfileChangeRequest(db.Model):
    """Track profile change requests that require admin approval"""
    __tablename__ = 'profile_change_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    
    # Changes Requested
    field_name = db.Column(db.String(255), nullable=False)  # full_name, phone, department, etc.
    old_value = db.Column(db.Text, nullable=True)
    new_value = db.Column(db.Text, nullable=False)
    
    # Admin Review
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='profile_change_requests')
    reviewed_by = db.relationship('User', foreign_keys=[reviewed_by_id])
    
    def __repr__(self):
        return f'<ProfileChangeRequest {self.id} - User {self.user_id}>'
