"""
WTForms for 7-step BCAR workflow
Server-side validation for all data entry
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, IntegerField, FloatField,
    TextAreaField, SelectField, DateField, BooleanField, FileField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, NumberRange, Optional, ValidationError
)
from models import User, Building, System, Rate, Weight, Priority, Responsibility


# ==================== AUTH FORMS ====================

class LoginForm(FlaskForm):
    """User login"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    """User registration"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


# ==================== STEP 1: BUILDING INFORMATION ====================

# Building Type choices from Excel
BUILDING_TYPE_CHOICES = [
    ('', '-- Select Building Type --'),
    ('LOAD-BEARING MASONRY', 'Load-Bearing Masonry'),
    ('STEEL FRAME', 'Steel Frame'),
    ('REINFORCED CONCRETE (RC)', 'Reinforced Concrete (RC)'),
    ('TIMBER/ WOOD FRAME', 'Timber / Wood Frame'),
    ('PRECAST/ PREFABRICATED', 'Precast / Prefabricated'),
    ('COMPOSITE', 'Composite')
]

# Primary Use choices from Excel
PRIMARY_USE_CHOICES = [
    ('', '-- Select Primary Use --'),
    ('RESIDENTIAL', 'Residential'),
    ('COMMERCIAL', 'Commercial'),
    ('INDUSTRIAL', 'Industrial'),
    ('INSTITUTIONAL / PUBLIC', 'Institutional / Public'),
    ('INFRASTRUCTURAL', 'Infrastructural'),
    ('AGRICULTURAL', 'Agricultural'),
    ('ADMIN', 'Administrative')
]

class BuildingHeaderForm(FlaskForm):
    """Step 1: Building/Project information"""
    
    project_name = StringField('Project / Building Name*', 
        validators=[DataRequired(), Length(min=3, max=200)])
    city = StringField('City*', 
        validators=[DataRequired(), Length(max=100)])
    address = StringField('Address*', 
        validators=[DataRequired(), Length(max=255)])
    latitude = FloatField('Latitude (GPS)', 
        validators=[Optional(), NumberRange(min=-90, max=90)])
    longitude = FloatField('Longitude (GPS)', 
        validators=[Optional(), NumberRange(min=-180, max=180)])
    building_type = SelectField('Building Type*', 
        choices=BUILDING_TYPE_CHOICES, validators=[DataRequired()])
    primary_use = SelectField('Primary Use*', 
        choices=PRIMARY_USE_CHOICES, validators=[DataRequired()])
    gross_built_area_m2 = FloatField('Gross Built Area (m²)*', 
        validators=[DataRequired(), NumberRange(min=0)])
    number_of_floors = IntegerField('Number of Floors*', 
        validators=[DataRequired(), NumberRange(min=1)])
    construction_year = IntegerField('Construction Year*', 
        validators=[DataRequired(), NumberRange(min=1900, max=2099)])
    last_major_renovation_date = DateField('Last Major Renovation Date', 
        validators=[Optional()])
    estimated_life_time_years = IntegerField('Estimated Life Time (Years)*', 
        validators=[DataRequired(), NumberRange(min=1, max=200)])
    planned_asset_retirement_year = IntegerField('Planned Asset Retirement Year', 
        validators=[Optional(), NumberRange(min=2000, max=2200)])
    fm_contractor = StringField('FM Contractor / Service Provider', 
        validators=[Optional(), Length(max=200)])
    inspection_date = DateField('Inspection Date*', 
        validators=[DataRequired()])
    current_year = IntegerField('Current Year*', 
        validators=[DataRequired(), NumberRange(min=2020, max=2099)])
    system_threshold_percent = FloatField('System Threshold (%)*', 
        validators=[DataRequired(), NumberRange(min=0, max=100)])
    
    submit = SubmitField('Create Building & Continue')


# ==================== STEP 2: ASSESSMENT ITEMS ====================

