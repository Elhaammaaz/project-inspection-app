from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, ProjectInspection
from forms import LoginForm, ProjectInspectionForm
from datetime import datetime


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables and seed demo account
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Database initialization error: {e}")
            print(f"⚠ Database initialization warning: {e}")
        
        # Create demo account if it doesn't exist
        try:
            demo_user = User.query.filter_by(email='demo@example.com').first()
            if not demo_user:
                demo_user = User(email='demo@example.com')
                demo_user.set_password('demo123')
                db.session.add(demo_user)
                db.session.commit()
                print("✓ Demo account created: demo@example.com / demo123")
        except Exception as e:
            app.logger.error(f"Demo user creation error: {e}")
            db.session.rollback()
            print(f"⚠ Demo user creation warning: {e}")
    
    # ==================== ROUTES ====================
    
    @app.route('/')
    def index():
        """Home page - redirect to dashboard if logged in, login if not"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login route"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Email or password is incorrect', 'danger')
        
        return render_template('login.html', form=form)
    
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout route"""
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('login'))
    
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Dashboard showing all project inspections for current user"""
        page = request.args.get('page', 1, type=int)
        projects = ProjectInspection.query.filter_by(user_id=current_user.id)\
            .order_by(ProjectInspection.created_at.desc())\
            .paginate(page=page, per_page=10)
        
        return render_template('dashboard.html', projects=projects)
    
    
    @app.route('/new', methods=['GET', 'POST'])
    @login_required
    def new_inspection():
        """Create new project inspection"""
        form = ProjectInspectionForm()
        if form.validate_on_submit():
            inspection = ProjectInspection(
                user_id=current_user.id,
                project_name=form.project_name.data,
                city=form.city.data,
                address=form.address.data,
                gps_latitude=form.gps_latitude.data,
                gps_longitude=form.gps_longitude.data,
                building_type=form.building_type.data,
                primary_use=form.primary_use.data,
                gross_built_area=form.gross_built_area.data,
                number_of_floors=form.number_of_floors.data,
                last_renovation_date=form.last_renovation_date.data,
                construction_year=form.construction_year.data,
                current_year=form.current_year.data,
                estimated_life_time=form.estimated_life_time.data,
                planned_retirement_year=form.planned_retirement_year.data,
                inspection_date=form.inspection_date.data,
                fm_contractor=form.fm_contractor.data,
                system_threshold=form.system_threshold.data,
                inspection_result=form.inspection_result.data,
                building_score=form.building_score.data,
                high_priority_classified=form.high_priority_classified.data,
                fm_performance=form.fm_performance.data,
                government_compliance=form.government_compliance.data,
                fire_life_safety=form.fire_life_safety.data,
                total_economic_life=form.total_economic_life.data,
                chronological_age=form.chronological_age.data,
                estimated_effective_age=form.estimated_effective_age.data,
                estimated_remaining_life=form.estimated_remaining_life.data,
                notes=form.notes.data
            )
            db.session.add(inspection)
            db.session.commit()
            
            flash('Project inspection saved successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        return render_template('form.html', form=form)
    
    
    @app.route('/view/<int:project_id>')
    @login_required
    def view_inspection(project_id):
        """View project inspection details"""
        inspection = ProjectInspection.query.get_or_404(project_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to view this project.', 'danger')
            return redirect(url_for('dashboard'))
        
        return render_template('view.html', inspection=inspection)
    
    
    @app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
    @login_required
    def edit_inspection(project_id):
        """Edit project inspection"""
        inspection = ProjectInspection.query.get_or_404(project_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to edit this project.', 'danger')
            return redirect(url_for('dashboard'))
        
        form = ProjectInspectionForm()
        if form.validate_on_submit():
            inspection.project_name = form.project_name.data
            inspection.city = form.city.data
            inspection.address = form.address.data
            inspection.gps_latitude = form.gps_latitude.data
            inspection.gps_longitude = form.gps_longitude.data
            inspection.building_type = form.building_type.data
            inspection.primary_use = form.primary_use.data
            inspection.gross_built_area = form.gross_built_area.data
            inspection.number_of_floors = form.number_of_floors.data
            inspection.last_renovation_date = form.last_renovation_date.data
            inspection.construction_year = form.construction_year.data
            inspection.current_year = form.current_year.data
            inspection.estimated_life_time = form.estimated_life_time.data
            inspection.planned_retirement_year = form.planned_retirement_year.data
            inspection.inspection_date = form.inspection_date.data
            inspection.fm_contractor = form.fm_contractor.data
            inspection.system_threshold = form.system_threshold.data
            inspection.inspection_result = form.inspection_result.data
            inspection.building_score = form.building_score.data
            inspection.high_priority_classified = form.high_priority_classified.data
            inspection.fm_performance = form.fm_performance.data
            inspection.government_compliance = form.government_compliance.data
            inspection.fire_life_safety = form.fire_life_safety.data
            inspection.total_economic_life = form.total_economic_life.data
            inspection.chronological_age = form.chronological_age.data
            inspection.estimated_effective_age = form.estimated_effective_age.data
            inspection.estimated_remaining_life = form.estimated_remaining_life.data
            inspection.notes = form.notes.data
            inspection.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Project inspection updated successfully!', 'success')
            return redirect(url_for('view_inspection', project_id=inspection.id))
        
        elif request.method == 'GET':
            form.project_name.data = inspection.project_name
            form.city.data = inspection.city
            form.address.data = inspection.address
            form.gps_latitude.data = inspection.gps_latitude
            form.gps_longitude.data = inspection.gps_longitude
            form.building_type.data = inspection.building_type
            form.primary_use.data = inspection.primary_use
            form.gross_built_area.data = inspection.gross_built_area
            form.number_of_floors.data = inspection.number_of_floors
            form.last_renovation_date.data = inspection.last_renovation_date
            form.construction_year.data = inspection.construction_year
            form.current_year.data = inspection.current_year
            form.estimated_life_time.data = inspection.estimated_life_time
            form.planned_retirement_year.data = inspection.planned_retirement_year
            form.inspection_date.data = inspection.inspection_date
            form.fm_contractor.data = inspection.fm_contractor
            form.system_threshold.data = inspection.system_threshold
            form.inspection_result.data = inspection.inspection_result
            form.building_score.data = inspection.building_score
            form.high_priority_classified.data = inspection.high_priority_classified
            form.fm_performance.data = inspection.fm_performance
            form.government_compliance.data = inspection.government_compliance
            form.fire_life_safety.data = inspection.fire_life_safety
            form.total_economic_life.data = inspection.total_economic_life
            form.chronological_age.data = inspection.chronological_age
            form.estimated_effective_age.data = inspection.estimated_effective_age
            form.estimated_remaining_life.data = inspection.estimated_remaining_life
            form.notes.data = inspection.notes
        
        return render_template('form.html', form=form, inspection=inspection)
    
    
    @app.route('/delete/<int:project_id>', methods=['POST'])
    @login_required
    def delete_inspection(project_id):
        """Delete project inspection"""
        inspection = ProjectInspection.query.get_or_404(project_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to delete this project.', 'danger')
            return redirect(url_for('dashboard'))
        
        db.session.delete(inspection)
        db.session.commit()
        flash('Project inspection deleted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration route"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            # Check if user already exists
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered. Please log in.', 'warning')
                return redirect(url_for('login'))
            
            # Create new user
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
