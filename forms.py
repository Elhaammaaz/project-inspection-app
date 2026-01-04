from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional, NumberRange
from models import User


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    submit = SubmitField('Sign In')
    
    def validate_email(self, field):
        """Check if email exists in database and is active"""
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('Email or password is incorrect')
        if not user.active:
            raise ValidationError('Your account is pending approval. Please wait for admin confirmation.')


class RegistrationForm(FlaskForm):
    """User registration form"""
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address'),
        Length(min=5, max=120)
    ], render_kw={'placeholder': 'your@email.com'})
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ], render_kw={'placeholder': 'At least 6 characters'})
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password')
    ], render_kw={'placeholder': 'Repeat password'})
    
    submit = SubmitField('Request Account')
    
    def validate_email(self, field):
        """Check if email already exists"""
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already registered. Please login or use a different email.')
    
    def validate_confirm_password(self, field):
        """Check if passwords match"""
        if field.data != self.password.data:
            raise ValidationError('Passwords do not match')


class ProjectInspectionForm(FlaskForm):
    """Comprehensive Project Inspection form"""
    
    # Project Information Section
    project_name = StringField('Project / Building Name', validators=[
        DataRequired(message='Project name is required'),
        Length(min=1, max=255)
    ], render_kw={'placeholder': 'Enter project/building name'})
    
    city = StringField('City', validators=[Optional(), Length(max=255)], render_kw={'placeholder': 'Enter city name'})
    address = StringField('Address', validators=[Optional(), Length(max=500)], render_kw={'placeholder': 'Enter full address'})
    
    gps_latitude = FloatField('GPS Latitude', validators=[Optional(), NumberRange(min=-90, max=90)])
    gps_longitude = FloatField('GPS Longitude', validators=[Optional(), NumberRange(min=-180, max=180)])
    
    # Building Details
    building_type = StringField('Building Type', validators=[Optional(), Length(max=255)], render_kw={'placeholder': 'e.g., Residential, Commercial, Industrial'})
    primary_use = StringField('Primary Use', validators=[Optional(), Length(max=255)], render_kw={'placeholder': 'e.g., Office, Warehouse, Shopping Center'})
    gross_built_area = FloatField('Gross Built Area (m²)', validators=[Optional(), NumberRange(min=0)])
    number_of_floors = IntegerField('Number of Floors', validators=[Optional(), NumberRange(min=0)])
    
    # Dates
    last_renovation_date = DateField('Last Major Renovation Date', validators=[Optional()], format='%Y-%m-%d')
    construction_year = IntegerField('Construction Year', validators=[Optional(), NumberRange(min=1800, max=2100)])
    current_year = IntegerField('Current Year', validators=[Optional(), NumberRange(min=1800, max=2100)])
    estimated_life_time = IntegerField('Estimated Life Time (years)', validators=[Optional(), NumberRange(min=0)])
    planned_retirement_year = IntegerField('Planned Asset Retirement Year', validators=[Optional(), NumberRange(min=1800, max=2100)])
    inspection_date = DateField('Inspection Date', validators=[Optional()], format='%Y-%m-%d')
    
    # Management
    fm_contractor = StringField('FM Contractor / Service Provider', validators=[Optional(), Length(max=500)], render_kw={'placeholder': 'Enter contractor name'})
    system_threshold = FloatField('System Threshold (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    # Assessment Results
    inspection_result = SelectField('Inspection Result', choices=[
        ('', '-- Select Result --'),
        ('Passed', 'Passed'),
        ('Passed but Need Attention', 'Passed but Need Attention'),
        ('Not Complied', 'Not Complied'),
        ('Pending', 'Pending')
    ], validators=[Optional()])
    
    building_score = FloatField('Building Score', validators=[Optional(), NumberRange(min=0, max=100)])
    high_priority_classified = IntegerField('High Priority Classified', validators=[Optional(), NumberRange(min=0)])
    fm_performance = FloatField('FM Performance', validators=[Optional(), NumberRange(min=0, max=100)])
    government_compliance = SelectField('Government Compliance', choices=[
        ('', '-- Select Status --'),
        ('Complied', 'Complied'),
        ('Not Complied', 'Not Complied'),
        ('Partial Compliance', 'Partial Compliance'),
        ('Pending Review', 'Pending Review')
    ], validators=[Optional()])
    
    # Fire & Safety & Other Metrics
    fire_life_safety = FloatField('Fire & Life Safety (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    total_economic_life = IntegerField('Total Economic Life (years)', validators=[Optional(), NumberRange(min=0)])
    chronological_age = IntegerField('Chronological (Actual) Age (years)', validators=[Optional(), NumberRange(min=0)])
    estimated_effective_age = IntegerField('Estimated Effective Age (years)', validators=[Optional(), NumberRange(min=0)])
    estimated_remaining_life = IntegerField('Estimated Remaining Life (years)', validators=[Optional(), NumberRange(min=0)])
    
    # Notes
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=5000)], render_kw={
        'rows': 5,
        'placeholder': 'Add any additional observations, recommendations, or notes from the inspection'
    })
    
    submit = SubmitField('Save Project Inspection')
