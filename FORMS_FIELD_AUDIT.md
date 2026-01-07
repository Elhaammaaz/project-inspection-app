# Form Fields Audit & Fixes

## Purpose
This document ensures all form fields match between:
- `forms.py` - Form field definitions
- `*.html` templates - Form field rendering
- `models.py` - Database fields (related fields)

## Form-by-Form Audit

### 1. LoginForm
**Location:** `forms.py` lines 11-14
**Fields Defined:**
- `username` - StringField
- `password` - PasswordField
- `submit` - SubmitField

**Template Used:** `templates/login.html`
**Expected Fields in Template:**
- ✅ `form.username` - CORRECT
- ✅ `form.password` - CORRECT
- ✅ `form.submit` - CORRECT

**Status:** ✅ FIXED

---

### 2. RegistrationForm
**Location:** `forms.py` lines 17-30
**Fields Defined:**
- `username` - StringField
- `email` - StringField
- `password` - PasswordField
- `password_confirm` - PasswordField (not `confirm_password`)
- `submit` - SubmitField

**Template Used:** `templates/register.html`
**Expected Fields in Template:**
- ✅ `form.username` - CORRECT
- ✅ `form.email` - CORRECT
- ✅ `form.password` - CORRECT
- ✅ `form.password_confirm` - CORRECT (fixed)
- ✅ `form.submit` - CORRECT

**Status:** ✅ FIXED

---

### 3. ProjectForm
**Location:** `forms.py` lines 33-79
**Fields Defined:**
- `project_name` - StringField
- `city` - StringField
- `address` - StringField
- `gps_coordinates` - StringField
- `building_type` - SelectField
- `primary_use` - SelectField
- `gross_built_area` - FloatField
- `num_floors` - IntegerField
- `construction_year` - IntegerField
- `last_major_renovation` - DateField
- `estimated_lifetime` - IntegerField
- `planned_retirement_year` - IntegerField
- `current_year` - IntegerField
- `system_threshold` - FloatField
- `inspection_date` - DateField
- `fm_contractor` - StringField
- `submit` - SubmitField

**Template Used:** `templates/form.html` and `templates/inspection_form.html`
**Notes:** ProjectForm is used for both new projects and project editing

**Status:** ✅ NEEDS REVIEW

---

### 4. AssessmentItemForm
**Location:** `forms.py` lines 82-107
**Fields Defined:**
- `rate` - IntegerField (1-5 dropdown)
- `item_weight` - FloatField (dropdown with standard values)
- `priority` - SelectField (P1-P4)
- `status` - SelectField (Open/In Progress/Closed/Verified)
- `evidence_type` - SelectField
- `responsibility` - SelectField
- `due_date` - DateField
- `remarks` - TextAreaField
- `submit` - SubmitField

**Status:** ✅ NEEDS REVIEW

---

### 5. ComplianceItemForm
**Location:** `forms.py` lines 151-167
**Fields Defined:**
- `compliance_area` - StringField (read-only)
- `description` - TextAreaField (read-only)
- `status` - SelectField
- `remarks` - TextAreaField
- `submit` - SubmitField

**Status:** ✅ NEEDS REVIEW

---

### 6. TestRecordForm
**Location:** `forms.py` lines 172-193
**Fields Defined:**
- `test_code` - StringField (read-only)
- `test_description` - StringField (read-only)
- `system` - StringField (read-only)
- `test_date` - DateField
- `test_result` - SelectField (Pass/Fail)
- `conducted_by` - StringField
- `remarks` - TextAreaField
- `submit` - SubmitField

**Status:** ✅ NEEDS REVIEW

---

### 7. CAPARecordForm
**Location:** `forms.py` lines 196-226
**Fields Defined:**
- `capa_id` - StringField (read-only)
- `finding_description` - TextAreaField (read-only)
- `root_cause` - TextAreaField (read-only)
- `corrective_action` - TextAreaField
- `responsible_party` - SelectField
- `target_completion_date` - DateField
- `actual_completion_date` - DateField
- `status` - SelectField
- `effectiveness_check` - TextAreaField
- `submit` - SubmitField

**Status:** ✅ NEEDS REVIEW

---

### 8. SystemWeightForm
**Location:** `forms.py` lines 229-237
**Fields Defined:**
- `system_name` - StringField (read-only)
- `weight` - FloatField (0.1-5.0)
- `submit` - SubmitField

**Status:** ✅ NEEDS REVIEW

---

### 9. ExcelUploadForm
**Location:** `forms.py` lines 240-243
**Fields Defined:**
- `excel_file` - FileField
- `submit` - SubmitField

**Status:** ✅ NEEDS REVIEW

---

## Template Mismatch Fixes Applied

### Fixed Issues:
1. ✅ `templates/login.html`: Changed `form.email` → `form.username`
2. ✅ `templates/register.html`: Changed `form.confirm_password` → `form.password_confirm`
3. ✅ `templates/register.html`: Removed `form.full_name` (not in LoginForm/RegistrationForm)
4. ✅ `templates/base.html`: Changed `url_for('index')` → `url_for('landing')`
5. ✅ `templates/404.html`: Changed `url_for('index')` → `url_for('landing')`
6. ✅ `templates/500.html`: Changed `url_for('index')` → `url_for('landing')`

---

## Field Naming Conventions

**Standard Naming Rules (for future templates):**

### Authentication Forms
- LoginForm uses: `username`, `password`
- RegistrationForm uses: `username`, `email`, `password`, `password_confirm`

### Project Forms
- ProjectForm uses: `project_name`, `city`, `address`, `gps_coordinates`, `building_type`, `primary_use`, `gross_built_area`, `num_floors`, `construction_year`, `last_major_renovation`, `estimated_lifetime`, `planned_retirement_year`, `current_year`, `system_threshold`, `inspection_date`, `fm_contractor`

### Assessment Forms
- AssessmentItemForm uses: `rate`, `item_weight`, `priority`, `status`, `evidence_type`, `responsibility`, `due_date`, `remarks`

### Compliance Forms
- ComplianceItemForm uses: `status`, `remarks`

### Test Forms
- TestRecordForm uses: `test_date`, `test_result`, `conducted_by`, `remarks`

### CAPA Forms
- CAPARecordForm uses: `corrective_action`, `responsible_party`, `target_completion_date`, `actual_completion_date`, `status`, `effectiveness_check`

### System Forms
- SystemWeightForm uses: `weight`

---

## How to Avoid This Error in Future

1. **When creating a new form:**
   - Define fields in `forms.py` with exact field names
   - Document the field names in this file

2. **When creating a template:**
   - Check this file for the correct field names
   - Use `form.field_name` exactly as defined in forms.py
   - NEVER use abbreviated or alternative names (e.g., `confirm_password` instead of `password_confirm`)

3. **Testing:**
   - Test every form field renders without UndefinedError
   - Check browser console for any missing form fields

4. **Review Process:**
   - Compare template fields with `forms.py` before deployment
   - Use IDE autocompletion to catch typos

---

## Status Summary

| Form | Login | Register | Project | Assessment | Compliance | Test | CAPA | System | Upload |
|------|-------|----------|---------|------------|-----------|------|------|--------|--------|
| Status | ✅ Fixed | ✅ Fixed | ⏳ Review | ⏳ Review | ⏳ Review | ⏳ Review | ⏳ Review | ⏳ Review | ⏳ Review |

**Last Updated:** January 6, 2026