class AssessmentItemForm(FlaskForm):
    """Step 2: Individual assessment item (read-only calculated fields)"""
    
    # Custom validator for non-zero selection
    def validate_system(form, field):
        if field.data is None or field.data == 0:
            raise ValidationError('Please select a system')
    
    # These are for display/selection - not all editable
    system = SelectField('System*', coerce=int, validators=[DataRequired(message="Please select a system")])
    subsystem = SelectField('Subsystem*', coerce=int, validators=[Optional()], choices=[])
    component = SelectField('Component*', coerce=int, validators=[Optional()], choices=[])
    
    # Item reference (editable)
    item_code = StringField('Item Code', validators=[Optional()])
    inspection_item = TextAreaField('Inspection Item', validators=[Optional()])
    criteria = TextAreaField('Criteria', validators=[Optional()])
    test_method = TextAreaField('Test Method', validators=[Optional()])
    
    # Asset & Location
    asset_tag_no = StringField('Asset Tag No.', validators=[Optional(), Length(max=100)])
    snag_location = StringField('Snag Location', validators=[Optional(), Length(max=255)])
    snag_evidence_ref = StringField('Snag Evidence Ref.', validators=[Optional(), Length(max=100)])
    snag_evidence_type = SelectField('Snag Evidence Type', 
        choices=[('Photo', 'Photo'), ('Video', 'Video'), ('Report', 'Report'), ('IR Scan', 'IR Scan')],
        validators=[Optional()])
    
    # Rating & Weight (USER EDITABLE)
    rate = SelectField('Rate (1-5)*', coerce=int, validators=[DataRequired()])
    item_weight = SelectField('Item Weight*', coerce=float, validators=[DataRequired()])
    
    # Risk & Actions
    risk_criticality = SelectField('Risk Criticality (0-5)*', coerce=int, 
        choices=[(i, str(i)) for i in range(6)], validators=[DataRequired()])
    responsibility = SelectField('Responsibility', coerce=int, validators=[Optional()])
    priority = SelectField('Priority*', validators=[DataRequired()], 
        choices=[('P1', 'P1 - Critical'), ('P2', 'P2 - High'), ('P3', 'P3 - Medium'), ('P4', 'P4 - Low')])
    status = SelectField('Status*', validators=[DataRequired()],
        choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed'), ('Verified', 'Verified')])
    due_date = DateField('Due Date', validators=[Optional()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    
    # Calculated fields (READ-ONLY, populated server-side)
    score = FloatField('Score (calculated)', render_kw={'readonly': True})
    score_percent = FloatField('Score % (calculated)', render_kw={'readonly': True})
    weighted_score = FloatField('Weighted Score (calculated)', render_kw={'readonly': True})
    
    # Evidence
    evidence_file = FileField('Upload Evidence', validators=[Optional()])
    
    submit = SubmitField('Save Item')
    submit_next = SubmitField('Save & Next: Compliance Checklist')


# ==================== STEP 3: COMPLIANCE CHECKLIST ====================

class ComplianceItemForm(FlaskForm):
    """Step 3: Individual compliance item"""
    
    item_code = StringField('Item Code', render_kw={'readonly': True})
    compliance_area = StringField('Compliance Area', render_kw={'readonly': True})
    requirement = TextAreaField('Requirement', render_kw={'readonly': True})
    evidence_required = BooleanField('Evidence Required', render_kw={'readonly': True})
    
    # User input
    status = SelectField('Status*', validators=[DataRequired()],
        choices=[('Yes', 'Yes'), ('No', 'No'), ('Partial', 'Partial'), ('N/A', 'N/A')])
    evidence_ref = StringField('Evidence Ref.', validators=[Optional(), Length(max=100)])
    evidence_file = FileField('Upload Evidence', validators=[Optional()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    
    submit = SubmitField('Save Compliance Item')


# ==================== STEP 4: SYSTEM SCORING ====================

class SystemScoringForm(FlaskForm):
    """Step 4: System weight adjustment (weight is USER EDITABLE only)"""
    
    system = StringField('System', render_kw={'readonly': True})
    item_count = IntegerField('Item Count', render_kw={'readonly': True})
    score_percent = FloatField('Score %', render_kw={'readonly': True})
    weight = FloatField('Weight* (must sum to 100)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    weighted_score = FloatField('Weighted Score', render_kw={'readonly': True})
    
    submit = SubmitField('Update Weight')
    submit_all = SubmitField('Save All Weights & Continue')


# ==================== STEP 5: TEST REGISTER ====================

class TestRegisterForm(FlaskForm):
    """Step 5: Test record"""
    
    system = SelectField('System*', coerce=int, validators=[DataRequired()])
    test_id = StringField('Test ID*', validators=[DataRequired(), Length(max=50)])
    test_name = StringField('Test Name*', validators=[DataRequired(), Length(max=200)])
    standard_reference = StringField('Standard / Reference', validators=[Optional(), Length(max=100)])
    instrument = StringField('Instrument', validators=[Optional(), Length(max=150)])
    locations_sampling = TextAreaField('Locations / Sampling', validators=[Optional()])
    acceptance_criteria = TextAreaField('Acceptance Criteria', validators=[Optional()])
    
    # Test results
    readings = TextAreaField('Readings (JSON or notes)', validators=[Optional()])
    result = SelectField('Result*', validators=[DataRequired()],
        choices=[('Pass', 'Pass'), ('Fail', 'Fail'), ('Need Attention', 'Need Attention')])
    test_date = DateField('Test Date*', validators=[DataRequired()])
    witness = StringField('Witness', validators=[Optional(), Length(max=100)])
    evidence_ref = StringField('Evidence Ref.', validators=[Optional(), Length(max=100)])
    evidence_file = FileField('Upload Evidence', validators=[Optional()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    
    submit = SubmitField('Save Test Record')
    submit_next = SubmitField('Save & Next: CAPA Register')


# ==================== STEP 6: CAPA REGISTER ====================

class CAPARegisterForm(FlaskForm):
    """Step 6: CAPA record"""
    
    capa_id = StringField('CAPA ID*', validators=[DataRequired(), Length(max=50)])
    system = SelectField('System*', coerce=int, validators=[DataRequired()])
    priority = SelectField('Priority*', validators=[DataRequired()],
        choices=[('P1', 'P1 - Critical'), ('P2', 'P2 - High'), ('P3', 'P3 - Medium'), ('P4', 'P4 - Low')])
    
    finding = TextAreaField('Finding*', validators=[DataRequired()])
    required_action = TextAreaField('Required Action*', validators=[DataRequired()])
    responsibility = SelectField('Responsibility', coerce=int, validators=[Optional()])
    due_date = DateField('Due Date*', validators=[DataRequired()])
    estimated_cost = FloatField('Estimated Cost', validators=[Optional()])
    
    status = SelectField('Status*', validators=[DataRequired()],
        choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed'), 
                 ('Verified', 'Verified'), ('Overdue', 'Overdue')])
    verification_evidence = StringField('Verification Evidence', validators=[Optional(), Length(max=500)])
    verification_date = DateField('Verification Date', validators=[Optional()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    
    submit = SubmitField('Save CAPA Record')
    submit_next = SubmitField('Save & View Dashboard')

