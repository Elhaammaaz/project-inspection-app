"""
Complete normalized database schema for Building Condition Assessment Report (BCAR)
Production-ready with PostgreSQL, audit trails, and BI-friendly structure
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import enum

db = SQLAlchemy()


# ==================== ENUMS ====================

class UserRoleEnum(enum.Enum):
    ADMIN = "Admin"
    PROJECT_MANAGER = "ProjectManager"
    ASSESSOR = "Assessor"
    REVIEWER = "Reviewer"
    VIEWER = "Viewer"


class StatusEnum(enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"
    VERIFIED = "Verified"


class PriorityEnum(enum.Enum):
    P1 = "P1 - Critical"
    P2 = "P2 - High"
    P3 = "P3 - Medium"
    P4 = "P4 - Low"


class ComplianceStatusEnum(enum.Enum):
    YES = "Yes"
    NO = "No"
    PARTIAL = "Partial"
    NA = "N/A"


class TestResultEnum(enum.Enum):
    PASS = "Pass"
    FAIL = "Fail"
    NEED_ATTENTION = "Need Attention"


class CAPAStatusEnum(enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"
    VERIFIED = "Verified"
    OVERDUE = "Overdue"


# ==================== GOVERNANCE ====================

class User(UserMixin, db.Model):
    """User accounts with role-based access"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='Viewer', nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    buildings = db.relationship('Building', backref='created_by_user', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        return self.role == role
    
    @property
    def is_admin(self):
        return self.role == 'Admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


