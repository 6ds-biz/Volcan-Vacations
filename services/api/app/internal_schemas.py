from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, AwareDatetime, field_validator, model_validator
from .inventory_schemas import Input, ReadModel

Role = Literal['owner_admin','operations_partner','staff']
Profile = Literal['Owner','Operations','Staff']
TaskStatus = Literal['open','in_progress','waiting','completed','cancelled']
Priority = Literal['low','normal','high','urgent']
Entity = Literal['booking','supplier','tour','payment','availability','agreement','customer']

class Credentials(BaseModel):
    model_config = ConfigDict(extra='forbid', hide_input_in_errors=True)
    email: str = Field(max_length=180, pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    password: str = Field(min_length=1, max_length=128, repr=False)
    @field_validator('email', mode='before')
    @classmethod
    def normalize(cls, value):
        return value.strip().lower() if isinstance(value,str) else value

class UserCreate(Credentials):
    password: str = Field(min_length=15, max_length=128, repr=False)
    display_name: str = Field(min_length=1,max_length=140)
    role: Role
    dashboard_profile: Profile | None = None

class UserUpdate(Input):
    display_name: str = Field(min_length=1,max_length=140)
    role: Role
    dashboard_profile: Profile
    active: bool

class PasswordChange(BaseModel):
    model_config = ConfigDict(extra='forbid', hide_input_in_errors=True)
    current_password: str = Field(min_length=1,max_length=128,repr=False)
    new_password: str = Field(min_length=15,max_length=128,repr=False)

class UserRead(ReadModel):
    id: int
    email: str
    display_name: str
    role: Role
    active: bool
    dashboard_profile: Profile
    must_change_password: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime

class TaskInput(Input):
    title: str = Field(min_length=1,max_length=220)
    description: str | None = Field(default=None,max_length=10000)
    assigned_user_id: int | None = Field(default=None,gt=0)
    related_entity_type: Entity | None = None
    related_entity_id: int | None = Field(default=None,gt=0)
    priority: Priority = 'normal'
    status: TaskStatus = 'open'
    queue_role: Literal['operations','owner_admin'] = 'operations'
    due_at: AwareDatetime | None = None
    @model_validator(mode='after')
    def related(self):
        if (self.related_entity_type is None) != (self.related_entity_id is None):
            raise ValueError('Related entity type and ID must be supplied together')
        return self

class TaskUpdate(TaskInput):
    expected_version: int = Field(gt=0)

class Assignment(Input):
    assigned_user_id: int | None = Field(default=None,gt=0)
    expected_version: int = Field(gt=0)

class Followup(Input):
    internal_notes: str = Field(max_length=10000)
    expected_version: int = Field(gt=0)
