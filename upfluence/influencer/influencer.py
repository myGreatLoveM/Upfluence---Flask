from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from decorators import influencer_required
from models import Proposal, Influencer, Sponsorship, Brand, Campaign, Engagement
from extensions import db

influencer = Blueprint('influencer', __name__)

@influencer.route('<int:infu_id>/')
@influencer.route('<int:infu_id>/dashboard')
def dashboard(infu_id):
    return render_template('influencer/infu_dashboard.html', infu_id=infu_id)

@influencer.route('<int:infu_id>/campaigns')
def campaigns(infu_id):
    public_campaigns = Campaign.query.filter_by(is_public=True).all()
    offered_sponsorships = Sponsorship.query.filter_by(influencer_id=infu_id).all()
    active_campaigns = []
    for sponsorship in offered_sponsorships:
        active_campaigns.append(sponsorship.campaign)
    return render_template('influencer/infu_campaigns.html', infu_id=infu_id, public_campaigns=public_campaigns, active_campaigns=active_campaigns)


@influencer.route('<int:infu_id>/proposals')
def proposals(infu_id):
    proposals = Proposal.query.filter_by(influencer_id=infu_id).all()
    return render_template('influencer/infu_proposals.html', infu_id=infu_id, proposals=proposals)


@influencer.route('<int:infu_id>/proposals/<int:proposal_id>')
def handle_proposal(infu_id, proposal_id):
    status = request.args.get('status')
    proposal = Proposal.query.filter_by(id=proposal_id).first()
    influencer = Influencer.query.filter_by(id=infu_id).first()

    if status.strip().lower() == 'accept':
        proposal.status = 'accepted'
        new_sponsorship = Sponsorship(amount=proposal.original_amount)
        proposal.sponsorships.append(new_sponsorship)
        influencer.sponsorships.append(new_sponsorship)
        proposal.campaign.sponsorships.all().append(new_sponsorship)

        db.session.add(new_sponsorship)
        db.session.commit()
    elif status.strip().lower() == 'reject':
        proposal.status = 'rejected'
        db.session.commit()
    else:
        print('negotiate')
        # proposal.status = 'negotiate'
        # proposal.negotiate_amount = request.form.get('amount')
    return redirect(url_for('influencer.proposals', infu_id=infu_id))

@influencer.route('<int:infu_id>/engagements')
def engagements(infu_id):
    engagements = db.session.query(Engagement).filter_by(id=infu_id).all()
    return render_template('influencer/infu_engagements.html', infu_id=infu_id)

@influencer.route('<int:infu_id>/payments')
def payments(infu_id):
    return render_template('influencer/infu_payments.html', infu_id=infu_id)

@influencer.route('<int:infu_id>/sponsorships')
def sponsorships(infu_id):
    return render_template('influencer/infu_sponsorships.html', infu_id=infu_id)

@influencer.route('<int:infu_id>/profile')
def profile(infu_id):
    return render_template('influencer/profile.html', infu_id=infu_id)

# @influencer.route('<int:infu_id>/request/<int:campaign_id>', methods=['POST'])
# def request_public_campaign(infu_id, campaign_id):
#     amount = request.form.get('amount')
#     new_proposal = Proposal(is_public_infu=True,
#                             status='public-request', original_amount=amount)
#     Influencer.query.filter_by(id=infu_id).proposals.append(new_proposal)
#     campaign = Campaign.query.filter_by(
#         id=campaign_id, is_public=True).first()
#     campaign.proposals.append(new_proposal)
#     campaign.brand.proposals.append(new_proposal)    

