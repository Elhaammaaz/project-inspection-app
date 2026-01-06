from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, ProjectInspection, InspectionSystem
from forms import LoginForm, RegistrationForm, ProjectInspectionForm, InspectionSystemForm
from datetime import datetime


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Login manager setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # ==================== AUTHENTICATION ROUTES ====================
    
    @app.route('/')
    def index():
        """Home page - redirect to inspections if logged in, login if not"""
        if current_user.is_authenticated:
            return redirect(url_for('inspections'))
        return redirect(url_for('login'))
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login route"""
        if current_user.is_authenticated:
            return redirect(url_for('inspections'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data) and user.active:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('inspections'))
            else:
                flash('Email or password is incorrect, or your account is pending approval.', 'danger')
        
        return render_template('login.html', form=form)
    
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration route - creates pending account"""
        if current_user.is_authenticated:
            return redirect(url_for('inspections'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                # Create new user (inactive by default)
                user = User(email=form.email.data, full_name=form.full_name.data)
                user.set_password(form.password.data)
                user.active = 0  # Pending approval
                db.session.add(user)
                db.session.commit()
                flash('Registration successful! Your account is pending approval.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error during registration: {str(e)}', 'danger')
        return render_template('register.html', form=form)
    
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout route"""
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))
    
    
    # ==================== INSPECTION ROUTES ====================
    
    @app.route('/inspections')
    @login_required
    def inspections():
        """View all inspections for current user"""
        inspections = ProjectInspection.query.filter_by(user_id=current_user.id).all()
        return render_template('inspections.html', inspections=inspections)
    
    
    @app.route('/inspection/new', methods=['GET', 'POST'])
    @login_required
    def new_inspection():
        """Create new inspection"""
        form = ProjectInspectionForm()
        if form.validate_on_submit():
            try:
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
                    notes=form.notes.data,
                    inspection_status=form.inspection_status.data,
                    inspection_by=form.inspection_by.data,
                    reviewed_by=form.reviewed_by.data
                )
                db.session.add(inspection)
                db.session.commit()
                
                flash(f'✓ Inspection "{inspection.project_name}" created successfully!', 'success')
                return redirect(url_for('view_inspection', inspection_id=inspection.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating inspection: {str(e)}', 'danger')
        
        return render_template('inspection_form.html', form=form)
    
    
    @app.route('/inspection/<int:inspection_id>', methods=['GET'])
    @login_required
    def view_inspection(inspection_id):
        """View project inspection details with all 21 systems"""
        inspection = ProjectInspection.query.get_or_404(inspection_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to view this inspection.', 'danger')
            return redirect(url_for('inspections'))
        
        return render_template('view_inspection.html', inspection=inspection)
    
    
    @app.route('/inspection/<int:inspection_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_inspection(inspection_id):
        """Edit project inspection"""
        inspection = ProjectInspection.query.get_or_404(inspection_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to edit this inspection.', 'danger')
            return redirect(url_for('inspections'))
        
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
            inspection.inspection_status = form.inspection_status.data
            inspection.inspection_by = form.inspection_by.data
            inspection.reviewed_by = form.reviewed_by.data
            inspection.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash(f'✓ Inspection "{inspection.project_name}" updated successfully!', 'success')
            return redirect(url_for('view_inspection', inspection_id=inspection.id))
        
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
            form.inspection_status.data = inspection.inspection_status
            form.inspection_by.data = inspection.inspection_by
            form.reviewed_by.data = inspection.reviewed_by
        
        return render_template('inspection_form.html', form=form, inspection=inspection)
    
    
    @app.route('/inspection/<int:inspection_id>/delete', methods=['POST'])
    @login_required
    def delete_inspection(inspection_id):
        """Delete inspection"""
        inspection = ProjectInspection.query.get_or_404(inspection_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to delete this inspection.', 'danger')
            return redirect(url_for('inspections'))
        
        try:
            db.session.delete(inspection)
            db.session.commit()
            flash('✓ Inspection deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting inspection: {str(e)}', 'danger')
        
        return redirect(url_for('inspections'))
    
    
    # ==================== INSPECTION SYSTEM ROUTES ====================
    
    @app.route('/inspection/<int:inspection_id>/system/add', methods=['GET', 'POST'])
    @login_required
    def add_system(inspection_id):
        """Add inspection system to a project"""
        inspection = ProjectInspection.query.get_or_404(inspection_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to edit this inspection.', 'danger')
            return redirect(url_for('inspections'))
        
        form = InspectionSystemForm()
        if form.validate_on_submit():
            try:
                system = InspectionSystem(
                    inspection_id=inspection.id,
                    system_name=form.system_name.data,
                    system_type=form.system_type.data,
                    condition_rating=form.condition_rating.data,
                    last_maintenance=form.last_maintenance.data,
                    maintenance_notes=form.maintenance_notes.data,
                    next_maintenance=form.next_maintenance.data
                )
                db.session.add(system)
                db.session.commit()
                
                flash(f'✓ System "{system.system_name}" added successfully!', 'success')
                return redirect(url_for('view_inspection', inspection_id=inspection.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding system: {str(e)}', 'danger')
        
        return render_template('system_form.html', form=form, inspection=inspection)
    
    
    @app.route('/system/<int:system_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_system(system_id):
        """Edit inspection system"""
        system = InspectionSystem.query.get_or_404(system_id)
        inspection = system.inspection
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to edit this system.', 'danger')
            return redirect(url_for('inspections'))
        
        form = InspectionSystemForm()
        if form.validate_on_submit():
            system.system_name = form.system_name.data
            system.system_type = form.system_type.data
            system.condition_rating = form.condition_rating.data
            system.last_maintenance = form.last_maintenance.data
            system.maintenance_notes = form.maintenance_notes.data
            system.next_maintenance = form.next_maintenance.data
            
            db.session.commit()
            flash(f'✓ System "{system.system_name}" updated successfully!', 'success')
            return redirect(url_for('view_inspection', inspection_id=inspection.id))
        
        elif request.method == 'GET':
            form.system_name.data = system.system_name
            form.system_type.data = system.system_type
            form.condition_rating.data = system.condition_rating
            form.last_maintenance.data = system.last_maintenance
            form.maintenance_notes.data = system.maintenance_notes
            form.next_maintenance.data = system.next_maintenance
        
        return render_template('system_form.html', form=form, system=system, inspection=inspection)
    
    
    @app.route('/system/<int:system_id>/delete', methods=['POST'])
    @login_required
    def delete_system(system_id):
        """Delete inspection system"""
        system = InspectionSystem.query.get_or_404(system_id)
        inspection = system.inspection
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to delete this system.', 'danger')
            return redirect(url_for('inspections'))
        
        try:
            db.session.delete(system)
            db.session.commit()
            flash('✓ System deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting system: {str(e)}', 'danger')
        
        return redirect(url_for('view_inspection', inspection_id=inspection.id))
    
    
    # ==================== ADMIN ROUTES ====================
    
    @app.route('/admin/requests')
    @login_required
    def admin_requests():
        """Admin page - view pending user approval requests"""
        # Check if user is admin (first user or has admin flag)
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user or current_user.id != admin_user.id:
            flash('You do not have permission to access the admin panel.', 'danger')
            return redirect(url_for('inspections'))
        
        pending_users = User.query.filter_by(active=0).all()
        return render_template('admin_requests.html', pending_users=pending_users)
    
    
    @app.route('/admin/approve/<int:user_id>', methods=['POST'])
    @login_required
    def approve_user(user_id):
        """Admin approves user registration"""
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user or current_user.id != admin_user.id:
            flash('You do not have permission to perform this action.', 'danger')
            return redirect(url_for('inspections'))
        
        user = User.query.get_or_404(user_id)
        try:
            user.active = 1
            db.session.commit()
            flash(f'✓ User {user.email} has been approved!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error approving user: {str(e)}', 'danger')
        
        return redirect(url_for('admin_requests'))
    
    
    @app.route('/admin/reject/<int:user_id>', methods=['POST'])
    @login_required
    def reject_user(user_id):
        """Admin rejects user registration"""
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user or current_user.id != admin_user.id:
            flash('You do not have permission to perform this action.', 'danger')
            return redirect(url_for('inspections'))
        
        user = User.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            flash(f'✓ User {user.email} has been rejected!', 'info')
        except Exception as e:
            db.session.rollback()
            flash(f'Error rejecting user: {str(e)}', 'danger')
        
        return redirect(url_for('admin_requests'))
    
    
    # ==================== API ENDPOINTS ====================
    
    @app.route('/api/inspections', methods=['GET'])
    @login_required
    def api_inspections():
        """API endpoint - get all inspections for current user"""
        try:
            inspections = ProjectInspection.query.filter_by(user_id=current_user.id).all()
            data = []
            for insp in inspections:
                data.append({
                    'id': insp.id,
                    'project_name': insp.project_name,
                    'city': insp.city,
                    'building_type': insp.building_type,
                    'created_at': str(insp.created_at),
                    'systems_count': len(insp.systems),
                })
            return jsonify({'status': 'success', 'count': len(data), 'data': data})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    @app.route('/api/systems', methods=['GET'])
    @login_required
    def api_systems():
        """API endpoint - get all systems for all inspections of current user"""
        try:
            inspections = ProjectInspection.query.filter_by(user_id=current_user.id).all()
            data = []
            for insp in inspections:
                for system in insp.systems:
                    data.append({
                        'id': system.id,
                        'inspection_id': insp.id,
                        'project_name': insp.project_name,
                        'system_name': system.system_name,
                        'system_type': system.system_type,
                        'condition_rating': system.condition_rating,
                        'created_at': str(system.created_at),
                    })
            return jsonify({'status': 'success', 'count': len(data), 'data': data})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    @app.route('/api/users', methods=['GET'])
    @login_required
    def api_users():
        """API endpoint - get list of active users (admin only)"""
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user or current_user.id != admin_user.id:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        
        try:
            users = User.query.filter_by(active=1).all()
            data = []
            for user in users:
                data.append({
                    'id': user.id,
                    'email': user.email,
                    'active': user.active,
                    'created_at': str(user.created_at),
                })
            return jsonify({'status': 'success', 'count': len(data), 'data': data})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    # ==================== ERROR HANDLERS ====================
    
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
