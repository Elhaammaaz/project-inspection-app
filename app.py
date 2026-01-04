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
            
            if user and user.check_password(form.password.data) and user.active:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Email or password is incorrect, or your account is pending approval.', 'danger')
        
        return render_template('login.html', form=form)
    
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration route - creates pending account"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                # Create new user (inactive by default)
                user = User(email=form.email.data, full_name=form.full_name.data)
                user.set_password(form.password.data)
                user.active = 0  # Pending approval
                
                db.session.add(user)
                db.session.commit()
                
                flash(
                    'Account request submitted! The admin (demo@example.com) will review and approve your account shortly.',
                    'success'
                )
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
    
    
    @app.route('/inspections', methods=['GET'])
    @login_required
    def inspections():
        """List all inspections for current user"""
        search_query = request.args.get('search', '', type=str)
        
        if search_query:
            inspections = ProjectInspection.query.filter_by(user_id=current_user.id)\
                .filter(
                    (ProjectInspection.project_name.ilike(f'%{search_query}%')) |
                    (ProjectInspection.city.ilike(f'%{search_query}%'))
                )\
                .order_by(ProjectInspection.created_at.desc())\
                .all()
        else:
            inspections = ProjectInspection.query.filter_by(user_id=current_user.id)\
                .order_by(ProjectInspection.created_at.desc())\
                .all()
        
        return render_template('inspections.html', inspections=inspections)
    
    
    @app.route('/inspection/new', methods=['GET', 'POST'])
    @login_required
    def create_inspection():
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
                notes=form.notes.data,
                inspection_status=form.inspection_status.data,
                inspection_by=form.inspection_by.data,
                reviewed_by=form.reviewed_by.data
            )
            db.session.add(inspection)
            db.session.commit()
            
            flash(f'✓ Inspection "{inspection.project_name}" created successfully!', 'success')
            return redirect(url_for('view_inspection', inspection_id=inspection.id))
        
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
        """Delete project inspection and all its systems"""
        inspection = ProjectInspection.query.get_or_404(inspection_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to delete this inspection.', 'danger')
            return redirect(url_for('inspections'))
        
        project_name = inspection.project_name
        db.session.delete(inspection)
        db.session.commit()
        flash(f'✓ Inspection "{project_name}" and all its systems deleted successfully!', 'success')
        return redirect(url_for('inspections'))
    
    
    # ==================== SYSTEM ROUTES ====================
    
    @app.route('/inspection/<int:inspection_id>/system/add', methods=['GET', 'POST'])
    @login_required
    def add_system(inspection_id):
        """Add a building system to an inspection"""
        inspection = ProjectInspection.query.get_or_404(inspection_id)
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to modify this inspection.', 'danger')
            return redirect(url_for('inspections'))
        
        form = InspectionSystemForm()
        if form.validate_on_submit():
            # Check if system with same name already exists for this inspection
            existing = InspectionSystem.query.filter_by(
                project_inspection_id=inspection_id,
                system_name=form.system_name.data
            ).first()
            
            if existing:
                flash(f'System "{form.system_name.data}" already exists for this inspection.', 'warning')
            else:
                system = InspectionSystem(
                    project_inspection_id=inspection_id,
                    system_name=form.system_name.data,
                    item_count=form.item_count.data,
                    score_percentage=form.score_percentage.data,
                    weight=form.weight.data,
                    weighted_score=form.weighted_score.data,
                    status=form.status.data if form.status.data else None
                )
                db.session.add(system)
                db.session.commit()
                flash(f'✓ System "{system.system_name}" added successfully!', 'success')
                return redirect(url_for('view_inspection', inspection_id=inspection_id))
        
        return render_template('system_form.html', form=form, inspection=inspection)
    
    
    @app.route('/system/<int:system_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_system(system_id):
        """Edit a building system"""
        system = InspectionSystem.query.get_or_404(system_id)
        inspection = system.inspection
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to modify this system.', 'danger')
            return redirect(url_for('inspections'))
        
        form = InspectionSystemForm()
        if form.validate_on_submit():
            system.system_name = form.system_name.data
            system.item_count = form.item_count.data
            system.score_percentage = form.score_percentage.data
            system.weight = form.weight.data
            system.weighted_score = form.weighted_score.data
            system.status = form.status.data if form.status.data else None
            system.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash(f'✓ System "{system.system_name}" updated successfully!', 'success')
            return redirect(url_for('view_inspection', inspection_id=inspection.id))
        
        elif request.method == 'GET':
            form.system_name.data = system.system_name
            form.item_count.data = system.item_count
            form.score_percentage.data = system.score_percentage
            form.weight.data = system.weight
            form.weighted_score.data = system.weighted_score
            form.status.data = system.status
        
        return render_template('system_form.html', form=form, inspection=inspection, system=system)
    
    
    @app.route('/system/<int:system_id>/delete', methods=['POST'])
    @login_required
    def delete_system(system_id):
        """Delete a building system"""
        system = InspectionSystem.query.get_or_404(system_id)
        inspection = system.inspection
        
        if inspection.user_id != current_user.id:
            flash('You do not have permission to delete this system.', 'danger')
            return redirect(url_for('inspections'))
        
        system_name = system.system_name
        db.session.delete(system)
        db.session.commit()
        flash(f'✓ System "{system_name}" deleted successfully!', 'success')
        return redirect(url_for('view_inspection', inspection_id=inspection.id))
    
    
    # ==================== ADMIN ROUTES (FOR ACCOUNT APPROVAL) ====================
    
    @app.route('/admin/requests')
    @login_required
    def admin_requests():
        """Admin panel to view and approve pending accounts"""
        # Only demo user can approve
        if current_user.email != 'demo@example.com':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('dashboard'))
        
        # Get pending users
        pending_users = User.query.filter_by(active=0).all()
        approved_users = User.query.filter_by(active=1).all()
        
        return render_template('admin_requests.html', 
                             pending_users=pending_users,
                             approved_users=approved_users)
    
    
    @app.route('/admin/approve/<int:user_id>', methods=['POST'])
    @login_required
    def approve_user(user_id):
        """Approve a pending user account"""
        # Only demo user can approve
        if current_user.email != 'demo@example.com':
            flash('You do not have permission to perform this action.', 'danger')
            return redirect(url_for('dashboard'))
        
        user = User.query.get_or_404(user_id)
        
        if user.active == 1:
            flash(f'User {user.email} is already approved.', 'info')
        else:
            try:
                user.active = 1
                user.approved_at = datetime.utcnow()
                user.approved_by_id = current_user.id
                db.session.commit()
                flash(f'User {user.email} has been approved! They can now log in.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error approving user: {str(e)}', 'danger')
        
        return redirect(url_for('admin_requests'))
    
    
    @app.route('/admin/reject/<int:user_id>', methods=['POST'])
    @login_required
    def reject_user(user_id):
        """Reject and delete a pending user account"""
        # Only demo user can reject
        if current_user.email != 'demo@example.com':
            flash('You do not have permission to perform this action.', 'danger')
            return redirect(url_for('dashboard'))
        
        user = User.query.get_or_404(user_id)
        
        if user.active == 1:
            flash(f'Cannot reject an already approved user.', 'warning')
        else:
            try:
                email = user.email
                db.session.delete(user)
                db.session.commit()
                flash(f'User {email} has been rejected and removed.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error rejecting user: {str(e)}', 'danger')
        
        return redirect(url_for('admin_requests'))
    
    
    # ==================== API ENDPOINTS (FOR POWER BI) ====================
    
    @app.route('/api/inspections', methods=['GET'])
    def api_inspections():
        """API endpoint for Power BI - Get all project inspections with systems"""
        try:
            inspections = ProjectInspection.query.all()
            data = []
            
            for inspection in inspections:
                # Build systems array for this inspection
                systems_data = []
                for system in inspection.systems:
                    systems_data.append({
                        'id': system.id,
                        'system_name': system.system_name,
                        'item_count': system.item_count,
                        'score_percentage': system.score_percentage,
                        'weight': system.weight,
                        'weighted_score': system.weighted_score,
                        'status': system.status,
                        'created_at': str(system.created_at),
                        'updated_at': str(system.updated_at)
                    })
                
                # Calculate total weighted score
                total_weighted_score = sum([s.get('weighted_score', 0) for s in systems_data])
                
                inspection_data = {
                    'id': inspection.id,
                    'user_id': inspection.user_id,
                    'project_name': inspection.project_name,
                    'city': inspection.city,
                    'address': inspection.address,
                    'gps_latitude': inspection.gps_latitude,
                    'gps_longitude': inspection.gps_longitude,
                    'building_type': inspection.building_type,
                    'primary_use': inspection.primary_use,
                    'gross_built_area': inspection.gross_built_area,
                    'number_of_floors': inspection.number_of_floors,
                    'last_renovation_date': str(inspection.last_renovation_date) if inspection.last_renovation_date else None,
                    'construction_year': inspection.construction_year,
                    'current_year': inspection.current_year,
                    'estimated_life_time': inspection.estimated_life_time,
                    'planned_retirement_year': inspection.planned_retirement_year,
                    'inspection_date': str(inspection.inspection_date) if inspection.inspection_date else None,
                    'fm_contractor': inspection.fm_contractor,
                    'system_threshold': inspection.system_threshold,
                    'inspection_result': inspection.inspection_result,
                    'building_score': inspection.building_score,
                    'high_priority_classified': inspection.high_priority_classified,
                    'fm_performance': inspection.fm_performance,
                    'government_compliance': inspection.government_compliance,
                    'fire_life_safety': inspection.fire_life_safety,
                    'total_economic_life': inspection.total_economic_life,
                    'chronological_age': inspection.chronological_age,
                    'estimated_effective_age': inspection.estimated_effective_age,
                    'estimated_remaining_life': inspection.estimated_remaining_life,
                    'notes': inspection.notes,
                    'inspection_status': inspection.inspection_status,
                    'inspection_by': inspection.inspection_by,
                    'reviewed_by': inspection.reviewed_by,
                    'systems_count': len(systems_data),
                    'total_weighted_score': round(total_weighted_score, 2),
                    'systems': systems_data,
                    'created_at': str(inspection.created_at),
                    'updated_at': str(inspection.updated_at),
                }
                data.append(inspection_data)
            
            return jsonify({'status': 'success', 'count': len(data), 'data': data})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    @app.route('/api/systems', methods=['GET'])
    def api_systems():
        """API endpoint for Power BI - Get all building systems across all inspections"""
        try:
            systems = InspectionSystem.query.all()
            data = []
            
            for system in systems:
                data.append({
                    'id': system.id,
                    'project_inspection_id': system.project_inspection_id,
                    'inspection_project_name': system.inspection.project_name,
                    'inspection_city': system.inspection.city,
                    'system_name': system.system_name,
                    'item_count': system.item_count,
                    'score_percentage': system.score_percentage,
                    'weight': system.weight,
                    'weighted_score': system.weighted_score,
                    'status': system.status,
                    'created_at': str(system.created_at),
                    'updated_at': str(system.updated_at)
                })
            
            return jsonify({'status': 'success', 'count': len(data), 'data': data})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    @app.route('/api/users', methods=['GET'])
    def api_users():
        """API endpoint for Power BI - Get all users"""
        try:
            users = User.query.all()
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
