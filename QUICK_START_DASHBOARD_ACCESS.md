# Quick Start Guide - Dashboard Access & Profile Management

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask with extensions (already installed)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Database Setup
The database models are automatically created on application startup:

```bash
# Just run the app - tables will be created automatically
python app.py
# or
flask run
```

## 👤 User Guide

### 1. **Accessing Your Profile**

After logging in:
1. Click **Profile** in the navigation bar
2. View all your information in organized cards:
   - Account Information (email, name, phone, etc.)
   - Dashboard Access status
   - Pending Profile Changes
   - Your Preferences (theme, notifications)

### 2. **Editing Your Profile**

On your profile page:
1. Click **Edit Profile** button
2. Update your information:
   - **Full Name** (requires admin approval)
   - **Phone** (requires admin approval)
   - **Department** (with autocomplete suggestions)
   - **Job Title** (with autocomplete suggestions)
   - **Office Location** (with autocomplete suggestions)
   - **Theme** preference
   - **Notifications** setting
3. Click **Update Profile**
4. See confirmation message

**Note**: Changes to name and phone require admin approval. You'll see them listed as "Pending Review" until approved.

### 3. **Requesting Dashboard Access**

To view the Power BI dashboard:
1. Click **Profile** in navigation
2. Scroll to "Dashboard Access" section
3. Click **Request Access** button
4. Fill in your reason for needing access (min 10 characters)
5. Check the confirmation box
6. Click **Request Dashboard Access**
7. Wait for admin approval (you'll see "Pending Review" status)
8. Once approved, click **View Dashboard**

### 4. **Viewing the Dashboard**

After your access is approved:
1. Click **Profile** → **View Dashboard**, OR
2. Go to `/dashboard` directly

You'll see:
- Embedded Power BI Building Assessment Report
- Quick action buttons for navigation
- Dashboard features information

## 🔑 Admin Guide

### Accessing Admin Panel

Only users with **admin role** can access the admin panel:
1. Log in with admin account (demo@example.com / demo123)
2. Look for **Admin** link in navigation bar
3. Click to access admin dashboard

### Admin Dashboard Overview

The admin panel shows three main sections:

#### 📊 Quick Stats
- Pending Access Requests
- Pending Profile Changes  
- Users with Dashboard Access

#### 1️⃣ **Dashboard Access Requests**

**View Pending Requests:**
- See user email, full name, and request date
- See request status (Pending)

**Approve a Request:**
1. Find the request
2. Click **Approve** button
3. User is added to dashboard access list
4. User receives permission

**Reject a Request:**
1. Find the request
2. Click **Reject** button
3. Modal appears asking for rejection reason
4. Enter reason (e.g., "User not authorized yet")
5. Click **Reject Request**
6. User sees rejection with your reason

#### 2️⃣ **Profile Change Requests**

**View Pending Changes:**
- See user requesting change
- See field being changed (Full Name, Phone, etc.)
- See current value vs. requested value side-by-side

**Approve a Change:**
1. Review the change
2. Click **Approve** button
3. User's profile is updated automatically
4. Change marked as "Approved"

**Reject a Change:**
1. Review the change
2. Click **Reject** button
3. Enter reason for rejection
4. User sees rejection with your reason

#### 3️⃣ **Approved Users List**

View all users who have dashboard access:
- User name/email
- Join date
- Active dashboard access status

### Best Practices for Admins

1. **Review Requests Regularly** - Check admin dashboard daily
2. **Provide Reasons** - Always include reason when rejecting
3. **Communicate** - Let users know status via rejections
4. **Audit Trail** - All approvals are timestamped and logged
5. **Security** - Only approve for authorized personnel

## 🎨 UI Features

### Smooth Animations
- **Page Load**: Content fades in smoothly
- **Card Transitions**: Cards appear sequentially
- **Hover Effects**: Buttons and cards lift on hover
- **Status Changes**: Smooth badge color transitions
- **Form Focus**: Input fields highlight when focused

### Autocomplete Dropdowns

When editing profile, certain fields have autocomplete:
1. Start typing in the field
2. Suggestions appear below
3. Click a suggestion or continue typing
4. Suggestions filter as you type
5. Click away to close suggestions

Available autocomplete fields:
- Department (fetches from existing data)
- Job Title (fetches from existing data)
- Office Location (fetches from existing data)

### Responsive Design

All pages work on any device:
- **Mobile**: Single column, touch-friendly buttons
- **Tablet**: 2-column layouts when appropriate
- **Desktop**: Full layouts with side-by-side comparisons

## 🔒 Security & Privacy

### Access Control
- Only authenticated users can access profiles
- Dashboard access requires explicit admin approval
- Admin panel restricted to admin users only
- All profile changes logged with timestamps

### Data Protection
- Passwords hashed with Werkzeug
- CSRF protection on all forms
- Secure session management
- No sensitive data in logs

## 📱 Mobile Access

### Optimized for Mobile
- Touch-friendly buttons and links
- Reduced animation complexity
- Optimized form sizes
- Mobile-first responsive design

### Best Experience
- Desktop/Laptop: Full feature set with all animations
- Tablet: Optimized for 2-column layouts
- Mobile: Single column, gesture-friendly

## 🆘 Troubleshooting

### Issue: Profile page shows no changes
**Solution**: Refresh the page or clear browser cache

### Issue: Autocomplete not showing suggestions
**Solution**: 
- Make sure other users exist with that data
- Start typing at least 2 characters
- Check browser console for errors

### Issue: Admin panel not visible
**Solution**:
- Make sure you're logged in as admin
- Check your user role in database
- Try logging out and back in

### Issue: Dashboard not loading
**Solution**:
- Make sure access is approved
- Check internet connection
- Power BI may be temporarily down
- Try refreshing the page

## 📊 Database Structure

### Three New Tables

**user_profiles**
- Links to users table
- Stores additional profile info
- Tracks dashboard permissions

**dashboard_access_requests**
- Stores access requests
- Tracks approval status
- Records who approved and when

**profile_change_requests**
- Stores requested changes
- Tracks old and new values
- Records approval/rejection

## 🔄 Common Workflows

### Workflow 1: New Employee Getting Dashboard Access
```
1. Employee logs in
2. Employee requests dashboard access
3. Admin reviews request (sees "Pending")
4. Admin approves
5. Employee checks profile - sees "Approved"
6. Employee views dashboard
```

### Workflow 2: Updating Contact Information
```
1. Employee edits profile
2. Changes department (approved immediately)
3. Changes phone (creates change request)
4. Admin reviews phone change
5. Admin approves
6. Employee's phone updated in profile
```

### Workflow 3: Rejecting Inappropriate Request
```
1. Admin sees access request from unauthorized user
2. Admin clicks "Reject"
3. Admin provides reason: "Not authorized for this data"
4. User sees rejection with reason
5. User cannot request again immediately
```

## 💡 Tips & Tricks

### For Users
- Complete your profile fully before requesting dashboard
- Use full email addresses and clear names
- Keep phone number updated
- Check profile regularly for pending approvals

### For Admins
- Process requests in batches
- Keep rejection reasons clear and professional
- Review audit trail weekly
- Monitor for unusual access patterns

## 🎯 Performance Notes

- Autocomplete loads data on first focus (lazy loading)
- Animations optimized for 60 FPS
- Mobile animations reduced for performance
- Database queries use indexes for speed
- Bootstrap CDN for fast CSS loading

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Check browser console (F12) for JavaScript errors
4. Review server logs for database errors
5. Contact system admin at demo@example.com

---

**Last Updated**: January 5, 2026  
**Version**: 1.0.0
