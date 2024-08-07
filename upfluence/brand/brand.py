from flask import Blueprint, request, render_template, redirect, url_for, session, flash, abort, make_response
from flask_login import login_required, current_user, logout_user
from models import Influencer, Brand, Campaign, Proposal, Sponsorship, Engagement, Payment, Review
from forms import CampaignForm
from extensions import db, csrf
from decorators import brand_required
from helpers import clean_arg, paginate

brand = Blueprint('brand', __name__)


@brand.route('<int:brand_id>/')
@brand.route('<int:brand_id>/dashboard')
def dashboard(brand_id):
    return render_template('brand/brand_dashboard.html', brand_id=brand_id)


@brand.route('<int:brand_id>/add-budget', methods=['POST'])
@csrf.exempt
def add_budget(brand_id):
    amount = request.form.get('amount')
    brand = Brand.query.filter_by(id=brand_id).first()
    brand.total_budget += int(amount)
    db.session.commit()
    flash('Added Budget successfully', category='success')
    return redirect(url_for('brand.dashboard', brand_id=brand_id))


@brand.route('<int:brand_id>/campaigns', methods=['GET'])
@csrf.exempt
def campaigns(brand_id):
    campaign_type = clean_arg(request.args.get('filter'))
    sort_type = clean_arg(request.args.get('sort'))
    page = request.args.get('page', default=1, type=int)
    per_page = 8

    form = CampaignForm()
    session['form'] = form.csrf_token
    brand = Brand.query.filter_by(id=brand_id).first()
    total_budget = brand.total_budget
    campaigns = None

    if campaign_type:
        if campaign_type in 'public':
            if sort_type:
                if sort_type in 'low-high':
                    campaigns = Campaign.query.filter_by(brand_id=brand_id, is_public=True).order_by(
                        Campaign.allocated_budget).paginate(page=page, per_page=per_page)
                elif sort_type in 'high-low':
                    campaigns = Campaign.query.filter_by(brand_id=brand_id, is_public=True).order_by(
                        Campaign.allocated_budget.desc()).paginate(page=page, per_page=per_page)
                elif sort_type in 'first-created':
                    campaigns = Campaign.query.filter_by(brand_id=brand_id, is_public=True).order_by(
                        Campaign.id).paginate(page=page, per_page=per_page)
            else:
                campaigns = Campaign.query.filter_by(brand_id=brand_id, is_public=True).order_by(
                    Campaign.id.desc()).paginate(page=page, per_page=per_page)
        elif campaign_type in 'private':
            if sort_type:
                if sort_type in 'low-high':
                    campaigns = Campaign.query.filter_by(brand_id=brand_id, is_public=False).order_by(
                        Campaign.allocated_budget).paginate(page=page, per_page=per_page)
                elif sort_type in 'high-low':
                    campaigns = Campaign.query.filter_by(brand_id=brand_id, is_public=False).order_by(
                        Campaign.allocated_budget.desc()).paginate(page=page, per_page=per_page)
                elif sort_type in 'first-created':
                    campaigns = Campaign.query.filter_by(brand_id=brand_id, is_public=False).order_by(
                        Campaign.id).paginate(page=page, per_page=per_page)
            else:
                campaigns = Campaign.query.filter_by(brand_id=brand_id, is_public=False).order_by(
                    Campaign.id.desc()).paginate(page=page, per_page=per_page)
    else:
        if sort_type:
            if sort_type in 'high-low':
                campaigns = Campaign.query.filter_by(brand_id=brand_id).order_by(
                    Campaign.allocated_budget.desc()).paginate(page=page, per_page=per_page)
            elif sort_type in 'low-high':
                campaigns = Campaign.query.filter_by(brand_id=brand_id).order_by(
                    Campaign.allocated_budget).paginate(page=page, per_page=per_page)
            elif sort_type in 'first-created':
                campaigns = Campaign.query.filter_by(brand_id=brand_id).order_by(
                    Campaign.id).paginate(page=page, per_page=per_page)
        else:
            campaigns = Campaign.query.filter_by(brand_id=brand_id).order_by(
                Campaign.id.desc()).paginate(page=page, per_page=per_page)

    if (page > campaigns.pages):
        abort(404)

    return render_template('brand/brand_campaigns.html', brand_id=brand_id, form=form, campaigns=campaigns, total_budget=total_budget, filter=campaign_type, sort=sort_type)


