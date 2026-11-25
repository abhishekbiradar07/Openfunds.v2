from app.database import db
from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.validators import validate_email


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def register_user(name, email, password):
        """Register a new user"""
        # Validate email
        if not validate_email(email):
            return None, "Invalid email format"
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return None, "Email already registered"
        
        # Validate password length
        if len(password) < 6:
            return None, "Password must be at least 6 characters"
        
        # Create user
        try:
            user = User(
                name=name,
                email=email,
                password_hash=hash_password(password)
            )
            db.session.add(user)
            db.session.commit()
            
            return user, "User registered successfully"
        except Exception as e:
            db.session.rollback()
            return None, f"Registration failed: {str(e)}"
    
    @staticmethod
    def login_user(email, password):
        """Authenticate user"""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return None, "Invalid email or password"
        
        if not user.is_active:
            return None, "Account is inactive"
        
        if not verify_password(password, user.password_hash):
            return None, "Invalid email or password"
        
        return user, "Login successful"
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()
