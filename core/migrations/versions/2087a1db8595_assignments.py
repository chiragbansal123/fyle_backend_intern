"""assignments

Revision ID: 2087a1db8595
Revises: 4078b3b57e24
Create Date: 2021-09-16 10:11:14.484440

"""
from alembic import op
import sqlalchemy as sa
from core import db
from core.apis.decorators import AuthPrincipal
from core.models.users import User
from core.models.students import Student
from core.models.teachers import Teacher
from core.models.assignments import Assignment , AssignmentStateEnum ,GradeEnum

# revision identifiers, used by Alembic.
revision = '2087a1db8595'
down_revision = '4078b3b57e24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assignments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('grade', sa.Enum('A', 'B', 'C', 'D', name='gradeenum'), nullable=True),
    sa.Column('state', sa.Enum('DRAFT', 'SUBMITTED', name='assignmentstateenum'), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    student_1 = Student(user_id=User.get_by_email('student1@fylebe.com').id)
    student_2 = Student(user_id=User.get_by_email('student2@fylebe.com').id)
    teacher_1 = Teacher(user_id=User.get_by_email('teacher1@fylebe.com').id)
    teacher_2 = Teacher(user_id=User.get_by_email('teacher2@fylebe.com').id)

    db.session.add(student_1)
    db.session.add(student_2)
    db.session.add(teacher_1)
    db.session.add(teacher_2)
    db.session.flush()

    assignment_1 = Assignment(student_id=student_1.id, content='ESSAY T1')
    assignment_2 = Assignment(student_id=student_1.id, content='THESIS T1')
    assignment_3 = Assignment(student_id=student_2.id, content='ESSAY T2')
    assignment_4 = Assignment(student_id=student_2.id, content='THESIS T2')
    # assignment_4.state= AssignmentStateEnum.GRADED
    # assignment_4.grade= GradeEnum.C
    assignment_5 = Assignment(student_id=student_1.id, content='SOLUTION T1')

    db.session.add(assignment_1)
    db.session.add(assignment_2)
    db.session.add(assignment_3)
    db.session.add(assignment_4)
    db.session.add(assignment_5)

    db.session.flush()

    Assignment.submit(
        _id=assignment_1.id,
        teacher_id=teacher_1.id,
        auth_principal=AuthPrincipal(user_id=student_1.user_id, student_id=student_1.id)
    )

    Assignment.submit(
        _id=assignment_3.id,
        teacher_id=teacher_2.id,
        auth_principal=AuthPrincipal(user_id=student_2.user_id, student_id=student_2.id)
    )

    Assignment.submit(
        _id=assignment_4.id,
        teacher_id=teacher_2.id,
        auth_principal=AuthPrincipal(user_id=student_2.user_id, student_id=student_2.id)
    )

    db.session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assignments')
    op.drop_table('teachers')
    op.drop_table('students')
    # ### end Alembic commands ###
