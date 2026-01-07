"""
BCAR Flask Application - 7-Step Guided Workflow
Enterprise production-ready with blueprints, role-based access, and audit logging
"""

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config as config_dict
import os
from datetime import datetime, date

from models import (
    db, User, Building, Assessment, AssessmentItem, SystemScore,
    ComplianceChecklist, ComplianceItem, TestRegister, CAPARegister,
    System, Subsystem, Component, Rate, Weight, Responsibility, Priority,
    ComplianceArea, AuditLog, ExecutiveDashboardSummary
)
from calculations import CalculationService


def _seed_lookup_tables():
    """Populate lookup tables on first run"""
    # Rates
    if Rate.query.first() is None:
        for i, desc in enumerate(['Poor', 'Below Average', 'Average', 'Good', 'Excellent'], 1):
            db.session.add(Rate(rate_value=i, description=desc, active=True))
    
    # Weights
    if Weight.query.first() is None:
        for w in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
            db.session.add(Weight(weight_value=w, description=f'Weight {w}', active=True))
    
    # Priorities
    if Priority.query.first() is None:
        for i, name in enumerate(['P1', 'P2', 'P3', 'P4'], 1):
            db.session.add(Priority(priority_name=name, order=i, active=True))
    
    # Responsibilities
    if Responsibility.query.first() is None:
        for name in ['MEP', 'Main Contractor', 'FM', 'Specialist', 'Client']:
            db.session.add(Responsibility(name=name, active=True))
    
    # Compliance Areas
    if ComplianceArea.query.first() is None:
        areas = [
            ('Fire Safety', 'Fire suppression and safety', 'FS-001'),
            ('Electrical Safety', 'Electrical systems compliance', 'ES-001'),
            ('HVAC Efficiency', 'Climate control systems', 'HV-001'),
            ('Water Systems', 'Plumbing and water treatment', 'WS-001'),
            ('Building Envelope', 'Structural and thermal integrity', 'BE-001'),
        ]
        for area, desc, code in areas:
            db.session.add(ComplianceArea(area_name=area, description=desc, regulation_code=code, active=True))
    
    # Systems (21 building systems)
    if System.query.first() is None:
        systems = [
            ('Fire_LifeSafety', 'Fire Life Safety'),
            ('Electrical', 'Electrical Systems'),
            ('HVAC', 'HVAC Systems'),
            ('Plumbing', 'Plumbing Systems'),
            ('Structural', 'Structural Systems'),
            ('Roofing', 'Roofing Systems'),
            ('Cladding', 'Facade & Cladding'),
            ('Doors_Windows', 'Doors & Windows'),
            ('Interior_Finishes', 'Interior Finishes'),
            ('Accessibility', 'Accessibility Features'),
            ('Security', 'Security Systems'),
            ('Vertical_Transport', 'Vertical Transport (Lifts)'),
            ('Controls', 'Building Management Controls'),
            ('Maintenance', 'Maintenance & Operations'),
            ('Landscaping', 'Landscaping & Grounds'),
            ('Parking', 'Parking Facilities'),
            ('Signage', 'Signage Systems'),
            ('IT_Telecom', 'IT & Telecommunications'),
            ('Wastewater', 'Wastewater Systems'),
            ('Waste_Management', 'Waste Management'),
            ('Energy_Efficiency', 'Energy & Efficiency'),
        ]
        for i, (code, name) in enumerate(systems, 1):
            db.session.add(System(system_code=code, system_name=name, order=i, active=True))
    
    db.session.commit()


