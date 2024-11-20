from app.models.lesson import Lesson, LessonCreate
from app.models.classroom import Classroom, ClassroomCreate
from app.models.user import User, UserCreate
from app.models.teacher import Teacher, TeacherCreate
from app.service.crud import CRUDBase, CRUDUser

lesson_crud = CRUDBase[Lesson, LessonCreate](Lesson)
classroom_crud = CRUDBase[Classroom, ClassroomCreate](Classroom)
user_crud = CRUDUser[User, UserCreate](User)
teacher_crud = CRUDBase[Teacher, TeacherCreate](Teacher)