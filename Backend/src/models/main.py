from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum
from uuid import UUID


class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class NotificationType(str, Enum):
    QUESTION_ANSWERED = "question_answered"
    ANSWER_ACCEPTED = "answer_accepted"
    COMMENT_ADDED = "comment_added"
    QUIZ_COMPLETED = "quiz_completed"


# Base Models for creation (without id and timestamps)
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class TagCreate(TagBase):
    pass


class QuestionBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)


class QuestionCreate(QuestionBase):
    tag_ids: List[UUID] = Field(default_factory=list)


class QuestionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    tag_ids: Optional[List[UUID]] = None


class AnswerBase(BaseModel):
    description: str = Field(..., min_length=10)


class AnswerCreate(AnswerBase):
    question_id: UUID


class AnswerUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=10)
    is_accepted: Optional[bool] = None


class CommentBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    answer_id: UUID
    parent_id: Optional[UUID] = None


class CommentUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=1000)


class VoteBase(BaseModel):
    value: int = Field(..., ge=-1, le=1)  # -1 for downvote, 0 for no vote, 1 for upvote


class VoteCreate(VoteBase):
    answer_id: UUID


class VoteUpdate(VoteBase):
    pass


class NotificationBase(BaseModel):
    type: NotificationType
    content: str = Field(..., min_length=1, max_length=500)


class NotificationCreate(NotificationBase):
    user_id: UUID


class NotificationUpdate(BaseModel):
    is_read: bool = True


class MCQQuizBase(BaseModel):
    topic: str = Field(..., min_length=1, max_length=100)


class MCQQuizCreate(MCQQuizBase):
    pass


class MCQQuizUpdate(BaseModel):
    topic: Optional[str] = Field(None, min_length=1, max_length=100)


class MCQQuestionBase(BaseModel):
    question_text: str = Field(..., min_length=5)
    option_a: str = Field(..., min_length=1, max_length=200)
    option_b: str = Field(..., min_length=1, max_length=200)
    option_c: str = Field(..., min_length=1, max_length=200)
    option_d: str = Field(..., min_length=1, max_length=200)
    correct_option: str = Field(..., regex=r'^[A-D]$')


class MCQQuestionCreate(MCQQuestionBase):
    quiz_id: UUID


class MCQQuestionUpdate(BaseModel):
    question_text: Optional[str] = Field(None, min_length=5)
    option_a: Optional[str] = Field(None, min_length=1, max_length=200)
    option_b: Optional[str] = Field(None, min_length=1, max_length=200)
    option_c: Optional[str] = Field(None, min_length=1, max_length=200)
    option_d: Optional[str] = Field(None, min_length=1, max_length=200)
    correct_option: Optional[str] = Field(None, regex=r'^[A-D]$')


# Response Models (with id and timestamps)
class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime


class UserPublic(BaseModel):
    """Public user model without sensitive information"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    username: str
    role: UserRole
    created_at: datetime


class Tag(TagBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID


class Question(QuestionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    # Related objects
    user: UserPublic
    tags: List[Tag] = Field(default_factory=list)
    answers: List["Answer"] = Field(default_factory=list)


class Answer(AnswerBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    question_id: UUID
    user_id: UUID
    is_accepted: bool = False
    created_at: datetime
    updated_at: datetime
    
    # Related objects
    user: UserPublic
    comments: List["Comment"] = Field(default_factory=list)
    votes: List["Vote"] = Field(default_factory=list)
    
    # Computed fields
    vote_count: int = Field(default=0)


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    answer_id: UUID
    parent_id: Optional[UUID] = None
    created_at: datetime
    
    # Related objects
    user: UserPublic
    replies: List["Comment"] = Field(default_factory=list)


class Vote(VoteBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    answer_id: UUID
    created_at: datetime
    
    # Related objects
    user: UserPublic


class Notification(NotificationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    is_read: bool = False
    created_at: datetime


class MCQQuiz(MCQQuizBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    created_at: datetime
    
    # Related objects
    user: UserPublic
    questions: List["MCQQuestion"] = Field(default_factory=list)


class MCQQuestion(MCQQuestionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    quiz_id: UUID


class MCQQuestionPublic(BaseModel):
    """MCQ Question without correct answer for quiz takers"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    quiz_id: UUID
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str


# Pagination and Response Models
class PaginatedResponse(BaseModel):
    items: List[BaseModel]
    total: int
    page: int
    per_page: int
    pages: int


class QuestionList(PaginatedResponse):
    items: List[Question]


class AnswerList(PaginatedResponse):
    items: List[Answer]


class CommentList(PaginatedResponse):
    items: List[Comment]


class NotificationList(PaginatedResponse):
    items: List[Notification]


class MCQQuizList(PaginatedResponse):
    items: List[MCQQuiz]


# Quiz attempt models
class QuizAttemptCreate(BaseModel):
    quiz_id: UUID
    answers: List[dict] = Field(..., description="List of {question_id: UUID, selected_option: str}")


class QuizResult(BaseModel):
    quiz_id: UUID
    total_questions: int
    correct_answers: int
    score_percentage: float
    answers: List[dict] = Field(..., description="List of {question_id: UUID, selected_option: str, correct_option: str, is_correct: bool}")


# Authentication models
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Error models
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    detail: List[dict]


# Update forward references
Question.model_rebuild()
Answer.model_rebuild()
Comment.model_rebuild()
MCQQuiz.model_rebuild()