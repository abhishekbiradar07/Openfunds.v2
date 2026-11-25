from app.database import db
from datetime import datetime
from sqlalchemy.sql import func


class Campaign(db.Model):
    """Campaign model for fundraising campaigns"""
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    btc_address = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='Active')  # Active, Funded, Closed
    
    # Foreign key
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<Campaign {self.title}>'
    
    def to_dict(self):
        """Convert campaign to dictionary"""
        progress = (self.current_amount / self.target_amount * 100) if self.target_amount > 0 else 0
        
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'btc_address': self.btc_address,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'status': self.status,
            'progress': round(progress, 2),
            'owner_id': self.owner_id,
            'owner_name': self.owner.name if self.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
