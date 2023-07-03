from app.database.database import Base
from sqlalchemy import Column, String, Boolean, Double
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import uuid

# create a class for the institution schema
class Institution_Schema(Base):
    __tablename__ = "institutions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(200), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))

# create a class for the person schema
class Person_Schema(Base):
    __tablename__ = "persons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))
    phone = Column(String(15), nullable=True)
    address = Column(String(255), nullable=True)
    institution_id = Column(UUID, ForeignKey("institutions.id", ondelete='CASCADE'), nullable=False)
    institution = relationship('Institution_Schema')

# create a class for the user schema
class User_Schema(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    email = Column(String(85), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, server_default='FALSE')
    is_superuser = Column(Boolean, server_default='FALSE')
    is_teacher = Column(Boolean, server_default='FALSE')
    person_id = Column(UUID, ForeignKey("persons.id", ondelete='CASCADE'), nullable=False)
    person = relationship('Person_Schema')

# create a class for the students schema
class Student_Schema(Base):
    __tablename__ = "students"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    identification = Column(String(255), nullable=False, unique=True)
    contact = Column(String(150), nullable=True)
    person_id = Column(UUID, ForeignKey("persons.id", ondelete='CASCADE'), nullable=False)
    person = relationship('Person_Schema')
    level_id = Column(UUID, ForeignKey("levels.id", ondelete='CASCADE'), nullable=False)
    level = relationship('Academic_Degree_Schema')
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User_Schema')
    observations = Column(String(255), nullable=True)

# create a class for the teachers in students schema
class Teacher_Schema(Base):
    __tablename__ = "teachers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    student_id = Column(UUID, ForeignKey("students.id", ondelete='CASCADE'), nullable=False)
    student = relationship('Student_Schema')
    teacher_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    teacher = relationship('User_Schema')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))

# create a class for the levels schema
class Academic_Degree_Schema(Base):
    __tablename__ = "levels"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(150), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))

# create a class for the subjects schema
class Subject_Schema(Base):
    __tablename__ = "subjects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(150), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User_Schema')

#create a class for the periods schema
class Period_Schema(Base):
    __tablename__ = "periods"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(150), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User_Schema')

# create a class for the sections schema
class Section_Schema(Base):
    __tablename__ = "sections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(150), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))

# create a class for the students in sections schema
class Student_In_Section_Schema(Base):
    __tablename__ = "students_in_sections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    section_id = Column(UUID, ForeignKey("sections.id", ondelete='CASCADE'), nullable=False)
    section = relationship('Section_Schema')
    student_id = Column(UUID, ForeignKey("students.id", ondelete='CASCADE'), nullable=False)
    student = relationship('Student_Schema')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))

# create a class for the teachers in sections schema
class Teacher_In_Section_Schema(Base):
    __tablename__ = "teachers_in_sections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    section_id = Column(UUID, ForeignKey("sections.id", ondelete='CASCADE'), nullable=False)
    section = relationship('Section_Schema')
    teacher_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    teacher = relationship('User_Schema')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))

# create a class for the assistance schema
class Assistance_Schema(Base):
    __tablename__ = "assistance"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    subject_id = Column(UUID, ForeignKey("subjects.id", ondelete='CASCADE'), nullable=False)
    subject = relationship('Subject_Schema')
    student_id = Column(UUID, ForeignKey("students.id", ondelete='CASCADE'), nullable=False)
    student = relationship('Student_Schema')
    level_id = Column(UUID, ForeignKey("levels.id", ondelete='CASCADE'), nullable=False)
    level = relationship('Academic_Degree_Schema')
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User_Schema')
    period_id = Column(UUID, ForeignKey("periods.id", ondelete='CASCADE'), nullable=False)
    period = relationship('Period_Schema')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))

# create a class for the homeworks schema
class Homework_Schema(Base):
    __tablename__ = "homeworks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    average = Column(Double, nullable=False)
    observations = Column(String(255), nullable=True)
    title = Column(String(200), nullable=False)
    subject_id = Column(UUID, ForeignKey("subjects.id", ondelete='CASCADE'), nullable=False)
    subject = relationship('Subject_Schema')
    student_id = Column(UUID, ForeignKey("students.id", ondelete='CASCADE'), nullable=False)
    student = relationship('Student_Schema')
    level_id = Column(UUID, ForeignKey("levels.id", ondelete='CASCADE'), nullable=False)
    level = relationship('Academic_Degree_Schema')
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User_Schema')
    period_id = Column(UUID, ForeignKey("periods.id", ondelete='CASCADE'), nullable=False)
    period = relationship('Period_Schema')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))

# create a class for the tests schema
class Test_Schema(Base):
    __tablename__ = "tests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    average = Column(Double, nullable=False)
    observations = Column(String(255), nullable=True)
    title = Column(String(200), nullable=False)
    subject_id = Column(UUID, ForeignKey("subjects.id", ondelete='CASCADE'), nullable=False)
    subject = relationship('Subject_Schema')
    student_id = Column(UUID, ForeignKey("students.id", ondelete='CASCADE'), nullable=False)
    student = relationship('Student_Schema')
    level_id = Column(UUID, ForeignKey("levels.id", ondelete='CASCADE'), nullable=False)
    level = relationship('Academic_Degree_Schema')
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User_Schema')
    period_id = Column(UUID, ForeignKey("periods.id", ondelete='CASCADE'), nullable=False)