@brand.route('<int:brand_id>/campaigns/create', methods=['POST'])
@csrf.exempt
def create_campaign(brand_id):
    form = CampaignForm()
    form.csrf_token = session.get('csrf_token')
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        visibility = form.visibility.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        end_date = form.end_date.data
        allocated_budget = form.allocate_budget.data

        session.pop('csrf_token', None)

        brand = db.session.query(Brand).filter_by(id=brand_id).first()

        # if(allocated_budget >= brand.total_budget):
        #     flash('Allocated budget exceeded total budget', category='error')
        #     return redirect(url_for('brand.campaigns', brand_id=brand_id))
        # else:
        #     brand.total_budget -= allocated_budget

        if visibility.lower().strip() == 'public':
            is_public = True
        else:
            is_public = False
        brand = Brand.query.filter_by(id=brand_id).first()
        new_campaign = Campaign(name=name.title(), description=description,
                                is_public=is_public, start_date=start_date, end_date=end_date, allocated_budget=int(allocated_budget))
        brand.campaigns.append(new_campaign)
        db.session.add(new_campaign)
        db.session.commit()
        flash('Campaign created successfully', category='success')
        return redirect(url_for('brand.campaigns', brand_id=brand_id))
    else:
        flash('Couldnt create a new campaign', category='error')
    return {}


@brand.route('<int:brand_id>/campaigns/<int:campaign_id>', methods=['GET'])
def campaign_detail(brand_id, campaign_id):
    campaign = Campaign.query.filter_by(
        id=campaign_id, brand_id=brand_id).first()

    return render_template('brand/brand_campaign_detail.html', brand_id=brand_id, campaign_id=campaign_id, campaign=campaign)


@brand.route('<int:brand_id>/campaigns/<int:campaign_id>/set-cookie', methods=['GET'])
def set_cookie(brand_id, campaign_id):
    print(campaign_id)
    resp = make_response({"message"})
    resp.set_cookie('campaign_id', campaign_id, )
    return resp

# @app.route('/cookies')
# def all_cookies():
#     cookies = request.cookies
#     print(cookies)
#     return render_template('base.html')


@brand.route('<int:brand_id>/search', methods=['GET', 'POST'])
@csrf.exempt
def search_influencer(brand_id):
    campaign_id = request.args.get('campaign_id')
    brand = Brand.query.filter_by(id=brand_id).first()
    brand_campaigns = brand.campaigns

    for campaign in brand_campaigns:
        campaign.sponsorships.filter()

    # brand_sponsorships = brand.sponsorships
    # prev_colab = []
    # for sponsorship in brand_sponsorships:
    #     if sponsorship.campaign_id != campaign_id:
    #         prev_colab.append(sponsorship.influencer)

    # db.session.query(Sponsorship).filter_by(brand_id=brand.id).group_by(Sponsorship.influencer)

    if request.method == 'POST':
        search_by = request.form.get('search-by')
        keyword = request.form.get('keyword')
        influencers = Influencer.query.filter_by(
            name=keyword.strip().title(), is_approved=True, is_blocked=False).all()
        print(influencers)
    return render_template('brand/search_influencer.html', brand_id=brand_id, campaign_id=campaign_id, campaigns=campaigns, influencers=influencers)


@brand.route('<int:brand_id>/influencer/<int:influencer_id>', methods=['GET'])
def show_influencer_profile(brand_id, influencer_id):
    campaign_id = request.args.get('campaign_id')
    influencer = Influencer.query.filter_by(id=influencer_id).first()
    return render_template('brand/influencer_profile.html', brand_id=brand_id, campaign_id=campaign_id, influencer_id=influencer_id, influencer=influencer)


@brand.route('<int:brand_id>/campaigns/<int:campaign_id>/request/<int:influencer_id>', methods=['POST'])
@csrf.exempt
def request_influencer(brand_id, campaign_id, influencer_id):
    amount = request.form.get('amount')
    message = request.form.get('message')
    requirements = request.form.get('requirements')

    new_proposal = Proposal(campaign_id=campaign_id, influencer_id=influencer_id, original_amount=int(
        amount), message=message, requirements=requirements)
    influencer = Influencer.query.get_or_404(influencer_id)
    influencer.proposals.append(new_proposal)
    db.session.add(new_proposal)
    db.session.commit()
    return redirect(url_for('brand.campaigns', brand_id=brand_id))


