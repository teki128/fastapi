from app.service.crud import CRUDBase, CRUDOnlyRead, CRUDNoUpdate, CRUDUser
from app.models.user import User, UserCreate, UserUpdate, UserPublic
from app.models.lesson import Lesson, LessonCreate, LessonUpdate, LessonPublic
from app.models.college import College, CollegeCreate, CollegeUpdate, CollegePublic
from app.models.classroom import Classroom, ClassroomCreate, ClassroomUpdate, ClassroomPublic
from app.models.course import Course, CourseCreate, CourseUpdate, CoursePublic
from app.models.favour import Favour, FavourCreate, FavourUpdate, FavourPublic
from app.models.notice import Notice, NoticeCreate, NoticeUpdate, NoticePublic
from app.models.schedule import Schedule, ScheduleCreate, ScheduleUpdate, SchedulePublic
from app.models.section import Section, SectionCreate, SectionUpdate, SectionPublic
from app.models.teacher import Teacher, TeacherCreate, TeacherUpdate, TeacherPublic
from app.models.teach import Teach, TeachCreate, TeachUpdate, TeachPublic

user_crud = CRUDUser(User, UserCreate, UserUpdate, UserPublic)
lesson_crud = CRUDNoUpdate(Lesson, LessonCreate, LessonUpdate, LessonPublic)
college_crud = CRUDOnlyRead(College, CollegeCreate, CollegeUpdate, CollegePublic)
classroom_crud = CRUDOnlyRead(Classroom, ClassroomCreate, ClassroomUpdate, ClassroomPublic)
course_crud = CRUDNoUpdate(Course, CourseCreate, CourseUpdate, CoursePublic)
favour_crud = CRUDNoUpdate(Favour, FavourCreate, FavourUpdate, FavourPublic)
notice_crud = CRUDBase(Notice, NoticeCreate, NoticeUpdate, NoticePublic)
schedule_crud = CRUDNoUpdate(Schedule, ScheduleCreate, ScheduleUpdate, SchedulePublic)
section_crud = CRUDBase(Section, SectionCreate, SectionUpdate, SectionPublic)
teacher_crud = CRUDOnlyRead(Teacher, TeacherCreate, TeacherUpdate, TeacherPublic)
teach_crud = CRUDNoUpdate(Teach, TeachCreate, TeachUpdate, TeachPublic)
