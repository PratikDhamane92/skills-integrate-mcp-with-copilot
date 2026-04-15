"""
SQLAlchemy models for the activity management system
"""

from sqlalchemy import Column, String, Integer, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# Association table for many-to-many relationship between activities and students
activity_participants = Table(
    'activity_participants',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True),
    Column('student_email', String, ForeignKey('students.email'), primary_key=True)
)


class Activity(Base):
    """Model for extracurricular activities"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)
    
    # Relationship to students
    participants = relationship(
        "Student",
        secondary=activity_participants,
        back_populates="activities"
    )

    def to_dict(self):
        """Convert activity to dictionary format"""
        return {
            "name": self.name,
            "description": self.description,
            "schedule": self.schedule,
            "max_participants": self.max_participants,
            "participants": [p.email for p in self.participants],
            "current_participants": len(self.participants)
        }


class Student(Base):
    """Model for students"""
    __tablename__ = "students"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade_level = Column(String, nullable=True)
    
    # Relationship to activities
    activities = relationship(
        "Activity",
        secondary=activity_participants,
        back_populates="participants"
    )

    def to_dict(self):
        """Convert student to dictionary format"""
        return {
            "email": self.email,
            "name": self.name,
            "grade_level": self.grade_level,
            "activities": [a.name for a in self.activities]
        }
