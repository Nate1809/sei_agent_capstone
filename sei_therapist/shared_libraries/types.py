# Copyright 2025 Sei AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Common data schema and types for Sei therapist agents."""

from typing import List, Optional, Dict, Any
from google.genai import types
from pydantic import BaseModel, Field

# Configuration for controlled JSON generation
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

class UserProfile(BaseModel):
    """User profile information."""
    name: str = Field(description="User's name")
    age: Optional[int] = Field(description="User's age if shared")
    gender: Optional[str] = Field(description="User's gender if shared")
    faith_preference: Optional[str] = Field(description="Faith preference if shared (e.g., Christian)")
    concerns: List[str] = Field(description="List of the user's therapeutic concerns")
    session_count: int = Field(default=0, description="Number of sessions completed")
    
class TherapeuticInsight(BaseModel):
    """An insight discovered during therapy."""
    content: str = Field(description="The insight content")
    session: int = Field(description="Session number in which insight was discovered")
    timestamp: str = Field(description="Timestamp when insight was recorded")

class ThoughtRecord(BaseModel):
    """A CBT thought record entry."""
    situation: str = Field(description="The situation that triggered the thought")
    thoughts: str = Field(description="Automatic thoughts that occurred")
    emotions: str = Field(description="Emotions experienced and their intensity")
    evidence_for: str = Field(description="Evidence supporting the thought")
    evidence_against: str = Field(description="Evidence against the thought")
    balanced_thought: str = Field(description="Alternative, balanced perspective")
    timestamp: str = Field(description="When the thought record was created")

class SessionPlan(BaseModel):
    """A plan for the current therapy session."""
    session_number: int = Field(description="The current session number")
    focus_areas: List[str] = Field(description="Key areas to focus on in this session")
    therapeutic_approaches: List[str] = Field(description="Therapeutic approaches to utilize")
    goals: List[str] = Field(description="Goals for this session")

class TreatmentPlan(BaseModel):
    """A longer-term treatment plan."""
    concerns: List[str] = Field(description="The concerns being addressed")
    goals: List[Dict[str, Any]] = Field(description="Therapeutic goals and their status")
    approaches: List[str] = Field(description="Therapeutic approaches being utilized")
    estimated_timeline: str = Field(description="Estimated timeline for treatment")
    milestones: List[str] = Field(description="Key milestones to work toward")

class SessionSummary(BaseModel):
    """A summary of a therapy session."""
    session_number: int = Field(description="The session number")
    date: str = Field(description="Date of the session")
    topics_discussed: List[str] = Field(description="Main topics discussed")
    insights_gained: List[str] = Field(description="Key insights discovered")
    homework: Optional[str] = Field(description="Any assignments for between sessions")
    progress_notes: str = Field(description="Notes on therapeutic progress")

class CrisisPlan(BaseModel):
    """A safety plan for crisis situations."""
    warning_signs: List[str] = Field(description="Warning signs to watch for")
    coping_strategies: List[str] = Field(description="Personal coping strategies")
    social_contacts: List[str] = Field(description="People who can provide support")
    professional_resources: List[str] = Field(description="Professional resources to contact")
    emergency_contacts: List[str] = Field(description="Emergency contact information")