class AuditLog(db.Model):
    """Complete audit trail for governance"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer)
    action = db.Column(db.String(20), nullable=False)  # CREATE, UPDATE, DELETE
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} on {self.table_name}>'


# ==================== LOOKUP TABLES ====================

class Rate(db.Model):
    """Rating scale: 1-5"""
    __tablename__ = 'rates_lookup'
    
    id = db.Column(db.Integer, primary_key=True)
    rate_value = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Rate {self.rate_value}: {self.description}>'


class Weight(db.Model):
    """Item weight scale"""
    __tablename__ = 'weights_lookup'
    
    id = db.Column(db.Integer, primary_key=True)
    weight_value = db.Column(db.Float, unique=True, nullable=False)
    description = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Weight {self.weight_value}>'


class Responsibility(db.Model):
    """Responsibility categories"""
    __tablename__ = 'responsibilities_lookup'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Responsibility {self.name}>'


class Priority(db.Model):
    """Priority levels"""
    __tablename__ = 'priorities_lookup'
    
    id = db.Column(db.Integer, primary_key=True)
    priority_name = db.Column(db.String(50), unique=True, nullable=False)
    order = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Priority {self.priority_name}>'


class ComplianceArea(db.Model):
    """Government compliance areas"""
    __tablename__ = 'compliance_areas_lookup'
    
    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    regulation_code = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<ComplianceArea {self.area_name}>'


# ==================== BUILDING SYSTEMS HIERARCHY ====================

class System(db.Model):
    """21 building systems"""
    __tablename__ = 'systems'
    
    id = db.Column(db.Integer, primary_key=True)
    system_code = db.Column(db.String(20), unique=True, nullable=False)
    system_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    subsystems = db.relationship('Subsystem', backref='system', lazy='dynamic', cascade='all, delete-orphan')
    assessment_items = db.relationship('AssessmentItem', backref='system', lazy='dynamic')
    system_scores = db.relationship('SystemScore', backref='system', lazy='dynamic')
    
    def __repr__(self):
        return f'<System {self.system_name}>'


class Subsystem(db.Model):
    """Subsystems under building systems"""
    __tablename__ = 'subsystems'
    
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'), nullable=False, index=True)
    subsystem_code = db.Column(db.String(30), nullable=False)
    subsystem_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    
    # Relationships
    components = db.relationship('Component', backref='subsystem', lazy='dynamic', cascade='all, delete-orphan')
    assessment_items = db.relationship('AssessmentItem', backref='subsystem', lazy='dynamic')
    
    def __repr__(self):
        return f'<Subsystem {self.subsystem_name}>'


class Component(db.Model):
    """Components under subsystems"""
    __tablename__ = 'components'
    
    id = db.Column(db.Integer, primary_key=True)
    subsystem_id = db.Column(db.Integer, db.ForeignKey('subsystems.id'), nullable=False, index=True)
    component_code = db.Column(db.String(30), nullable=False)
    component_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    
    # Relationships
    assessment_items = db.relationship('AssessmentItem', backref='component', lazy='dynamic')
    
    def __repr__(self):
        return f'<Component {self.component_name}>'


# ==================== CORE BUSINESS ====================

class Building(db.Model):
    """Step 1: Building/Project Information Header"""
    __tablename__ = 'buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Identification
    project_name = db.Column(db.String(200), nullable=False)
    building_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    building_type = db.Column(db.String(100), nullable=False)
    primary_use = db.Column(db.String(100), nullable=False)
    
    # Physical
    gross_built_area_m2 = db.Column(db.Float, nullable=False)
    number_of_floors = db.Column(db.Integer)
    construction_year = db.Column(db.Integer)
    
    # Lifecycle
    last_major_renovation_date = db.Column(db.Date)
    estimated_life_time_years = db.Column(db.Integer)
    planned_asset_retirement_year = db.Column(db.Integer)
    fm_contractor = db.Column(db.String(200))
    
    # Assessment
    inspection_date = db.Column(db.Date, nullable=False)
    current_year = db.Column(db.Integer, nullable=False, default=2026)
    system_threshold_percent = db.Column(db.Float, default=75.0)
    
    # Governance
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='Draft')  # Draft, InProgress, Complete
    
    # Relationships
    assessments = db.relationship('Assessment', backref='building', lazy='dynamic', cascade='all, delete-orphan')
    compliance_checklists = db.relationship('ComplianceChecklist', backref='building', lazy='dynamic', cascade='all, delete-orphan')
    system_scores = db.relationship('SystemScore', backref='building', lazy='dynamic', cascade='all, delete-orphan')
    test_registers = db.relationship('TestRegister', backref='building', lazy='dynamic', cascade='all, delete-orphan')
    capa_registers = db.relationship('CAPARegister', backref='building', lazy='dynamic', cascade='all, delete-orphan')
    dashboard_summary = db.relationship('ExecutiveDashboardSummary', backref='building', uselist=False)
    
    def as_dict(self):
        """Convert to dictionary for audit logging"""
        return {
            'id': self.id,
            'project_name': self.project_name,
            'building_code': self.building_code,
            'city': self.city,
            'building_type': self.building_type,
            'status': self.status
        }
    
    def __repr__(self):
        return f'<Building {self.project_name}>'


class Assessment(db.Model):
    """Step 2: Building Assessment session"""
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False, index=True)
    assessment_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationships
    assessment_items = db.relationship('AssessmentItem', backref='assessment', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Assessment {self.assessment_code}>'


class AssessmentItem(db.Model):
    """Step 2: Individual inspection items"""
    __tablename__ = 'assessment_items'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False, index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'), nullable=False)
    subsystem_id = db.Column(db.Integer, db.ForeignKey('subsystems.id'), nullable=False)
    component_id = db.Column(db.Integer, db.ForeignKey('components.id'), nullable=False)
    
    # Item Definition (read-only)
    item_code = db.Column(db.String(50), nullable=False)
    inspection_item = db.Column(db.String(255), nullable=False)
    criteria = db.Column(db.Text)
    test_method = db.Column(db.String(255))
    
    # Asset Information
    asset_tag_no = db.Column(db.String(100))
    snag_location = db.Column(db.String(255))
    snag_evidence_ref = db.Column(db.String(100))
    snag_evidence_type = db.Column(db.String(50))
    
    # User Input
    rate = db.Column(db.Integer)  # 1-5
    item_weight = db.Column(db.Float)
    risk_criticality = db.Column(db.Integer, default=0)  # 0-5
    responsibility_id = db.Column(db.Integer, db.ForeignKey('responsibilities_lookup.id'))
    priority = db.Column(db.String(20), default='P3')  # P1, P2, P3, P4
    status = db.Column(db.String(20), default='Open')  # Open, In Progress, Closed, Verified
    due_date = db.Column(db.Date)
    remarks = db.Column(db.Text)
    
    # Calculated (READ-ONLY)
    score = db.Column(db.Float)  # Rate × 2 × 10
    score_percent = db.Column(db.Float)  # Score / 100
    weighted_score = db.Column(db.Float)  # Score% × Item Weight
    
    # Relationships
    responsibility = db.relationship('Responsibility')
    capa_records = db.relationship('CAPARegister', backref='assessment_item')
    test_item_links = db.relationship('TestItemLink', backref='assessment_item', cascade='all, delete-orphan')
    
    # Governance
    evidence_file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_scores(self):
        """Server-side calculation"""
        if self.rate:
            self.score = self.rate * 2 * 10
            self.score_percent = self.score / 100.0
            if self.item_weight:
                self.weighted_score = self.score_percent * self.item_weight
    
    def as_dict(self):
        """Convert to dictionary for audit logging"""
        return {
            'id': self.id,
            'item_code': self.item_code,
            'system_id': self.system_id,
            'rate': self.rate,
            'status': self.status,
            'priority': self.priority
        }
    
    def __repr__(self):
        return f'<AssessmentItem {self.item_code}>'


class ComplianceChecklist(db.Model):
    """Step 3: Compliance checklist"""
    __tablename__ = 'compliance_checklist'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False, index=True)
    checklist_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    compliance_items = db.relationship('ComplianceItem', backref='checklist', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ComplianceChecklist {self.checklist_code}>'


class ComplianceItem(db.Model):
    """Step 3: Individual compliance item"""
    __tablename__ = 'compliance_items'
    
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('compliance_checklist.id'), nullable=False, index=True)
    compliance_area_id = db.Column(db.Integer, db.ForeignKey('compliance_areas_lookup.id'), nullable=False)
    
    # Item
    item_code = db.Column(db.String(50), nullable=False)
    requirement = db.Column(db.Text, nullable=False)
    evidence_required = db.Column(db.Boolean, default=True)
    
    # User Input
    status = db.Column(db.String(20))  # Yes, No, Partial, N/A
    evidence_ref = db.Column(db.String(100))
    remarks = db.Column(db.Text)
    evidence_file_path = db.Column(db.String(500))
    
    # Relationships
    compliance_area = db.relationship('ComplianceArea')
    
    # Governance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ComplianceItem {self.item_code}>'


class SystemScore(db.Model):
    """Step 4: System scoring summary"""
    __tablename__ = 'system_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False, index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'), nullable=False, index=True)
    
    # Calculated
    item_count = db.Column(db.Integer, default=0)
    score_percent = db.Column(db.Float)
    weight = db.Column(db.Float, nullable=False, default=0.0)  # USER EDITABLE
    weighted_score = db.Column(db.Float)
    
    # Governance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('building_id', 'system_id', name='uq_building_system'),)
    
    def calculate_weighted_score(self):
        """Calculate Weighted Score = Score % × Weight / 100"""
        if self.score_percent and self.weight:
            self.weighted_score = (self.score_percent * self.weight) / 100.0
    
    def __repr__(self):
        return f'<SystemScore {self.system_id}>'


class TestRegister(db.Model):
    """Step 5: Test register"""
    __tablename__ = 'test_register'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False, index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'), nullable=False)
    
    # Test Definition
    test_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    test_name = db.Column(db.String(200), nullable=False)
    standard_reference = db.Column(db.String(100))
    instrument = db.Column(db.String(150))
    locations_sampling = db.Column(db.Text)
    acceptance_criteria = db.Column(db.Text)
    
    # Test Results
    readings = db.Column(db.JSON)
    result = db.Column(db.String(50))  # Pass, Fail, Need Attention
    witness = db.Column(db.String(100))
    test_date = db.Column(db.Date, nullable=False)
    evidence_ref = db.Column(db.String(100))
    evidence_file_path = db.Column(db.String(500))
    remarks = db.Column(db.Text)
    
    # Relationships
    system = db.relationship('System')
    test_item_links = db.relationship('TestItemLink', backref='test_record', cascade='all, delete-orphan')
    
    # Governance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestRegister {self.test_id}>'


class TestItemLink(db.Model):
    """Many-to-Many: Tests to assessment items"""
    __tablename__ = 'test_item_links'
    
    id = db.Column(db.Integer, primary_key=True)
    test_record_id = db.Column(db.Integer, db.ForeignKey('test_register.id'), nullable=False, index=True)
    assessment_item_id = db.Column(db.Integer, db.ForeignKey('assessment_items.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestItemLink>'


class CAPARegister(db.Model):
    """Step 6: CAPA register"""
    __tablename__ = 'capa_register'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False, index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'), nullable=False)
    assessment_item_id = db.Column(db.Integer, db.ForeignKey('assessment_items.id'), nullable=True)
    
    # CAPA Details
    capa_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    priority = db.Column(db.String(20), nullable=False)  # P1, P2, P3, P4
    finding = db.Column(db.Text, nullable=False)
    required_action = db.Column(db.Text, nullable=False)
    
    # Ownership
    responsibility_id = db.Column(db.Integer, db.ForeignKey('responsibilities_lookup.id'))
    due_date = db.Column(db.Date, nullable=False)
    estimated_cost = db.Column(db.Float)
    
    # Status
    status = db.Column(db.String(20), default='Open')  # Open, In Progress, Closed, Verified, Overdue
    verification_evidence = db.Column(db.String(500))
    verification_date = db.Column(db.Date)
    remarks = db.Column(db.Text)
    
    # Relationships
    system = db.relationship('System')
    responsibility = db.relationship('Responsibility')
    
    # Governance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_overdue(self):
        """Check if CAPA is past due"""
        if self.status not in ['Closed', 'Verified']:
            return self.due_date < date.today()
        return False
    
    def __repr__(self):
        return f'<CAPARegister {self.capa_id}>'


class ExecutiveDashboardSummary(db.Model):
    """Step 7: Executive dashboard (computed summary)"""
    __tablename__ = 'executive_dashboard_summary'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False, index=True, unique=True)
    
    # Overall Metrics
    overall_building_score = db.Column(db.Float)
    overall_compliance_percent = db.Column(db.Float)
    threshold_pass = db.Column(db.Boolean)
    
    # Counts
    total_assessment_items = db.Column(db.Integer, default=0)
    items_open = db.Column(db.Integer, default=0)
    items_in_progress = db.Column(db.Integer, default=0)
    items_closed = db.Column(db.Integer, default=0)
    items_verified = db.Column(db.Integer, default=0)
    
    risk_critical = db.Column(db.Integer, default=0)
    risk_high = db.Column(db.Integer, default=0)
    risk_medium = db.Column(db.Integer, default=0)
    risk_low = db.Column(db.Integer, default=0)
    risk_acceptable = db.Column(db.Integer, default=0)
    
    capa_open = db.Column(db.Integer, default=0)
    capa_in_progress = db.Column(db.Integer, default=0)
    capa_closed = db.Column(db.Integer, default=0)
    capa_overdue = db.Column(db.Integer, default=0)
    
    test_pass = db.Column(db.Integer, default=0)
    test_fail = db.Column(db.Integer, default=0)
    test_need_attention = db.Column(db.Integer, default=0)
    
    # Narrative
    notes_observations = db.Column(db.Text)
    
    # Governance
    computed_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExecutiveDashboardSummary {self.building_id}>'