@brand.route('<int:brand_id>/proposals')
def proposals(brand_id):
    filter_by_status = clean_arg(request.args.get('filter_by_status'))
    filter_by_campaign_id = clean_arg(request.args.get('filter_by_campaign'))
    page = request.args.get('page', default=1, type=int)
    per_page = 2

    brand = Brand.query.filter_by(id=brand_id).first()
    brand_campaigns = brand.campaigns
    brand_proposals = []

    for campaign in brand_campaigns:
        if filter_by_status:
            if filter_by_status in 'accepted':
                brand_proposals.extend(
                    campaign.proposals.filter_by(status='accepted').all())
            elif filter_by_status in 'rejected':
                brand_proposals.extend(
                    campaign.proposals.filter_by(status='rejected').all())
            elif filter_by_status in 'pending':
                brand_proposals.extend(
                    campaign.proposals.filter_by(status='pending').all())
        else:
            brand_proposals.extend(campaign.proposals.all())

    if filter_by_campaign_id:
        brand_proposals = [proposal for proposal in brand_proposals if proposal.campaign_id == int(
            filter_by_campaign_id)]

    brand_proposals.sort(reverse=True, key=lambda x: x.id)

    paginated_proposals, total, total_pages, start, end = paginate(
        brand_proposals, page, per_page)

    return render_template('brand/brand_proposals.html', brand_id=brand_id, proposals=paginated_proposals, campaigns=brand_campaigns, filter_by_status=filter_by_status, filter_by_campaign=filter_by_campaign_id, curr_page=page, total=total, total_pages=total_pages, start=start, end=end)


@brand.route('<int:brand_id>/sponsorships')
def sponsorships(brand_id):
    page = request.args.get('page', default=1, type=int)
    per_page = 1
    brand = Brand.query.filter_by(id=brand_id).first()
    brand_campaigns = brand.campaigns
    brand_sponsorships = []

    for campaign in brand_campaigns:
        brand_sponsorships.extend(campaign.sponsorships.all())

    brand_sponsorships.sort(reverse=True, key=lambda x: x.id)

    paginated_sponsorships, total, total_pages, start, end = paginate(
        brand_sponsorships, page, per_page)

    return render_template('brand/brand_sponsorships.html', brand_id=brand_id, sponsorships=paginated_sponsorships, campaigns=brand_campaigns, curr_page=page, total=total, total_pages=total_pages, start=start, end=end)


@brand.route('<int:brand_id>/engagements')
def engagements(brand_id):
    page = request.args.get('page', default=1, type=int)
    per_page = 1
    brand = Brand.query.filter_by(id=brand_id).first()
    brand_campaigns = brand.campaigns
    brand_engagements = []

    for campaign in brand_campaigns:
        brand_engagements.extend(campaign.sponsorships.all())

    brand_engagements.sort(reverse=True, key=lambda x: x.id)

    paginated_engagements, total, total_pages, start, end = paginate(
        brand_engagements, page, per_page)

    return render_template('brand/brand_sponsorships.html', brand_id=brand_id, sponsorships=paginated_engagements, campaigns=brand_campaigns, curr_page=page, total=total, total_pages=total_pages, start=start, end=end)


@brand.route('<int:brand_id>/payments')
def payments(brand_id):
    page = request.args.get('page', default=1, type=int)
    per_page = 1
    brand = Brand.query.filter_by(id=brand_id).first()
    brand_campaigns = brand.campaigns
    brand_payments = []

    for campaign in brand_campaigns:
        brand_payments.extend(campaign.sponsorships.all())

    brand_payments.sort(reverse=True, key=lambda x: x.id)

    paginated_payments, total, total_pages, start, end = paginate(
        brand_payments, page, per_page)

    return render_template('brand/brand_payments.html', brand_id=brand_id, payments=paginated_payments, campaigns=brand_campaigns, curr_page=page, total=total, total_pages=total_pages, start=start, end=end)


@brand.route('<int:brand_id>/profile')
def profile(brand_id):
    brand = Brand.query.filter_by(id=brand_id).first()
    brand_profile = brand.user.profile
    return render_template('brand/brand_profile.html', brand_id=brand_id, profile=brand_profile)
