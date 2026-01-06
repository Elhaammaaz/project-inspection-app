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
    active = db.Column(db.Integer, default=0, nullable=False)  # 0 = pending, 1 = approved
    approved_at = db.Column(db.DateTime, nullable=True)
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_admin = db.Column(db.Integer, default=0, nullable=False)  # 0 = regular user, 1 = admin
    # Relationships
    project_inspections = db.relationship('ProjectInspection', backref='user', lazy=True, cascade='all, delete-orphan')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
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
    """Building System Performance - Detail table with one row per system"""
    __tablename__ = 'inspection_systems'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('project_inspections.id', ondelete='CASCADE'), 
                                     nullable=False, index=True)
    
    # System Information
    system_name = db.Column(db.String(255), nullable=False)
    system_type = db.Column(db.String(255), nullable=True)
    condition_rating = db.Column(db.String(50), nullable=True)  # Excellent, Good, Fair, Poor, Critical
    last_maintenance = db.Column(db.Date, nullable=True)
    maintenance_notes = db.Column(db.Text, nullable=True)
    next_maintenance = db.Column(db.Date, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<InspectionSystem {self.id} - {self.system_name}>'












