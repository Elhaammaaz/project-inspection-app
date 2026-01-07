"""
Calculation Engine - Server-side business logic for all aggregations
Replaces Excel formulas with production-grade Python service
"""

from models import (
    db, AssessmentItem, Assessment, SystemScore, TestRegister, TestResultEnum,
    CAPARegister, ComplianceItem, ExecutiveDashboardSummary, Building, System
)
from datetime import date


class CalculationService:
    """Core calculations for BCAR workflow"""
    
    @staticmethod
    def calculate_assessment_item_scores(item):
        """
        Calculate scores for an assessment item (called on every update)
        
        Formula:
        - Score = Rate × 2 × 10
        - Score % = Score / 100
        - Weighted Score = Score % × Item Weight
        """
        if item.rate is None:
            item.score = None
            item.score_percent = None
            item.weighted_score = None
            return
        
        # Calculate score: Rate × 2 × 10
        item.score = item.rate * 2 * 10
        
        # Calculate score percent: Score / 100
        item.score_percent = item.score / 100.0
        
        # Calculate weighted score if weight is set
        if item.item_weight:
            item.weighted_score = item.score_percent * item.item_weight
        
        return item
    
    @staticmethod
    def calculate_system_metrics(building_id, system_id):
        """
        Calculate system-level metrics:
        - Item count
        - Average score %
        - Weighted score (using system weight)
        """
        # Get all assessment items for this building and system
        items = AssessmentItem.query.join(Assessment).filter(
            Assessment.building_id == building_id,
            AssessmentItem.system_id == system_id
        ).all()
        
        if not items:
            return None
        
        # Get or create system score record
        sys_score = SystemScore.query.filter_by(
            building_id=building_id, 
            system_id=system_id
        ).first()
        
        if not sys_score:
            sys_score = SystemScore(
                building_id=building_id,
                system_id=system_id,
                weight=0.0
            )
            db.session.add(sys_score)
        
        # Calculate metrics
        sys_score.item_count = len(items)
        
        # Average score %
        valid_items = [i for i in items if i.score_percent is not None]
        if valid_items:
            sys_score.score_percent = sum(i.score_percent for i in valid_items) / len(valid_items)
        else:
            sys_score.score_percent = 0.0
        
        # Calculate weighted score
        sys_score.calculate_weighted_score()
        
        db.session.add(sys_score)
        return sys_score
    
    @staticmethod
    def calculate_overall_building_score(building_id):
        """
        Calculate overall building score
        Formula: Sum(Weighted Scores) / Count(Systems with weights)
        
        Only systems with weight > 0 contribute to score
        """
        system_scores = SystemScore.query.filter_by(building_id=building_id).all()
        
        if not system_scores:
            return 0.0
        
        # Only consider systems with weights
        weighted_systems = [s for s in system_scores if s.weight > 0]
        if not weighted_systems:
            return 0.0
        
        total_weighted_score = sum(s.weighted_score or 0 for s in weighted_systems)
        count = len(weighted_systems)
        
        overall_score = total_weighted_score / count if count > 0 else 0.0
        return round(overall_score, 2)
    
    @staticmethod
    def calculate_compliance_percentage(building_id):
        """
        Calculate compliance %
        Formula: Count(Status='Yes' or 'Partial') / Total Count * 100
        """
        from models import ComplianceChecklist
        
        # Get the compliance checklist for this building
        checklist = ComplianceChecklist.query.filter_by(building_id=building_id).first()
        if not checklist:
            return 0.0
        
        # Get all compliance items for this checklist
        items = ComplianceItem.query.filter_by(checklist_id=checklist.id).all()
        
        if not items:
            return 0.0
        
        compliant = sum(1 for item in items if item.status in ['Yes', 'Partial'])
        return round((compliant / len(items)) * 100, 2)
    
    @staticmethod
    def get_status_distribution(building_id):
        """
        Get count of items by status
        Returns: {Open: count, In Progress: count, Closed: count, Verified: count}
        """
        items = AssessmentItem.query.join(Assessment).filter(
            Assessment.building_id == building_id
        ).all()
        
        distribution = {
            'Open': 0,
            'In Progress': 0,
            'Closed': 0,
            'Verified': 0
        }
        
        for item in items:
            if item.status in distribution:
                distribution[item.status] += 1
        
        return distribution
    
    @staticmethod
    def get_priority_distribution(building_id):
        """
        Get count of items by priority (P1-P4)
        """
        items = AssessmentItem.query.join(Assessment).filter(
            Assessment.building_id == building_id
        ).all()
        
        distribution = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
        
        for item in items:
            if item.priority in distribution:
                distribution[item.priority] += 1
        
        return distribution
    
    @staticmethod
    def get_risk_distribution(building_id):
        """
        Get count of items by risk criticality level
        Maps criticality (0-5) to risk levels
        0-1: Acceptable, 1-2: Low, 2-3: Medium, 3-4: High, 4-5: Critical
        """
        items = AssessmentItem.query.join(Assessment).filter(
            Assessment.building_id == building_id
        ).all()
        
        distribution = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0,
            'Acceptable': 0
        }
        
        for item in items:
            risk = item.risk_criticality or 0
            if risk >= 4:
                distribution['Critical'] += 1
            elif risk >= 3:
                distribution['High'] += 1
            elif risk >= 2:
                distribution['Medium'] += 1
            elif risk >= 1:
                distribution['Low'] += 1
            else:
                distribution['Acceptable'] += 1
        
        return distribution
    
    @staticmethod
    def get_capa_distribution(building_id):
        """
        Get count of CAPAs by status
        """
        capas = CAPARegister.query.filter_by(building_id=building_id).all()
        
        distribution = {
            'Open': 0,
            'In Progress': 0,
            'Closed': 0,
            'Verified': 0,
            'Overdue': 0
        }
        
        for capa in capas:
            # Check if overdue
            if capa.is_overdue():
                distribution['Overdue'] += 1
            elif capa.status in distribution:
                distribution[capa.status] += 1
        
        return distribution
    
    @staticmethod
    def get_test_results_distribution(building_id):
        """
        Get count of tests by result
        """
        tests = TestRegister.query.filter_by(building_id=building_id).all()
        
        distribution = {
            'Pass': 0,
            'Fail': 0,
            'Need Attention': 0,
            'Not Tested': 0
        }
        
        for test in tests:
            if test.result in distribution:
                distribution[test.result] += 1
            else:
                distribution['Not Tested'] += 1
        
        return distribution
    
    @staticmethod
    def compute_executive_dashboard(building_id):
        """
        Compute all metrics for executive dashboard
        Called after each major change (item added/updated, weight changed, etc)
        """
        building = Building.query.get(building_id)
        if not building:
            return None
        
        # Get or create dashboard summary
        dashboard = ExecutiveDashboardSummary.query.filter_by(building_id=building_id).first()
        if not dashboard:
            dashboard = ExecutiveDashboardSummary(building_id=building_id)
            db.session.add(dashboard)
        
        # Get all assessment items
        items = AssessmentItem.query.join(Assessment).filter(
            Assessment.building_id == building_id
        ).all()
        
        # Overall score
        dashboard.overall_building_score = CalculationService.calculate_overall_building_score(building_id)
        
        # Compliance %
        dashboard.overall_compliance_percent = CalculationService.calculate_compliance_percentage(building_id)
        
        # Threshold check
        dashboard.threshold_pass = dashboard.overall_building_score >= building.system_threshold_percent
        
        # Status distribution
        status_dist = CalculationService.get_status_distribution(building_id)
        dashboard.total_assessment_items = len(items)
        dashboard.items_open = status_dist['Open']
        dashboard.items_in_progress = status_dist['In Progress']
        dashboard.items_closed = status_dist['Closed']
        dashboard.items_verified = status_dist['Verified']
        
        # Risk distribution
        risk_dist = CalculationService.get_risk_distribution(building_id)
        dashboard.risk_critical = risk_dist['Critical']
        dashboard.risk_high = risk_dist['High']
        dashboard.risk_medium = risk_dist['Medium']
        dashboard.risk_low = risk_dist['Low']
        dashboard.risk_acceptable = risk_dist['Acceptable']
        
        # CAPA distribution
        capa_dist = CalculationService.get_capa_distribution(building_id)
        dashboard.capa_open = capa_dist['Open']
        dashboard.capa_in_progress = capa_dist['In Progress']
        dashboard.capa_closed = capa_dist['Closed'] + capa_dist['Verified']  # Combine verified with closed
        dashboard.capa_overdue = capa_dist['Overdue']
        
        # Test results distribution
        test_dist = CalculationService.get_test_results_distribution(building_id)
        dashboard.test_pass = test_dist['Pass']
        dashboard.test_fail = test_dist['Fail']
        dashboard.test_need_attention = test_dist['Need Attention']
        
        # Generate observations
        dashboard.notes_observations = CalculationService.generate_observations(dashboard, building)
        
        db.session.add(dashboard)
        return dashboard
    
    @staticmethod
    def generate_observations(dashboard, building):
        """
        Generate automated narrative observations
        """
        observations = []
        
        # Score observation
        if dashboard.overall_building_score:
            status = "PASS" if dashboard.threshold_pass else "FAIL"
            observations.append(
                f"Overall Building Score: {dashboard.overall_building_score:.1f}% - {status} "
                f"(Threshold: {building.system_threshold_percent}%)"
            )
        
        # Risk observation
        if dashboard.risk_critical > 0:
            observations.append(
                f"ALERT: {dashboard.risk_critical} critical risk items identified requiring immediate attention"
            )
        
        # CAPA observation
        if dashboard.capa_overdue > 0:
            observations.append(
                f"WARNING: {dashboard.capa_overdue} overdue CAPAs require attention"
            )
        
        # Compliance observation
        if dashboard.overall_compliance_percent:
            observations.append(
                f"Compliance: {dashboard.overall_compliance_percent:.1f}% of regulatory requirements met"
            )
        
        # Status observation
        if dashboard.items_verified > 0:
            pct = (dashboard.items_verified / dashboard.total_assessment_items * 100) if dashboard.total_assessment_items > 0 else 0
            observations.append(
                f"Closure Progress: {dashboard.items_verified}/{dashboard.total_assessment_items} items verified ({pct:.0f}%)"
            )
        
        return '. '.join(observations)
