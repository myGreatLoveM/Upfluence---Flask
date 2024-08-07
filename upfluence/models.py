from extensions import db
from datetime import datetime
from flask_login import UserMixin


# user
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_influencer = db.Column(db.Boolean, default=False)
    is_brand = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    profile = db.relationship(
        'Profile', uselist=False, lazy=True)
    admin = db.relationship('Admin', uselist=False, lazy=True)
    influencer = db.relationship(
        'Influencer', back_populates='user', uselist=False, lazy=True)
    brand = db.relationship(
        'Brand', back_populates='user', uselist=False, lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(200))
    contact = db.Column(db.String(20))
    location = db.Column(db.String(50))
    website = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<Profile {self.user.username}>'

# admin


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    activities = db.relationship('AdminActivityLog')

    def __repr__(self):
        return f'<Admin>'


class AdminActivityLog(db.Model):
    __tablename__ = 'admin_activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    activity = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

# influencer
class Influencer(db.Model):
    __tablename__ = 'influencers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)  # FK
    name = db.Column(db.String(50), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)  # admin
    is_blocked = db.Column(db.Boolean, default=False)  # admin
    wallet = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('User', back_populates='influencer', lazy=True)
    niches = db.relationship(
        'InfluencerNiche', back_populates='influencer', lazy=True)
    social_medias = db.relationship(
        'SocialMediaAccount', back_populates='influencer', lazy=True)
    proposals = db.relationship(
        'Proposal', back_populates='influencer', lazy='dynamic')
    sponsorships = db.relationship(
        'Sponsorship', back_populates='influencer', lazy='dynamic')
    engagements = db.relationship(
        'Engagement', back_populates='influencer', lazy='dynamic')
    payments = db.relationship(
        'Payment', back_populates='influencer', lazy='dynamic')
    reviews = db.relationship(
        'Review', back_populates='influencer', lazy='dynamic')
    activities = db.relationship(
        'InfluencerActivity', lazy=True)


class InfluencerNiche(db.Model):
    __tablename__ = 'influencer_niche'

    id = db.Column(db.Integer, primary_key=True)
    niche = db.Column(db.String(50), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey(
        'influencers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    influencer = db.relationship(
        'Influencer', back_populates='niches', lazy=True)

# Instagram, Facebook, Twitter, Youtube, Tiktok
class SocialMediaAccount(db.Model):
    __table_name__ = 'social_media_profiles'

    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey(
        'influencers.id'), nullable=False)
    platform = db.Column(db.String(20), nullable=False)
    handle = db.Column(db.String(100), nullable=False)  # url
    followers = db.Column(db.Integer, nullable=False)  # reach
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    influencer = db.relationship(
        'Influencer', back_populates='social_medias', lazy=True)


class InfluencerActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(
        db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)


# brand
class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)  # admin
    is_blocked = db.Column(db.Boolean, default=False)  # admin
    total_budget = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('User', back_populates='brand', lazy=True)
    campaigns = db.relationship(
        'Campaign', back_populates='brand', lazy='dynamic')
    activities = db.relationship(
        'BrandActivity', lazy=True)

    def __repr__(self):
        return f'<Brand {self.name}>'


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey(
        'brands.id'), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_date = db.Column(db.DateTime, nullable=False)
    allocated_budget = db.Column(db.Integer, default=0, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    brand = db.relationship('Brand', back_populates='campaigns', lazy=True)
    proposals = db.relationship(
        'Proposal', back_populates='campaign', lazy='dynamic')
    sponsorships = db.relationship(
        'Sponsorship', back_populates='campaign', lazy='dynamic')
    engagements = db.relationship(
        'Engagement', back_populates='campaign', lazy='dynamic')

    def __repr__(self):
        return f'<Campaign {self.name}>'


class Proposal(db.Model):
    __tablename__ = 'proposals'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(
        'campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey(
        'influencers.id'), nullable=False)
    message = db.Column(db.Text)
    requirements = db.Column(db.Text)
    is_public_infu = db.Column(db.Boolean, default=False)
    # 'pending', 'accepted', 'rejected', renegotiate, public-request
    status = db.Column(db.String(50), default='pending')
    original_amount = db.Column(db.Integer, default=0)
    negotiate_amount = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    influencer = db.relationship(
        'Influencer', back_populates='proposals', lazy=True)
    campaign = db.relationship(
        'Campaign', back_populates='proposals', lazy=True)
    sponsorship = db.relationship(
        'Sponsorship', back_populates='proposal', uselist=False, lazy=True)


class Sponsorship(db.Model):
    __tablename__ = 'sponsorships'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey(
        'campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey(
        'influencers.id'), nullable=False)
    proposal_id = db.Column(db.Integer, db.ForeignKey(
        'proposals.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    is_infu_reviewed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    influencer = db.relationship(
        'Influencer',  back_populates='sponsorships', lazy=True)
    campaign = db.relationship(
        'Campaign', back_populates='sponsorships', lazy=True)
    proposal = db.relationship(
        'Proposal', back_populates='sponsorship', lazy=True)
    payment = db.relationship(
        'Payment', back_populates='sponsorship', uselist=False, lazy=True)


class Engagement(db.Model):
    __tablename__ = 'engagements'

    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey(
        'influencers.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey(
        'campaigns.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # yt, insta, ...
    # 'post', 'story', 'video'
    content_type = db.Column(db.String(50), nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    reach = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(
        db.DateTime, default=datetime.now)  # engagement_date
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)  # approval date

    influencer = db.relationship(
        'Influencer', back_populates='engagements', lazy=True)
    campaign = db.relationship(
        'Campaign', back_populates='engagements', lazy=True)


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    sponsorship_id = db.Column(db.Integer, db.ForeignKey(
        'sponsorships.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey(
        'influencers.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    # 'pending', 'completed'
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    influencer = db.relationship(
        'Influencer', back_populates='payments', lazy=True)
    sponsorship = db.relationship(
        'Sponsorship', back_populates='payment', lazy=True)


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    sponsorship_id = db.Column(db.Integer, db.ForeignKey(
        'sponsorships.id'), nullable=False)
    influencer_id = db.Column(
        db.Integer, db.ForeignKey('influencers.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    influencer = db.relationship(
        'Influencer', back_populates='reviews', lazy=True)


class BrandActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey(
        'brands.id'), nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)


# enaggerment
# indian_views = db.Column(db.Integer, default=0)  demographic
    # male_views = db.Column(dbInteger, default=0)
    # new_followers = db.Column(db.Integer, default=0)
    # viral_posts = db.Column(db.Boolean, default=False)
    # agegroup


# class PlatformMetric(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     influencer_id = db.Column(db.Integer, db.ForeignKey(
#         'influencer.id'), nullable=False)
#     engagement_rate = db.Column(db.Float)
#     average_sponsorship_amount = db.Column(db.Float)
#     total_engagements = db.Column(db.Integer)
#     last_updated = db.Column(db.DateTime, default=datetime.now)


# campign management

# subcription for brands

# class Subcription(db.Model):
#     pass

# class CampaignManagement(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
#     brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
#     campaign_id = db.Column(db.Integer, db.ForeignKey('Campaign.id'), nullable=False)