def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    config_obj = config_dict.get(config_name, config_dict['development'])
    app.config.from_object(config_obj)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # ==================== DATABASE INITIALIZATION ====================
    
    with app.app_context():
        db.create_all()
        
        # Create demo user if not exists
        demo = User.query.filter_by(username='demo').first()
        if not demo:
            demo = User(
                username='demo',
                email='demo@example.com',
                role='Admin'
            )
            demo.set_password('demo123')
            db.session.add(demo)
            db.session.commit()
            print('✓ Demo user created: demo / demo123')
        
        # Seed lookup tables if empty
        _seed_lookup_tables()
    
    # ==================== CONTEXT PROCESSOR ====================
    
    @app.context_processor
    def inject_pending_requests():
        """Inject pending user count for admin notification bell"""
        pending_count = 0
        if current_user.is_authenticated and current_user.is_admin:
            pending_count = User.query.filter_by(is_active=False).count()
        return dict(pending_requests_count=pending_count)
    
    # ==================== CACHE CONTROL (Prevent back button after logout) ====================
    
    @app.after_request
    def add_cache_control_headers(response):
        """Prevent browser from caching authenticated pages"""
        if current_user.is_authenticated:
            # Prevent caching of authenticated pages
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response
    
    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403
    
    # ==================== AUTHENTICATION ====================
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        from forms import RegisterForm
        form = RegisterForm()
        
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                role='Viewer',
                is_active=False  # Pending admin approval
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            flash('Account request submitted! Please wait for admin approval.', 'info')
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        from forms import LoginForm
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                if not user.is_active:
                    flash('Your account is pending admin approval. Please wait.', 'warning')
                    return render_template('login.html', form=form)
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))
    
    # ==================== PROFILE ====================
    
    @app.route('/profile')
    @login_required
    def profile():
        """View user profile"""
        return render_template('profile.html', user=current_user)
    
    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        """Edit user profile"""
        from forms import LoginForm  # Reuse for simplicity
        if request.method == 'POST':
            new_email = request.form.get('email')
            if new_email and new_email != current_user.email:
                current_user.email = new_email
                db.session.commit()
                flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        return render_template('edit_profile.html', user=current_user)
    
    # ==================== ADMIN ====================
    
    @app.route('/admin')
    @login_required
    def admin_dashboard():
        """Admin dashboard"""
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        
        # Get all users for admin overview
        all_users = User.query.all()
        pending_users = User.query.filter_by(is_active=False).all()
        return render_template('admin_dashboard.html', 
                             all_users=all_users, 
                             pending_users=pending_users)
    
    @app.route('/admin/requests')
    @login_required
    def admin_requests():
        """Admin - view pending account requests"""
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        
        pending_users = User.query.filter_by(is_active=False).all()
        approved_users = User.query.filter_by(is_active=True).all()
        return render_template('admin_requests.html', 
                             pending_users=pending_users,
                             approved_users=approved_users)
    
    @app.route('/admin/approve/<int:user_id>', methods=['POST'])
    @login_required
    def approve_user(user_id):
        """Approve a pending user"""
        if not current_user.is_admin:
            flash('Access denied.', 'danger')
            return redirect(url_for('dashboard'))
        
        user = User.query.get_or_404(user_id)
        user.is_active = True
        db.session.commit()
        flash(f'User {user.email} has been approved!', 'success')
        return redirect(url_for('admin_requests'))
    
    @app.route('/admin/reject/<int:user_id>', methods=['POST'])
    @login_required
    def reject_user(user_id):
        """Reject/delete a pending user"""
        if not current_user.is_admin:
            flash('Access denied.', 'danger')
            return redirect(url_for('dashboard'))
        
        user = User.query.get_or_404(user_id)
        email = user.email
        db.session.delete(user)
        db.session.commit()
        flash(f'User {email} has been rejected and removed.', 'warning')
        return redirect(url_for('admin_requests'))
    
    # ==================== LANDING PAGE & DASHBOARD ====================
    
    @app.route('/')
    def index():
        """Landing page - redirect to dashboard if logged in"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('landing.html')
    
    @app.route('/landing')
    def landing():
        """Landing page"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('landing.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard - list all buildings"""
        page = request.args.get('page', 1, type=int)
        buildings = Building.query.filter_by(created_by_id=current_user.id).paginate(page=page, per_page=10)
        return render_template('dashboard.html', buildings=buildings)
    
    # ==================== STEP 1: BUILDING INFORMATION ====================
    
    @app.route('/building/new', methods=['GET', 'POST'])
    @login_required
    def building_new():
        """Create new building (Step 1)"""
        from forms import BuildingHeaderForm
        from datetime import date
        
        form = BuildingHeaderForm()
        
        if form.validate_on_submit():
            # Generate unique building code
            code = f"BLD-{current_user.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            building = Building(
                building_code=code,
                project_name=form.project_name.data,
                city=form.city.data,
                address=form.address.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                building_type=form.building_type.data,
                primary_use=form.primary_use.data,
                gross_built_area_m2=form.gross_built_area_m2.data,
                number_of_floors=form.number_of_floors.data,
                construction_year=form.construction_year.data,
                last_major_renovation_date=form.last_major_renovation_date.data,
                estimated_life_time_years=form.estimated_life_time_years.data,
                planned_asset_retirement_year=form.planned_asset_retirement_year.data,
                fm_contractor=form.fm_contractor.data,
                inspection_date=form.inspection_date.data,
                current_year=form.current_year.data,
                system_threshold_percent=form.system_threshold_percent.data,
                created_by_id=current_user.id,
                status='Draft'
            )
            db.session.add(building)
            db.session.commit()
            
            # Create initial assessment record
            assessment = Assessment(
                building_id=building.id,
                assessment_code=f"ASS-{building.id}-001",
                status='Open'
            )
            db.session.add(assessment)
            db.session.commit()
            
            _log_audit('buildings', building.id, 'CREATE', None, building.as_dict())
            
            flash('Building created! Now add assessment items.', 'success')
            return redirect(url_for('building_view', building_id=building.id))
        
        return render_template('building_header.html', form=form)
    
    @app.route('/building/<int:building_id>')
    @login_required
    def building_view(building_id):
        """View building and manage workflow"""
        building = Building.query.get_or_404(building_id)
        
        # Role-based access check
        if building.created_by_id != current_user.id and current_user.role != 'Admin':
            flash('Access denied', 'danger')
            return redirect(url_for('dashboard'))
        
        # Get workflow progress
        assessment = Assessment.query.filter_by(building_id=building_id).first()
        compliance = ComplianceChecklist.query.filter_by(building_id=building_id).first()
        system_scores = SystemScore.query.filter_by(building_id=building_id).all()
        tests = TestRegister.query.filter_by(building_id=building_id).count()
        capas = CAPARegister.query.filter_by(building_id=building_id).count()
        dashboard = ExecutiveDashboardSummary.query.filter_by(building_id=building_id).first()
        
        return render_template('building_view.html', 
            building=building, 
            assessment=assessment,
            compliance=compliance,
            system_scores=system_scores,
            tests=tests,
            capas=capas,
            dashboard=dashboard
        )
    
    # ==================== STEP 2: ASSESSMENT ITEMS ====================
    
    @app.route('/building/<int:building_id>/assessment/items')
    @login_required
    def assessment_items_list(building_id):
        """List all assessment items for building"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        page = request.args.get('page', 1, type=int)
        items = AssessmentItem.query.join(Assessment).filter(
            Assessment.building_id == building_id
        ).paginate(page=page, per_page=20)
        
        return render_template('assessment_items_list.html', building=building, items=items)
    
    @app.route('/building/<int:building_id>/assessment/item/new', methods=['GET', 'POST'])
    @login_required
    def assessment_item_new(building_id):
        """Add new assessment item"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        from forms import AssessmentItemForm
        form = AssessmentItemForm()
        
        # Populate dropdowns
        form.system.choices = [(0, '-- Select System --')] + [(s.id, s.system_name) for s in System.query.filter_by(active=True).all()]
        
        # Get subsystems and components for the selected system (for form resubmission)
        selected_system = request.form.get('system', type=int) or 0
        selected_subsystem = request.form.get('subsystem', type=int) or 0
        
        if selected_system > 0:
            form.subsystem.choices = [(0, '-- Select Subsystem --')] + [(s.id, s.subsystem_name) for s in Subsystem.query.filter_by(system_id=selected_system, active=True).all()]
        else:
            form.subsystem.choices = [(0, '-- Select System First --')]
        
        if selected_subsystem > 0:
            form.component.choices = [(0, '-- Select Component --')] + [(c.id, c.component_name) for c in Component.query.filter_by(subsystem_id=selected_subsystem, active=True).all()]
        else:
            form.component.choices = [(0, '-- Select Subsystem First --')]
        
        form.rate.choices = [(r.rate_value, f"{r.rate_value} - {r.description}") 
                             for r in Rate.query.filter_by(active=True).order_by(Rate.rate_value).all()]
        form.item_weight.choices = [(w.weight_value, str(w.weight_value)) 
                                     for w in Weight.query.filter_by(active=True).all()]
        form.responsibility.choices = [(0, '-- Select --')] + [(r.id, r.name) 
                                        for r in Responsibility.query.filter_by(active=True).all()]
        
        if request.method == 'POST':
            # Debug: print form errors if any
            if not form.validate():
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f'{field}: {error}', 'danger')
                return render_template('assessment_item_form.html', form=form, building=building)
            
            assessment = Assessment.query.filter_by(building_id=building_id).first()
            if not assessment:
                # Auto-create assessment if not exists
                assessment = Assessment(
                    building_id=building_id,
                    assessment_code=f"ASM-{building_id}-001",
                    status='Open'
                )
                db.session.add(assessment)
                db.session.commit()
            
            # Generate item code if not provided
            item_code = form.item_code.data
            if not item_code:
                count = AssessmentItem.query.filter_by(assessment_id=assessment.id).count()
                item_code = f"AI-{count + 1:03d}"
            
            item = AssessmentItem(
                assessment_id=assessment.id,
                system_id=form.system.data if form.system.data > 0 else None,
                subsystem_id=form.subsystem.data if form.subsystem.data and form.subsystem.data > 0 else None,
                component_id=form.component.data if form.component.data and form.component.data > 0 else None,
                item_code=item_code,
                inspection_item=form.inspection_item.data or '',
                criteria=form.criteria.data or '',
                test_method=form.test_method.data or '',
                asset_tag_no=form.asset_tag_no.data,
                snag_location=form.snag_location.data,
                snag_evidence_ref=form.snag_evidence_ref.data,
                snag_evidence_type=form.snag_evidence_type.data,
                rate=form.rate.data,
                item_weight=form.item_weight.data,
                risk_criticality=form.risk_criticality.data,
                responsibility_id=form.responsibility.data if form.responsibility.data and form.responsibility.data > 0 else None,
                priority=form.priority.data,
                status=form.status.data,
                due_date=form.due_date.data,
                remarks=form.remarks.data
            )
            
            # Calculate scores server-side
            CalculationService.calculate_assessment_item_scores(item)
            
            db.session.add(item)
            db.session.commit()
            
            # Recalculate system metrics
            if item.system_id:
                CalculationService.calculate_system_metrics(building_id, item.system_id)
            CalculationService.compute_executive_dashboard(building_id)
            db.session.commit()
            
            _log_audit('assessment_items', item.id, 'CREATE', None, item.as_dict())
            
            flash('Assessment item added!', 'success')
            return redirect(url_for('assessment_items_list', building_id=building_id))
        
        return render_template('assessment_item_form.html', form=form, building=building)
    
    # ==================== STEP 3: COMPLIANCE CHECKLIST ====================
    
    @app.route('/building/<int:building_id>/compliance')
    @login_required
    def compliance_checklist(building_id):
        """Step 3: Compliance checklist"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        compliance = ComplianceChecklist.query.filter_by(building_id=building_id).first()
        compliance_items = []
        if compliance:
            compliance_items = ComplianceItem.query.filter_by(checklist_id=compliance.id).all()
        
        areas = ComplianceArea.query.filter_by(active=True).all()
        
        # Calculate area status based on items - determine overall status per area
        area_status = {}
        for area in areas:
            area_items = [item for item in compliance_items if item.compliance_area_id == area.id]
            if area_items:
                # Determine overall status: if any "No" -> No, if all "Yes" -> Yes, otherwise Partial
                statuses = [item.status for item in area_items if item.status]
                if 'No' in statuses:
                    area_status[area.id] = 'No'
                elif all(s == 'Yes' for s in statuses):
                    area_status[area.id] = 'Yes'
                elif statuses:
                    area_status[area.id] = 'Partial'
        
        return render_template('compliance_checklist.html', 
            building=building, 
            compliance=compliance,
            compliance_items=compliance_items,
            areas=areas,
            area_status=area_status
        )
    
    @app.route('/building/<int:building_id>/compliance/status', methods=['POST'])
    @login_required
    def compliance_status_update(building_id):
        """Update compliance area statuses (bulk update)"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        # Get or create checklist
        checklist = ComplianceChecklist.query.filter_by(building_id=building_id).first()
        if not checklist:
            checklist = ComplianceChecklist(
                building_id=building_id,
                checklist_code=f"CCL-{building_id}-001",
                status='Open'
            )
            db.session.add(checklist)
            db.session.commit()
        
        areas = ComplianceArea.query.filter_by(active=True).all()
        
        # Process each area status from form
        for area in areas:
            status = request.form.get(f'area_status_{area.id}')
            if status:
                # Find existing item for this area or create new one
                existing_item = ComplianceItem.query.filter_by(
                    checklist_id=checklist.id,
                    compliance_area_id=area.id
                ).first()
                
                if existing_item:
                    existing_item.status = status
                    existing_item.updated_at = db.func.now()
                else:
                    # Create a default compliance item for this area
                    count = ComplianceItem.query.filter_by(checklist_id=checklist.id).count()
                    item_code = f"GC-{count + 1:03d}"
                    item = ComplianceItem(
                        checklist_id=checklist.id,
                        compliance_area_id=area.id,
                        item_code=item_code,
                        requirement=f"{area.area_name} - Overall Status",
                        status=status
                    )
                    db.session.add(item)
        
        db.session.commit()
        flash('Compliance status saved successfully!', 'success')
        return redirect(url_for('compliance_checklist', building_id=building_id))
    
    @app.route('/building/<int:building_id>/compliance/item/<int:item_id>/edit', methods=['GET', 'POST'])
    @login_required
    def compliance_item_edit(building_id, item_id):
        """Edit existing compliance item"""
        import os
        from werkzeug.utils import secure_filename
        
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        item = ComplianceItem.query.get_or_404(item_id)
        areas = ComplianceArea.query.filter_by(active=True).all()
        
        from forms import ComplianceItemForm
        form = ComplianceItemForm()
        
        if request.method == 'POST':
            item.compliance_area_id = int(request.form.get('compliance_area_id')) if request.form.get('compliance_area_id') else item.compliance_area_id
            item.requirement = request.form.get('requirement', item.requirement)
            item.status = request.form.get('status', item.status)
            item.evidence_ref = request.form.get('evidence_ref')
            item.remarks = request.form.get('remarks')
            
            # Handle file upload
            if 'evidence_file' in request.files:
                file = request.files['evidence_file']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'compliance', str(building_id))
                    os.makedirs(upload_dir, exist_ok=True)
                    import time
                    timestamped_filename = f"{int(time.time())}_{filename}"
                    file_path = os.path.join(upload_dir, timestamped_filename)
                    file.save(file_path)
                    item.evidence_file_path = f"uploads/compliance/{building_id}/{timestamped_filename}"
            
            db.session.commit()
            flash('Compliance item updated!', 'success')
            return redirect(url_for('compliance_checklist', building_id=building_id))
        
        return render_template('compliance_item_edit.html', form=form, building=building, item=item, areas=areas)
    
    @app.route('/building/<int:building_id>/compliance/item/<int:item_id>/delete')
    @login_required
    def compliance_item_delete(building_id, item_id):
        """Delete compliance item"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        item = ComplianceItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        
        flash('Compliance item deleted!', 'success')
        return redirect(url_for('compliance_checklist', building_id=building_id))
    
    @app.route('/compliance/document/<int:item_id>')
    @login_required
    def download_compliance_doc(item_id):
        """Download compliance document"""
        from flask import send_from_directory
        import os
        
        item = ComplianceItem.query.get_or_404(item_id)
        
        if not item.evidence_file_path:
            flash('No document attached to this item.', 'warning')
            return redirect(request.referrer or url_for('dashboard'))
        
        # Extract directory and filename from path
        file_path = os.path.join(app.root_path, 'static', item.evidence_file_path)
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        if os.path.exists(file_path):
            return send_from_directory(directory, filename, as_attachment=True)
        else:
            flash('Document file not found.', 'error')
            return redirect(request.referrer or url_for('dashboard'))
    
    # ==================== STEP 4: SYSTEM SCORING ====================
    
    @app.route('/building/<int:building_id>/system-scoring')
    @login_required
    def system_scoring(building_id):
        """Step 4: System scoring overview"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        system_scores = SystemScore.query.filter_by(building_id=building_id).all()
        systems = System.query.filter_by(active=True).all()
        
        return render_template('system_scoring.html', 
            building=building, 
            system_scores=system_scores,
            systems=systems
        )
    
    # ==================== STEP 5: TEST REGISTER ====================
    
    @app.route('/building/<int:building_id>/tests')
    @login_required
    def test_register(building_id):
        """Step 5: Test register"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        page = request.args.get('page', 1, type=int)
        tests = TestRegister.query.filter_by(building_id=building_id).paginate(page=page, per_page=20)
        
        return render_template('test_register.html', 
            building=building, 
            tests=tests
        )
    
    # ==================== STEP 6: CAPA REGISTER ====================
    
    @app.route('/building/<int:building_id>/capa')
    @login_required
    def capa_register(building_id):
        """Step 6: CAPA register"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        page = request.args.get('page', 1, type=int)
        capas = CAPARegister.query.filter_by(building_id=building_id).paginate(page=page, per_page=20)
        
        return render_template('capa_register.html', 
            building=building, 
            capas=capas
        )
    
    # ==================== STEP 7: EXECUTIVE DASHBOARD ====================
    
    @app.route('/building/<int:building_id>/dashboard')
    @login_required
    def executive_dashboard(building_id):
        """Step 7: Executive dashboard view"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        # Get dashboard summary (computed)
        dashboard = ExecutiveDashboardSummary.query.filter_by(building_id=building_id).first()
        if not dashboard:
            dashboard = CalculationService.compute_executive_dashboard(building_id)
            db.session.commit()
        
        # Get system scores
        system_scores = SystemScore.query.filter_by(building_id=building_id).all()
        
        return render_template('executive_dashboard.html', 
            building=building, 
            dashboard=dashboard,
            system_scores=system_scores
        )
    
    # ==================== API ENDPOINTS ====================
    
    @app.route('/api/subsystems/<int:system_id>')
    @login_required
    def api_get_subsystems(system_id):
        """Get subsystems for cascading dropdown"""
        subsystems = Subsystem.query.filter_by(system_id=system_id, active=True).order_by(Subsystem.order).all()
        return jsonify([{'id': s.id, 'name': s.subsystem_name} for s in subsystems])
    
    @app.route('/api/components/<int:subsystem_id>')
    @login_required
    def api_get_components(subsystem_id):
        """Get components for cascading dropdown"""
        components = Component.query.filter_by(subsystem_id=subsystem_id, active=True).order_by(Component.order).all()
        return jsonify([{'id': c.id, 'name': c.component_name} for c in components])
    
    @app.route('/api/systems')
    @login_required
    def api_get_systems():
        """Get all active systems"""
        systems = System.query.filter_by(active=True).order_by(System.order).all()
        return jsonify([{'id': s.id, 'code': s.system_code, 'name': s.system_name} for s in systems])
    
    # ==================== POWER BI API ENDPOINTS ====================
    
    @app.route('/api/powerbi/users')
    def api_powerbi_users():
        """Power BI: Get all users"""
        users = User.query.all()
        return jsonify({'data': [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role,
            'is_active': u.is_active,
            'created_at': u.created_at.isoformat() if u.created_at else None,
            'updated_at': u.updated_at.isoformat() if u.updated_at else None
        } for u in users]})
    
    @app.route('/api/powerbi/systems')
    def api_powerbi_systems():
        """Power BI: Get all systems"""
        systems = System.query.all()
        return jsonify({'data': [{
            'id': s.id,
            'system_code': s.system_code,
            'system_name': s.system_name,
            'description': s.description,
            'order': s.order,
            'active': s.active,
            'created_at': s.created_at.isoformat() if s.created_at else None
        } for s in systems]})
    
    @app.route('/api/powerbi/subsystems')
    def api_powerbi_subsystems():
        """Power BI: Get all subsystems"""
        subsystems = Subsystem.query.all()
        return jsonify({'data': [{
            'id': s.id,
            'system_id': s.system_id,
            'subsystem_code': s.subsystem_code,
            'subsystem_name': s.subsystem_name,
            'description': s.description,
            'order': s.order,
            'active': s.active
        } for s in subsystems]})
    
    @app.route('/api/powerbi/components')
    def api_powerbi_components():
        """Power BI: Get all components"""
        components = Component.query.all()
        return jsonify({'data': [{
            'id': c.id,
            'subsystem_id': c.subsystem_id,
            'component_code': c.component_code,
            'component_name': c.component_name,
            'description': c.description,
            'order': c.order,
            'active': c.active
        } for c in components]})
    
    @app.route('/api/powerbi/buildings')
    def api_powerbi_buildings():
        """Power BI: Get all buildings"""
        buildings = Building.query.all()
        return jsonify({'data': [{
            'id': b.id,
            'project_name': b.project_name,
            'building_code': b.building_code,
            'city': b.city,
            'address': b.address,
            'latitude': b.latitude,
            'longitude': b.longitude,
            'building_type': b.building_type,
            'primary_use': b.primary_use,
            'gross_built_area_m2': b.gross_built_area_m2,
            'number_of_floors': b.number_of_floors,
            'construction_year': b.construction_year,
            'last_major_renovation_date': b.last_major_renovation_date.isoformat() if b.last_major_renovation_date else None,
            'estimated_life_time_years': b.estimated_life_time_years,
            'planned_asset_retirement_year': b.planned_asset_retirement_year,
            'fm_contractor': b.fm_contractor,
            'inspection_date': b.inspection_date.isoformat() if b.inspection_date else None,
            'current_year': b.current_year,
            'system_threshold_percent': b.system_threshold_percent,
            'created_by_id': b.created_by_id,
            'status': b.status,
            'created_at': b.created_at.isoformat() if b.created_at else None,
            'updated_at': b.updated_at.isoformat() if b.updated_at else None
        } for b in buildings]})
    
    @app.route('/api/powerbi/assessments')
    def api_powerbi_assessments():
        """Power BI: Get all assessments"""
        assessments = Assessment.query.all()
        return jsonify({'data': [{
            'id': a.id,
            'building_id': a.building_id,
            'assessment_code': a.assessment_code,
            'status': a.status,
            'notes': a.notes,
            'created_at': a.created_at.isoformat() if a.created_at else None,
            'updated_at': a.updated_at.isoformat() if a.updated_at else None
        } for a in assessments]})
    
    @app.route('/api/powerbi/assessment_items')
    def api_powerbi_assessment_items():
        """Power BI: Get all assessment items"""
        items = AssessmentItem.query.all()
        return jsonify({'data': [{
            'id': i.id,
            'assessment_id': i.assessment_id,
            'system_id': i.system_id,
            'subsystem_id': i.subsystem_id,
            'component_id': i.component_id,
            'item_code': i.item_code,
            'inspection_item': i.inspection_item,
            'criteria': i.criteria,
            'test_method': i.test_method,
            'asset_tag_no': i.asset_tag_no,
            'snag_location': i.snag_location,
            'snag_evidence_ref': i.snag_evidence_ref,
            'snag_evidence_type': i.snag_evidence_type,
            'rate': i.rate,
            'item_weight': i.item_weight,
            'risk_criticality': i.risk_criticality,
            'responsibility_id': i.responsibility_id,
            'priority': i.priority,
            'status': i.status,
            'due_date': i.due_date.isoformat() if i.due_date else None,
            'remarks': i.remarks,
            'score': i.score,
            'score_percent': i.score_percent,
            'weighted_score': i.weighted_score,
            'created_at': i.created_at.isoformat() if i.created_at else None,
            'updated_at': i.updated_at.isoformat() if i.updated_at else None
        } for i in items]})
    
    @app.route('/api/powerbi/compliance_checklists')
    def api_powerbi_compliance_checklists():
        """Power BI: Get all compliance checklists"""
        checklists = ComplianceChecklist.query.all()
        return jsonify({'data': [{
            'id': c.id,
            'building_id': c.building_id,
            'checklist_code': c.checklist_code,
            'status': c.status,
            'created_at': c.created_at.isoformat() if c.created_at else None,
            'updated_at': c.updated_at.isoformat() if c.updated_at else None
        } for c in checklists]})
    
    @app.route('/api/powerbi/compliance_items')
    def api_powerbi_compliance_items():
        """Power BI: Get all compliance items"""
        items = ComplianceItem.query.all()
        return jsonify({'data': [{
            'id': i.id,
            'checklist_id': i.checklist_id,
            'compliance_area_id': i.compliance_area_id,
            'item_code': i.item_code,
            'requirement': i.requirement,
            'evidence_required': i.evidence_required,
            'status': i.status,
            'evidence_ref': i.evidence_ref,
            'remarks': i.remarks,
            'evidence_file_path': i.evidence_file_path,
            'created_at': i.created_at.isoformat() if i.created_at else None,
            'updated_at': i.updated_at.isoformat() if i.updated_at else None
        } for i in items]})
    
    @app.route('/api/powerbi/compliance_areas')
    def api_powerbi_compliance_areas():
        """Power BI: Get all compliance areas"""
        areas = ComplianceArea.query.all()
        return jsonify({'data': [{
            'id': a.id,
            'area_name': a.area_name,
            'description': a.description,
            'regulation_code': a.regulation_code,
            'active': a.active
        } for a in areas]})
    
    @app.route('/api/powerbi/system_scores')
    def api_powerbi_system_scores():
        """Power BI: Get all system scores"""
        scores = SystemScore.query.all()
        return jsonify({'data': [{
            'id': s.id,
            'building_id': s.building_id,
            'system_id': s.system_id,
            'item_count': s.item_count,
            'score_percent': s.score_percent,
            'weight': s.weight,
            'weighted_score': s.weighted_score,
            'created_at': s.created_at.isoformat() if s.created_at else None,
            'updated_at': s.updated_at.isoformat() if s.updated_at else None
        } for s in scores]})
    
    @app.route('/api/powerbi/test_registers')
    def api_powerbi_test_registers():
        """Power BI: Get all test registers"""
        tests = TestRegister.query.all()
        return jsonify({'data': [{
            'id': t.id,
            'building_id': t.building_id,
            'system_id': t.system_id,
            'test_id': t.test_id,
            'test_name': t.test_name,
            'standard_reference': t.standard_reference,
            'instrument': t.instrument,
            'locations_sampling': t.locations_sampling,
            'acceptance_criteria': t.acceptance_criteria,
            'readings': t.readings,
            'result': t.result,
            'witness': t.witness,
            'test_date': t.test_date.isoformat() if t.test_date else None,
            'evidence_ref': t.evidence_ref,
            'remarks': t.remarks,
            'created_at': t.created_at.isoformat() if t.created_at else None,
            'updated_at': t.updated_at.isoformat() if t.updated_at else None
        } for t in tests]})
    
    @app.route('/api/powerbi/capa_registers')
    def api_powerbi_capa_registers():
        """Power BI: Get all CAPA registers"""
        capas = CAPARegister.query.all()
        return jsonify({'data': [{
            'id': c.id,
            'building_id': c.building_id,
            'system_id': c.system_id,
            'assessment_item_id': c.assessment_item_id,
            'capa_id': c.capa_id,
            'priority': c.priority,
            'finding': c.finding,
            'required_action': c.required_action,
            'responsibility_id': c.responsibility_id,
            'due_date': c.due_date.isoformat() if c.due_date else None,
            'estimated_cost': c.estimated_cost,
            'status': c.status,
            'verification_evidence': c.verification_evidence,
            'verification_date': c.verification_date.isoformat() if c.verification_date else None,
            'remarks': c.remarks,
            'is_overdue': c.is_overdue(),
            'created_at': c.created_at.isoformat() if c.created_at else None,
            'updated_at': c.updated_at.isoformat() if c.updated_at else None
        } for c in capas]})
    
    @app.route('/api/powerbi/executive_dashboard')
    def api_powerbi_executive_dashboard():
        """Power BI: Get all executive dashboard summaries"""
        dashboards = ExecutiveDashboardSummary.query.all()
        return jsonify({'data': [{
            'id': d.id,
            'building_id': d.building_id,
            'overall_building_score': d.overall_building_score,
            'overall_compliance_percent': d.overall_compliance_percent,
            'threshold_pass': d.threshold_pass,
            'total_assessment_items': d.total_assessment_items,
            'items_open': d.items_open,
            'items_in_progress': d.items_in_progress,
            'items_closed': d.items_closed,
            'items_verified': d.items_verified,
            'risk_critical': d.risk_critical,
            'risk_high': d.risk_high,
            'risk_medium': d.risk_medium,
            'risk_low': d.risk_low,
            'risk_acceptable': d.risk_acceptable,
            'capa_open': d.capa_open,
            'capa_in_progress': d.capa_in_progress,
            'capa_closed': d.capa_closed,
            'capa_overdue': d.capa_overdue,
            'test_pass': d.test_pass,
            'test_fail': d.test_fail,
            'test_need_attention': d.test_need_attention,
            'notes_observations': d.notes_observations,
            'computed_at': d.computed_at.isoformat() if d.computed_at else None
        } for d in dashboards]})
    
    @app.route('/api/powerbi/responsibilities')
    def api_powerbi_responsibilities():
        """Power BI: Get all responsibilities"""
        responsibilities = Responsibility.query.all()
        return jsonify({'data': [{
            'id': r.id,
            'name': r.name,
            'description': r.description,
            'active': r.active
        } for r in responsibilities]})
    
    @app.route('/api/powerbi/priorities')
    def api_powerbi_priorities():
        """Power BI: Get all priorities"""
        priorities = Priority.query.all()
        return jsonify({'data': [{
            'id': p.id,
            'priority_name': p.priority_name,
            'order': p.order,
            'active': p.active
        } for p in priorities]})
    
    @app.route('/api/powerbi/rates')
    def api_powerbi_rates():
        """Power BI: Get all rates"""
        rates = Rate.query.all()
        return jsonify({'data': [{
            'id': r.id,
            'rate_value': r.rate_value,
            'description': r.description,
            'active': r.active
        } for r in rates]})
    
    @app.route('/api/powerbi/weights')
    def api_powerbi_weights():
        """Power BI: Get all weights"""
        weights = Weight.query.all()
        return jsonify({'data': [{
            'id': w.id,
            'weight_value': w.weight_value,
            'description': w.description,
            'active': w.active
        } for w in weights]})
    
    @app.route('/api/powerbi/audit_logs')
    def api_powerbi_audit_logs():
        """Power BI: Get all audit logs"""
        logs = AuditLog.query.all()
        return jsonify({'data': [{
            'id': l.id,
            'user_id': l.user_id,
            'table_name': l.table_name,
            'record_id': l.record_id,
            'action': l.action,
            'old_values': l.old_values,
            'new_values': l.new_values,
            'timestamp': l.timestamp.isoformat() if l.timestamp else None
        } for l in logs]})
    
    @app.route('/api/seed-systems-hierarchy')
    def api_seed_systems_hierarchy():
        """Seed complete systems, subsystems, and components hierarchy"""
        try:
            # Complete 21 Systems with Subsystems and Components
            SYSTEMS_HIERARCHY = {
                'Fire_LifeSafety': {
                    'name': 'Fire & Life Safety',
                    'subsystems': {
                        'Fire Detection': ['Smoke Detectors', 'Heat Detectors', 'Manual Call Points', 'Fire Alarm Panel', 'Beam Detectors'],
                        'Fire Suppression': ['Sprinkler System', 'Fire Extinguishers', 'FM200 System', 'CO2 System', 'Foam System'],
                        'Emergency Systems': ['Emergency Lighting', 'Exit Signs', 'PA System', 'Fire Doors', 'Smoke Dampers'],
                    }
                },
                'Electrical': {
                    'name': 'Electrical Systems',
                    'subsystems': {
                        'Power Distribution': ['Main Switchboard', 'Distribution Boards', 'Busway System', 'Cable Trays', 'Power Cables'],
                        'Lighting': ['General Lighting', 'Task Lighting', 'Decorative Lighting', 'External Lighting', 'Control Systems'],
                        'Earthing & Protection': ['Earthing System', 'Lightning Protection', 'Surge Protection', 'RCDs', 'MCBs'],
                    }
                },
                'HVAC': {
                    'name': 'HVAC Systems',
                    'subsystems': {
                        'Cooling': ['Chillers', 'AHUs', 'FCUs', 'Split Units', 'VRF System'],
                        'Heating': ['Boilers', 'Heat Pumps', 'Radiators', 'Underfloor Heating', 'Heat Exchangers'],
                        'Ventilation': ['Supply Fans', 'Extract Fans', 'Ductwork', 'Grilles & Diffusers', 'Dampers'],
                    }
                },
                'Plumbing': {
                    'name': 'Plumbing Systems',
                    'subsystems': {
                        'Water Supply': ['Main Supply', 'Pumps', 'Storage Tanks', 'PRVs', 'Piping'],
                        'Drainage': ['Soil Pipes', 'Waste Pipes', 'Floor Drains', 'Manholes', 'Inspection Chambers'],
                        'Fixtures': ['WCs', 'Basins', 'Showers', 'Baths', 'Kitchen Sinks'],
                    }
                },
                'Structural': {
                    'name': 'Structural Systems',
                    'subsystems': {
                        'Foundations': ['Pile Caps', 'Raft Foundation', 'Strip Footings', 'Ground Beams', 'Basement Walls'],
                        'Superstructure': ['Columns', 'Beams', 'Slabs', 'Walls', 'Stairs'],
                        'Roof Structure': ['Roof Slab', 'Steel Trusses', 'Purlins', 'Roof Beams', 'Parapet Walls'],
                    }
                },
                'Roofing': {
                    'name': 'Roofing Systems',
                    'subsystems': {
                        'Roof Covering': ['Membrane', 'Tiles', 'Metal Sheets', 'Insulation', 'Vapor Barrier'],
                        'Drainage': ['Gutters', 'Downpipes', 'Roof Drains', 'Overflow Pipes', 'Scuppers'],
                        'Accessories': ['Skylights', 'Roof Hatches', 'Ventilators', 'Flashings', 'Expansion Joints'],
                    }
                },
                'Cladding': {
                    'name': 'Facade & Cladding',
                    'subsystems': {
                        'Curtain Wall': ['Aluminum Frames', 'Glass Panels', 'Spandrel Panels', 'Sealants', 'Gaskets'],
                        'External Finishes': ['Stone Cladding', 'Metal Panels', 'Render', 'Paint', 'Ceramic Tiles'],
                        'Openings': ['Windows', 'Doors', 'Louvers', 'Vents', 'Shutters'],
                    }
                },
                'Doors_Windows': {
                    'name': 'Doors & Windows',
                    'subsystems': {
                        'Doors': ['Entrance Doors', 'Internal Doors', 'Fire Doors', 'Access Doors', 'Revolving Doors'],
                        'Windows': ['Fixed Windows', 'Openable Windows', 'Curtain Wall Windows', 'Roof Lights', 'Glass Blocks'],
                        'Hardware': ['Locks', 'Hinges', 'Door Closers', 'Panic Hardware', 'Handles'],
                    }
                },
                'Interior_Finishes': {
                    'name': 'Interior Finishes',
                    'subsystems': {
                        'Floors': ['Tiles', 'Carpet', 'Vinyl', 'Marble', 'Raised Floor'],
                        'Walls': ['Paint', 'Wallpaper', 'Tiles', 'Paneling', 'Plaster'],
                        'Ceilings': ['Suspended Ceiling', 'Gypsum Board', 'Metal Ceiling', 'Exposed Ceiling', 'Acoustic Ceiling'],
                    }
                },
                'Accessibility': {
                    'name': 'Accessibility Features',
                    'subsystems': {
                        'Circulation': ['Ramps', 'Handrails', 'Tactile Paving', 'Lifts', 'Platform Lifts'],
                        'Facilities': ['Accessible WCs', 'Shower Rooms', 'Baby Change', 'Refuge Areas', 'Hearing Loops'],
                        'Signage': ['Braille Signs', 'Tactile Signs', 'Contrast Markings', 'Wayfinding', 'Emergency Signs'],
                    }
                },
                'Security': {
                    'name': 'Security Systems',
                    'subsystems': {
                        'Access Control': ['Card Readers', 'Biometric Readers', 'Intercoms', 'Turnstiles', 'Barriers'],
                        'CCTV': ['Cameras', 'Recorders', 'Monitors', 'Analytics', 'Storage'],
                        'Intruder Alarm': ['PIR Sensors', 'Door Contacts', 'Glass Break Sensors', 'Control Panel', 'Keypads'],
                    }
                },
                'Vertical_Transport': {
                    'name': 'Vertical Transport (Lifts)',
                    'subsystems': {
                        'Passenger Lifts': ['Machine', 'Controller', 'Car', 'Doors', 'Safety Gear'],
                        'Goods Lifts': ['Platform', 'Controls', 'Gates', 'Motor', 'Cables'],
                        'Escalators': ['Steps', 'Handrails', 'Motor', 'Controller', 'Safety Switches'],
                    }
                },
                'Controls': {
                    'name': 'Building Management Controls',
                    'subsystems': {
                        'BMS': ['Controllers', 'Sensors', 'Actuators', 'Software', 'Network'],
                        'Metering': ['Electric Meters', 'Water Meters', 'Gas Meters', 'BTU Meters', 'Data Loggers'],
                        'Integration': ['Gateways', 'Protocols', 'Head End', 'Graphics', 'Alarms'],
                    }
                },
                'Maintenance': {
                    'name': 'Maintenance & Operations',
                    'subsystems': {
                        'Facilities': ['Plant Rooms', 'Stores', 'Workshops', 'Loading Bays', 'Waste Areas'],
                        'Access': ['Maintenance Walkways', 'Ladders', 'Platforms', 'Cradles', 'Anchor Points'],
                        'Equipment': ['Tools', 'Spares', 'Consumables', 'PPE', 'Testing Equipment'],
                    }
                },
                'Landscaping': {
                    'name': 'Landscaping & Grounds',
                    'subsystems': {
                        'Hard Landscaping': ['Paving', 'Kerbs', 'Steps', 'Retaining Walls', 'Fencing'],
                        'Soft Landscaping': ['Trees', 'Shrubs', 'Lawns', 'Planters', 'Irrigation'],
                        'Features': ['Water Features', 'Sculptures', 'Seating', 'Pergolas', 'Outdoor Lighting'],
                    }
                },
                'Parking': {
                    'name': 'Parking Facilities',
                    'subsystems': {
                        'Structure': ['Ramps', 'Floors', 'Barriers', 'Markings', 'Signage'],
                        'Systems': ['Payment Systems', 'Guidance Systems', 'Ventilation', 'Fire Systems', 'CCTV'],
                        'EV Charging': ['Chargers', 'Cable Management', 'Payment', 'Signage', 'Power Supply'],
                    }
                },
                'Signage': {
                    'name': 'Signage Systems',
                    'subsystems': {
                        'Wayfinding': ['Directories', 'Directional Signs', 'Room Signs', 'Floor Signs', 'Maps'],
                        'Safety': ['Fire Signs', 'Exit Signs', 'Warning Signs', 'Prohibition Signs', 'Mandatory Signs'],
                        'Information': ['Notice Boards', 'Digital Displays', 'Tenant Boards', 'Reception Signs', 'External Signs'],
                    }
                },
                'IT_Telecom': {
                    'name': 'IT & Telecommunications',
                    'subsystems': {
                        'Data Network': ['Switches', 'Routers', 'Cabling', 'Patch Panels', 'Racks'],
                        'Voice': ['PABX', 'Handsets', 'Voice Cabling', 'Conference Systems', 'Voicemail'],
                        'Wireless': ['Access Points', 'Controllers', 'Antennas', 'DAS', 'WiFi'],
                    }
                },
                'Wastewater': {
                    'name': 'Wastewater Systems',
                    'subsystems': {
                        'Collection': ['Grease Traps', 'Interceptors', 'Pumping Stations', 'Manholes', 'Piping'],
                        'Treatment': ['Septic Tanks', 'Treatment Plants', 'Filters', 'Disinfection', 'Sludge Handling'],
                        'Disposal': ['Soak-aways', 'Discharge Points', 'Recycling', 'Monitoring', 'Controls'],
                    }
                },
                'Waste_Management': {
                    'name': 'Waste Management',
                    'subsystems': {
                        'Collection': ['Bins', 'Chutes', 'Compactors', 'Balers', 'Containers'],
                        'Storage': ['Bin Stores', 'Recycling Areas', 'Hazardous Stores', 'Cold Stores', 'Wash Down'],
                        'Disposal': ['Collection Points', 'Schedules', 'Contractors', 'Documentation', 'Monitoring'],
                    }
                },
                'Energy_Efficiency': {
                    'name': 'Energy & Efficiency',
                    'subsystems': {
                        'Renewables': ['Solar PV', 'Solar Thermal', 'Wind', 'Heat Recovery', 'Biomass'],
                        'Efficiency': ['LED Lighting', 'VFDs', 'Insulation', 'Glazing', 'Controls'],
                        'Monitoring': ['Energy Dashboard', 'Sub-metering', 'Benchmarking', 'Reporting', 'Targets'],
                    }
                },
            }
            
            created_systems = 0
            created_subsystems = 0
            created_components = 0
            
            for sys_order, (sys_code, sys_data) in enumerate(SYSTEMS_HIERARCHY.items(), 1):
                # Check if system exists
                system = System.query.filter_by(system_code=sys_code).first()
                if not system:
                    system = System(
                        system_code=sys_code,
                        system_name=sys_data['name'],
                        description=f"Building system for {sys_data['name']}",
                        order=sys_order,
                        active=True
                    )
                    db.session.add(system)
                    db.session.flush()
                    created_systems += 1
                
                # Add subsystems
                for sub_order, (sub_name, components) in enumerate(sys_data['subsystems'].items(), 1):
                    sub_code = f"{sys_code}_{sub_name.replace(' ', '_').replace('&', 'and')}"
                    subsystem = Subsystem.query.filter_by(subsystem_code=sub_code).first()
                    if not subsystem:
                        subsystem = Subsystem(
                            system_id=system.id,
                            subsystem_code=sub_code,
                            subsystem_name=sub_name,
                            description=f"Subsystem: {sub_name} under {sys_data['name']}",
                            order=sub_order,
                            active=True
                        )
                        db.session.add(subsystem)
                        db.session.flush()
                        created_subsystems += 1
                    
                    # Add components
                    for comp_order, comp_name in enumerate(components, 1):
                        comp_code = f"{sub_code}_{comp_name.replace(' ', '_').replace('&', 'and')}"
                        component = Component.query.filter_by(component_code=comp_code).first()
                        if not component:
                            component = Component(
                                subsystem_id=subsystem.id,
                                component_code=comp_code,
                                component_name=comp_name,
                                description=f"Component: {comp_name}",
                                order=comp_order,
                                active=True
                            )
                            db.session.add(component)
                            created_components += 1
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Systems hierarchy seeded successfully',
                'created': {
                    'systems': created_systems,
                    'subsystems': created_subsystems,
                    'components': created_components
                },
                'totals': {
                    'systems': System.query.count(),
                    'subsystems': Subsystem.query.count(),
                    'components': Component.query.count()
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/seed-sample-data')
    def api_seed_sample_data():
        """Seed sample data for Power BI testing"""
        import random
        from datetime import timedelta
        
        try:
            # First seed systems hierarchy
            api_seed_systems_hierarchy()
            
            # Get existing data
            systems = System.query.all()
            subsystems = Subsystem.query.all()
            
            # Ensure we have a user
            user = User.query.first()
            if not user:
                user = User(username='admin', email='admin@daralriyadh.com', role='Admin', is_active=True)
                user.set_password('admin123')
                db.session.add(user)
                db.session.commit()
            
            # Add compliance areas if not exists
            if ComplianceArea.query.count() == 0:
                areas = [
                    ('Civil Defense Approval', 'Fire safety compliance', 'CD-001'),
                    ('Municipality License', 'Building permit compliance', 'MUN-001'),
                    ('Electricity Approval', 'Electrical compliance', 'SEC-001'),
                    ('Water Authority', 'Water systems compliance', 'NWC-001'),
                    ('Environmental', 'Environmental compliance', 'ENV-001'),
                ]
                for name, desc, code in areas:
                    db.session.add(ComplianceArea(area_name=name, description=desc, regulation_code=code, active=True))
                db.session.commit()
            
            # Add sample buildings
            buildings_data = [
                ('King Fahd Medical City', 'BLDG-001', 'Riyadh', 'King Fahd Road', 24.7136, 46.6753, 'Hospital', 'Healthcare', 50000, 10, 1995),
                ('Al Faisaliah Tower', 'BLDG-002', 'Riyadh', 'King Fahd Road', 24.6908, 46.6855, 'Commercial', 'Office', 120000, 44, 2000),
                ('Kingdom Centre', 'BLDG-003', 'Riyadh', 'Olaya Street', 24.7117, 46.6742, 'Mixed Use', 'Commercial', 185000, 99, 2002),
            ]
            
            buildings = []
            for name, code, city, addr, lat, lng, btype, use, area, floors, year in buildings_data:
                existing = Building.query.filter_by(building_code=code).first()
                if not existing:
                    b = Building(
                        project_name=name, building_code=code, city=city, address=addr,
                        latitude=lat, longitude=lng, building_type=btype, primary_use=use,
                        gross_built_area_m2=area, number_of_floors=floors, construction_year=year,
                        inspection_date=date.today(), current_year=2026, system_threshold_percent=75.0,
                        estimated_life_time_years=50, fm_contractor='Dar Al Riyadh',
                        created_by_id=user.id, status='InProgress'
                    )
                    db.session.add(b)
                    buildings.append(b)
                else:
                    buildings.append(existing)
            db.session.commit()
            
            # Add assessments
            for b in buildings:
                if Assessment.query.filter_by(building_id=b.id).count() == 0:
                    assessment = Assessment(building_id=b.id, assessment_code=f'ASS-{b.building_code}', status='In Progress')
                    db.session.add(assessment)
            db.session.commit()
            
            # Add assessment items
            assessments = Assessment.query.all()
            for assessment in assessments:
                if AssessmentItem.query.filter_by(assessment_id=assessment.id).count() == 0:
                    for i in range(5):
                        system = systems[i % len(systems)] if systems else None
                        subsystem = Subsystem.query.filter_by(system_id=system.id).first() if system else None
                        component = Component.query.filter_by(subsystem_id=subsystem.id).first() if subsystem else None
                        if system and subsystem and component:
                            rate_val = random.choice([3, 4, 5])
                            weight_val = random.choice([1.0, 1.5, 2.0])
                            item = AssessmentItem(
                                assessment_id=assessment.id, system_id=system.id,
                                subsystem_id=subsystem.id, component_id=component.id,
                                item_code=f'ITEM-{assessment.id}-{i+1}',
                                inspection_item=f'Inspection of {component.component_name}',
                                criteria='Visual inspection', test_method='Visual',
                                rate=rate_val, item_weight=weight_val,
                                risk_criticality=random.randint(1, 5),
                                priority=random.choice(['P1', 'P2', 'P3', 'P4']),
                                status=random.choice(['Open', 'In Progress', 'Closed']),
                                score=rate_val * 20, score_percent=(rate_val * 20) / 100.0,
                                weighted_score=((rate_val * 20) / 100.0) * weight_val
                            )
                            db.session.add(item)
            db.session.commit()
            
            # Add compliance checklists
            compliance_areas = ComplianceArea.query.all()
            for b in buildings:
                if ComplianceChecklist.query.filter_by(building_id=b.id).count() == 0:
                    checklist = ComplianceChecklist(building_id=b.id, checklist_code=f'CC-{b.building_code}', status='In Progress')
                    db.session.add(checklist)
                    db.session.flush()
                    for i, area in enumerate(compliance_areas[:3]):
                        item = ComplianceItem(
                            checklist_id=checklist.id, compliance_area_id=area.id,
                            item_code=f'CI-{checklist.id}-{i+1}', requirement=f'Compliance with {area.area_name}',
                            evidence_required=True, status=random.choice(['Yes', 'No', 'Partial']),
                            evidence_ref=f'DOC-{i+1}', remarks='Reviewed'
                        )
                        db.session.add(item)
            db.session.commit()
            
            # Add system scores
            for b in buildings:
                for system in systems[:5]:
                    if SystemScore.query.filter_by(building_id=b.id, system_id=system.id).count() == 0:
                        score = SystemScore(
                            building_id=b.id, system_id=system.id,
                            item_count=random.randint(5, 20), score_percent=random.uniform(70, 95),
                            weight=random.uniform(5, 15), weighted_score=random.uniform(5, 12)
                        )
                        db.session.add(score)
            db.session.commit()
            
            # Add test registers
            for b in buildings:
                if TestRegister.query.filter_by(building_id=b.id).count() == 0:
                    for i, system in enumerate(systems[:3]):
                        test = TestRegister(
                            building_id=b.id, system_id=system.id,
                            test_id=f'TEST-{b.id}-{i+1}', test_name=f'{system.system_name} Test',
                            standard_reference='ASHRAE/NFPA', instrument='Multi-meter',
                            acceptance_criteria='Within range', result=random.choice(['Pass', 'Fail', 'Need Attention']),
                            witness='Engineer', test_date=date.today() - timedelta(days=random.randint(1, 30)),
                            evidence_ref=f'TEST-DOC-{i+1}', remarks='Completed'
                        )
                        db.session.add(test)
            db.session.commit()
            
            # Add CAPA registers
            responsibilities = Responsibility.query.all()
            for b in buildings:
                if CAPARegister.query.filter_by(building_id=b.id).count() == 0:
                    for i, system in enumerate(systems[:3]):
                        resp = responsibilities[i % len(responsibilities)] if responsibilities else None
                        capa = CAPARegister(
                            building_id=b.id, system_id=system.id,
                            capa_id=f'CAPA-{b.id}-{i+1}', priority=random.choice(['P1', 'P2', 'P3', 'P4']),
                            finding=f'Issue in {system.system_name}', required_action='Repair required',
                            responsibility_id=resp.id if resp else None,
                            due_date=date.today() + timedelta(days=random.randint(7, 60)),
                            estimated_cost=random.uniform(5000, 50000),
                            status=random.choice(['Open', 'In Progress', 'Closed']), remarks='Action needed'
                        )
                        db.session.add(capa)
            db.session.commit()
            
            # Add executive dashboard summaries
            for b in buildings:
                if ExecutiveDashboardSummary.query.filter_by(building_id=b.id).count() == 0:
                    dashboard = ExecutiveDashboardSummary(
                        building_id=b.id, overall_building_score=random.uniform(70, 95),
                        overall_compliance_percent=random.uniform(75, 98), threshold_pass=True,
                        total_assessment_items=random.randint(50, 200),
                        items_open=random.randint(5, 20), items_in_progress=random.randint(10, 30),
                        items_closed=random.randint(30, 100), items_verified=random.randint(20, 50),
                        risk_critical=random.randint(0, 3), risk_high=random.randint(2, 8),
                        risk_medium=random.randint(5, 15), risk_low=random.randint(10, 30),
                        risk_acceptable=random.randint(20, 50), capa_open=random.randint(2, 10),
                        capa_in_progress=random.randint(3, 8), capa_closed=random.randint(10, 30),
                        capa_overdue=random.randint(0, 3), test_pass=random.randint(15, 40),
                        test_fail=random.randint(0, 5), test_need_attention=random.randint(2, 8),
                        notes_observations='Assessment in progress'
                    )
                    db.session.add(dashboard)
            db.session.commit()
            
            # Add audit logs
            if AuditLog.query.count() == 0:
                for i in range(5):
                    log = AuditLog(
                        user_id=user.id, table_name=random.choice(['buildings', 'assessments']),
                        record_id=random.randint(1, 10), action=random.choice(['CREATE', 'UPDATE']),
                        old_values={'status': 'Draft'}, new_values={'status': 'InProgress'}
                    )
                    db.session.add(log)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Sample data seeded successfully',
                'counts': {
                    'users': User.query.count(),
                    'buildings': Building.query.count(),
                    'assessments': Assessment.query.count(),
                    'assessment_items': AssessmentItem.query.count(),
                    'compliance_checklists': ComplianceChecklist.query.count(),
                    'compliance_items': ComplianceItem.query.count(),
                    'system_scores': SystemScore.query.count(),
                    'test_registers': TestRegister.query.count(),
                    'capa_registers': CAPARegister.query.count(),
                    'executive_dashboards': ExecutiveDashboardSummary.query.count(),
                    'audit_logs': AuditLog.query.count()
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ==================== STEP 2: ASSESSMENT ITEM EDIT/DELETE ====================
    
    @app.route('/building/<int:building_id>/assessment/item/<int:item_id>/edit', methods=['GET', 'POST'])
    @login_required
    def assessment_item_edit(building_id, item_id):
        """Edit assessment item"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        item = AssessmentItem.query.get_or_404(item_id)
        
        from forms import AssessmentItemForm
        form = AssessmentItemForm(obj=item)
        
        # Populate dropdowns
        form.system.choices = [(0, '-- Select System --')] + [(s.id, s.system_name) for s in System.query.filter_by(active=True).all()]
        form.subsystem.choices = [(0, '-- Select System First --')]
        form.component.choices = [(0, '-- Select Subsystem First --')]
        form.rate.choices = [(r.rate_value, f"{r.rate_value} - {r.description}") 
                             for r in Rate.query.filter_by(active=True).order_by(Rate.rate_value).all()]
        form.item_weight.choices = [(w.weight_value, str(w.weight_value)) 
                                     for w in Weight.query.filter_by(active=True).all()]
        form.responsibility.choices = [(0, '-- Select --')] + [(r.id, r.name) 
                                        for r in Responsibility.query.filter_by(active=True).all()]
        
        if form.validate_on_submit():
            old_data = item.as_dict()
            
            item.system_id = form.system.data
            item.rate = form.rate.data
            item.item_weight = form.item_weight.data
            item.risk_criticality = form.risk_criticality.data
            item.responsibility_id = form.responsibility.data if form.responsibility.data > 0 else None
            item.priority = form.priority.data
            item.status = form.status.data
            item.due_date = form.due_date.data
            item.remarks = form.remarks.data
            
            # Recalculate scores
            CalculationService.calculate_assessment_item_scores(item)
            db.session.commit()
            
            # Recalculate system metrics
            CalculationService.calculate_system_metrics(building_id, item.system_id)
            CalculationService.compute_executive_dashboard(building_id)
            db.session.commit()
            
            _log_audit('assessment_items', item.id, 'UPDATE', old_data, item.as_dict())
            
            flash('Assessment item updated!', 'success')
            return redirect(url_for('assessment_items_list', building_id=building_id))
        
        return render_template('assessment_item_form.html', form=form, building=building, item=item, edit_mode=True)
    
    @app.route('/building/<int:building_id>/assessment/item/<int:item_id>/delete', methods=['POST'])
    @login_required
    def assessment_item_delete(building_id, item_id):
        """Delete assessment item"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        item = AssessmentItem.query.get_or_404(item_id)
        system_id = item.system_id
        
        _log_audit('assessment_items', item.id, 'DELETE', item.as_dict(), None)
        
        db.session.delete(item)
        db.session.commit()
        
        # Recalculate system metrics
        CalculationService.calculate_system_metrics(building_id, system_id)
        CalculationService.compute_executive_dashboard(building_id)
        db.session.commit()
        
        flash('Assessment item deleted!', 'warning')
        return redirect(url_for('assessment_items_list', building_id=building_id))
    
    # ==================== STEP 3: COMPLIANCE CRUD ====================
    
    @app.route('/building/<int:building_id>/compliance/item/new', methods=['GET', 'POST'])
    @app.route('/building/<int:building_id>/compliance/item/new/<int:area_id>', methods=['GET', 'POST'])
    @login_required
    def compliance_item_new(building_id, area_id=None):
        """Add new compliance item"""
        import os
        from werkzeug.utils import secure_filename
        
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        from forms import ComplianceItemForm
        form = ComplianceItemForm()
        
        # Get or create checklist
        checklist = ComplianceChecklist.query.filter_by(building_id=building_id).first()
        if not checklist:
            checklist = ComplianceChecklist(
                building_id=building_id,
                checklist_code=f"CCL-{building_id}-001",
                status='Open'
            )
            db.session.add(checklist)
            db.session.commit()
        
        areas = ComplianceArea.query.filter_by(active=True).all()
        
        if request.method == 'POST':
            area_id_form = request.form.get('compliance_area_id')
            requirement = request.form.get('requirement')
            status = request.form.get('status')
            evidence_ref = request.form.get('evidence_ref')
            remarks = request.form.get('remarks')
            
            # Generate item code
            count = ComplianceItem.query.filter_by(checklist_id=checklist.id).count()
            item_code = f"GC-{count + 1:03d}"
            
            # Handle file upload
            evidence_file_path = None
            if 'evidence_file' in request.files:
                file = request.files['evidence_file']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    # Create upload directory if not exists
                    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'compliance', str(building_id))
                    os.makedirs(upload_dir, exist_ok=True)
                    # Add timestamp to filename to avoid conflicts
                    import time
                    timestamped_filename = f"{int(time.time())}_{filename}"
                    file_path = os.path.join(upload_dir, timestamped_filename)
                    file.save(file_path)
                    # Store relative path for serving
                    evidence_file_path = f"uploads/compliance/{building_id}/{timestamped_filename}"
            
            item = ComplianceItem(
                checklist_id=checklist.id,
                compliance_area_id=int(area_id_form) if area_id_form else None,
                item_code=item_code,
                requirement=requirement or '',
                status=status,
                evidence_ref=evidence_ref,
                remarks=remarks,
                evidence_file_path=evidence_file_path
            )
            db.session.add(item)
            db.session.commit()
            
            flash('Compliance item added!', 'success')
            return redirect(url_for('compliance_checklist', building_id=building_id))
        
        return render_template('compliance_item_form.html', form=form, building=building, areas=areas, selected_area_id=area_id)
    
    # ==================== STEP 4: SYSTEM SCORING UPDATE ====================
    
    @app.route('/building/<int:building_id>/system-scoring/update', methods=['POST'])
    @login_required
    def system_scoring_update(building_id):
        """Update system weights"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        # Get all weights from form
        total_weight = 0
        updates = []
        
        for key, value in request.form.items():
            if key.startswith('weight_'):
                system_id = int(key.replace('weight_', ''))
                weight = float(value) if value else 0
                total_weight += weight
                updates.append((system_id, weight))
        
        # Validate total weight = 100
        if abs(total_weight - 100) > 0.01:
            flash(f'Total weight must equal 100%. Current total: {total_weight:.1f}%', 'danger')
            return redirect(url_for('system_scoring', building_id=building_id))
        
        # Update weights
        for system_id, weight in updates:
            score = SystemScore.query.filter_by(building_id=building_id, system_id=system_id).first()
            if score:
                score.weight = weight
                score.calculate_weighted_score()
        
        db.session.commit()
        
        # Recalculate dashboard
        CalculationService.compute_executive_dashboard(building_id)
        db.session.commit()
        
        flash('System weights updated successfully!', 'success')
        return redirect(url_for('system_scoring', building_id=building_id))
    
    # ==================== STEP 5: TEST REGISTER CRUD ====================
    
    @app.route('/building/<int:building_id>/tests/new', methods=['GET', 'POST'])
    @login_required
    def test_register_new(building_id):
        """Add new test record"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        from forms import TestRegisterForm
        form = TestRegisterForm()
        form.system.choices = [(s.id, s.system_name) for s in System.query.filter_by(active=True).all()]
        
        if form.validate_on_submit():
            test = TestRegister(
                building_id=building_id,
                system_id=form.system.data,
                test_id=form.test_id.data,
                test_name=form.test_name.data,
                standard_reference=form.standard_reference.data,
                instrument=form.instrument.data,
                locations_sampling=form.locations_sampling.data,
                acceptance_criteria=form.acceptance_criteria.data,
                readings=form.readings.data,
                result=form.result.data,
                test_date=form.test_date.data,
                witness=form.witness.data,
                evidence_ref=form.evidence_ref.data,
                remarks=form.remarks.data
            )
            db.session.add(test)
            db.session.commit()
            
            # Recalculate dashboard
            CalculationService.compute_executive_dashboard(building_id)
            db.session.commit()
            
            flash('Test record added!', 'success')
            return redirect(url_for('test_register', building_id=building_id))
        
        return render_template('test_register_form.html', form=form, building=building)
    
    # ==================== STEP 6: CAPA CRUD ====================
    
    @app.route('/building/<int:building_id>/capa/new', methods=['GET', 'POST'])
    @login_required
    def capa_register_new(building_id):
        """Add new CAPA record"""
        building = Building.query.get_or_404(building_id)
        _check_access(building)
        
        from forms import CAPARegisterForm
        form = CAPARegisterForm()
        form.system.choices = [(s.id, s.system_name) for s in System.query.filter_by(active=True).all()]
        form.responsibility.choices = [(0, '-- Select --')] + [(r.id, r.name) 
                                        for r in Responsibility.query.filter_by(active=True).all()]
        
        # Auto-generate CAPA ID
        count = CAPARegister.query.filter_by(building_id=building_id).count()
        suggested_id = f"CAPA-{building_id:03d}-{count + 1:04d}"
        
        if form.validate_on_submit():
            capa = CAPARegister(
                building_id=building_id,
                system_id=form.system.data,
                capa_id=form.capa_id.data or suggested_id,
                priority=form.priority.data,
                finding=form.finding.data,
                required_action=form.required_action.data,
                responsibility_id=form.responsibility.data if form.responsibility.data > 0 else None,
                due_date=form.due_date.data,
                estimated_cost=form.estimated_cost.data,
                status=form.status.data,
                verification_evidence=form.verification_evidence.data,
                verification_date=form.verification_date.data,
                remarks=form.remarks.data
            )
            db.session.add(capa)
            db.session.commit()
            
            # Recalculate dashboard
            CalculationService.compute_executive_dashboard(building_id)
            db.session.commit()
            
            flash('CAPA record added!', 'success')
            return redirect(url_for('capa_register', building_id=building_id))
        
        return render_template('capa_register_form.html', form=form, building=building, suggested_id=suggested_id)
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def _check_access(building):
        """Check if current user has access to building"""
        if building.created_by_id != current_user.id and current_user.role != 'Admin':
            flash('Access denied', 'danger')
            redirect(url_for('dashboard'))
    
    def _log_audit(table, record_id, action, old_vals, new_vals):
        """Log audit event"""
        audit = AuditLog(
            user_id=current_user.id,
            table_name=table,
            record_id=record_id,
            action=action,
            old_values=old_vals,
            new_values=new_vals,
            timestamp=datetime.utcnow()
        )
        db.session.add(audit)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
