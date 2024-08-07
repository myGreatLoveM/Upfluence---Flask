from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import Admin, Influencer, Brand, AdminActivityLog, User, Campaign, Engagement
from extensions import db

admin = Blueprint('admin', __name__)

@admin.route('/')
@admin.route('/dashboard', methods=['GET'])
def dashboard():
    activities = AdminActivityLog.query.all()
    infu_list = Influencer.query.all()
    new_infu = [infu for infu in infu_list if not infu.is_approved]
    return render_template('admin/admin_dashboard.html', new_infu=new_infu, activities=activities)


@admin.route('/brands')
def brands():
    page = request.args.get('page', default=1, type=int)
    brands = Brand.query.filter_by(
        is_approved=True, is_blocked=False).paginate(page=page, per_page=6)
    return render_template('admin/admin_brands.html', brands=brands)


@admin.route('/brands/<int:brand_id>')
def get_brand(brand_id):
    brand = Brand.query.filter_by(
        id=brand_id, is_approved=True, is_blocked=False).first()
    return render_template('admin/admin_brand_detail.html', brand_id=brand_id, brand=brand)


@admin.route('/influencers')
def influencers():
    page = request.args.get('page', default=1, type=int)
    influencers = Influencer.query.filter_by(
        is_approved=True, is_blocked=False).paginate(page=page, per_page=6)
    return render_template('admin/admin_influencers.html', influencers=influencers)


@admin.route('/influencers/<int:infu_id>')
def get_influencer(infu_id):
    influencer = Influencer.query.filter_by(
        id=infu_id, is_approved=True, is_blocked=False).first()
    return render_template('admin/admin_infu_detail.html', infu_id=infu_id, influencer=influencer)


@admin.route('/approvals/brands', methods=['GET'])
def pending_brands():
    page = request.args.get('page', default=1, type=int)
    brands = Brand.query.filter_by(
        is_approved=False, is_blocked=False).paginate(page=page, per_page=6)
    return render_template('admin/pending_brands.html', brands=brands)


@admin.route('/approvals/brands/<int:brand_id>', methods=['GET'])
def handle_pending_brand(brand_id):
    admin = Admin.query.first()
    brand = Brand.query.filter_by(
        id=brand_id, is_approved=False, is_blocked=False).first()
    approve = request.args('approve')

    if approve:
        if approve == 'y':
            brand.is_approved = True
            activity = AdminActivityLog(activity=f'admin approved brand {brand.name} with id {brand.id}')
            admin.activities.append(activity)
            flash(f'brand {brand.name} is approved', category='success')
        elif approve == 'n':
            brand.is_blocked = True
            activity = AdminActivityLog(activity_description=f'admin blocked brand {brand.name} with id {brand.id}')
            admin.activities.append(activity)
            flash(f'brand {brand.name} is blocked', category='error')
        db.session.commit()
    return redirect(url_for('admin.pending_brands'))


@admin.route('/approvals/influencers', methods=['GET'])
def pending_influencers():
    page = request.args.get('page', default=1, type=int)
    influencers = Influencer.query.filter_by(is_approved=False, is_blocked=False).paginate(page=page, per_page=6)
    return render_template('admin/pending_influencers.html', influencers=influencers)


@admin.route('/approvals/influencers/<int:infu_id>', methods=['GET'])
def handle_pending_influencer(infu_id):
    admin = Admin.query.first()
    influencer = Influencer.query.filter_by(
        id=infu_id, is_approved=False, is_blocked=False).first()
    approve = request.args('approve')

    if approve:
        if approve == 'y':
            influencer.is_approved = True
            activity = AdminActivityLog(activity=f'admin approved influencer {influencer.name} with id {influencer.id}')
            admin.activities.append(activity)
            flash(f'Influencer {influencer.name} is approved', category='success')
        elif approve == 'n':
            influencer.is_blocked = True
            activity = AdminActivityLog(activity_description=f'admin blocked influencer {influencer.name} with id {influencer.id}')
            admin.activities.append(activity)
            flash(f'Influencer {influencer.name} is blocked', category='error')
        db.session.commit()
    return redirect(url_for('admin.pending_influencers'))


@admin.route('/approvals/campaigns')
def pending_campaigns():
    page = request.args.get('page', default=1, type=int)
    campaigns = Campaign.query.filter_by(is_approved=False, is_blocked=False).paginate(page=page, per_page=6)
    return render_template('admin/admin_campaigns.html', campaigns=campaigns)


@admin.route('/approvals/campaigns/<int:campaign_id>')
def handle_pending_campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id, is_approved=False, is_blocked=False).first()
    approve = request.args('approve')

    if approve:
        if approve == 'y':
            campaign.is_approved = True
            activity = AdminActivityLog(activity=f'admin approved campaign {campaign.name} with id {campaign.id}')
            admin.activities.append(activity)
            flash(f'campaign {campaign.name} is approved', category='success')
        elif approve == 'n':
            campaign.is_blocked = True
            activity = AdminActivityLog(activity_description=f'admin blocked campaign {campaign.name} with id {campaign.id}')
            admin.activities.append(activity)
            flash(f'campaign {campaign.name} is blocked', category='error')
        db.session.commit() 
    return redirect(url_for('admin.pending_campaigns'))


@admin.route('/approvals/engagements')
def pending_engagements():
    page = request.args.get('page', default=1, type=int)
    engagements = Engagement.query.filter_by(is_approved=False, is_blocked=False).paginate(page=page, per_page=6)
    return render_template('admin/admin_engagements.html', engagements=engagements)


@admin.route('/approvals/engagements/<int:engag_id>')
def handle_pending_engagement(engag_id):
    engagement = Engagement.query.filter_by(id=engag_id, is_approved=False, is_blocked=False).first()
    approve = request.args('approve')

    if approve:
        if approve == 'y':
            engagement.is_approved = True
            activity = AdminActivityLog(activity=f'admin approved engagement {engagement.name} with id {engagement.id}')
            admin.activities.append(activity)
            flash(f'engagement {engagement.name} is approved', category='success')
        elif approve == 'n':
            engagement.is_blocked = True
            activity = AdminActivityLog(activity_description=f'admin blocked engagement {engagement.name} with id {engagement.id}')
            admin.activities.append(activity)
            flash(f'engagement {engagement.name} is blocked', category='error')
        db.session.commit() 
    return redirect(url_for('admin.pending_engagements'))