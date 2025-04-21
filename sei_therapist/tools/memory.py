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

"""Memory tools for Sei therapist to store and retrieve information."""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from sei_therapist.shared_libraries import constants

# Path to load a default profile if needed
DEFAULT_PROFILE_PATH = os.getenv("SEI_DEFAULT_PROFILE", "eval/default_profile.json")

def memorize(key: str, value: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Store a piece of information in memory.
    
    Args:
        key: The label for storing the value.
        value: The information to be stored.
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming storage.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}

def memorize_list(key: str, value: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Add an item to a list in memory.
    
    Args:
        key: The label for the list.
        value: The item to add to the list.
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming addition.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    if value not in mem_dict[key]:
        mem_dict[key].append(value)
    return {"status": f'Added "{value}" to list "{key}"'}

def forget(key: str, value: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Remove an item from memory.
    
    Args:
        key: The label of the memory containing the value.
        value: The value to remove.
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming removal.
    """
    if tool_context.state.get(key) is None:
        return {"status": f'Key "{key}" not found in memory.'}
    
    if isinstance(tool_context.state[key], list):
        if value in tool_context.state[key]:
            tool_context.state[key].remove(value)
            return {"status": f'Removed "{value}" from list "{key}".'}
        return {"status": f'Value "{value}" not found in list "{key}".'}
    
    tool_context.state[key] = None
    return {"status": f'Removed value at key "{key}".'}

def remember_insight(insight: str, category: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Record a therapeutic insight discovered during the session.
    
    Args:
        insight: The content of the insight.
        category: The category of the insight (e.g., "patterns", "beliefs", "emotions").
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming the insight was recorded.
    """
    session_insights = tool_context.state.get(constants.SESSION_INSIGHTS, [])
    
    new_insight = {
        "content": insight,
        "category": category,
        "timestamp": datetime.now().isoformat()
    }
    
    session_insights.append(new_insight)
    tool_context.state[constants.SESSION_INSIGHTS] = session_insights
    
    return {"status": f"Insight recorded in category '{category}'."}

def update_user_profile(field: str, value: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Update a field in the user's profile.
    
    Args:
        field: The field to update (e.g., "name", "age", "faith_preference").
        value: The value to set for the field.
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming the profile was updated.
    """
    print(f"DEBUG: Starting update_user_profile for field '{field}' with value '{value}'")
    
    # Get the entire user profile as a new dictionary
    user_profile = dict(tool_context.state.get(constants.USER_PROFILE, {}))
    print(f"DEBUG: Current profile: {user_profile}")
    
    # Update the field in our copy
    user_profile[field] = value
    
    # Reassign the entire profile back to state
    tool_context.state[constants.USER_PROFILE] = user_profile
    
    print(f"DEBUG: Updated profile: {tool_context.state.get(constants.USER_PROFILE, {})}")
    
    return {"status": f"Profile updated - {field}: {value}"}

def add_user_concern(concern: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Add a therapeutic concern to the user's profile.
    
    Args:
        concern: The concern to add (e.g., "depression", "anxiety", "relationships").
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming the concern was added.
    """
    print(f"DEBUG: Starting add_user_concern for concern '{concern}'")
    
    # Get the entire user profile as a new dictionary
    user_profile = dict(tool_context.state.get(constants.USER_PROFILE, {}))
    print(f"DEBUG: Current profile: {user_profile}")
    
    # Make sure concerns exist
    if constants.USER_CONCERNS not in user_profile:
        user_profile[constants.USER_CONCERNS] = []
    
    # Add the concern if not already present
    if concern not in user_profile[constants.USER_CONCERNS]:
        user_profile[constants.USER_CONCERNS].append(concern)
    
    # Reassign the entire profile back to state
    tool_context.state[constants.USER_PROFILE] = user_profile
    
    print(f"DEBUG: Updated profile: {tool_context.state.get(constants.USER_PROFILE, {})}")
    
    return {"status": f"Added concern '{concern}' to user profile."}

def create_session_summary(topics: List[str], insights: List[str], homework: Optional[str], progress: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Create a summary of the current therapy session.
    
    Args:
        topics: List of main topics discussed.
        insights: List of key insights from the session.
        homework: Optional homework assignments (provide empty string if none).
        progress: Notes on therapeutic progress.
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming the summary was created.
    """
    # Ensure homework is never None
    if homework is None:
        homework = ""
        
    session_count = tool_context.state.get(constants.SESSION_COUNT, 0)
    
    summary = {
        "session_number": session_count + 1,
        "date": datetime.now().isoformat(),
        "topics_discussed": topics,
        "insights_gained": insights,
        "homework": homework,
        "progress_notes": progress
    }
    
    summaries = tool_context.state.get(constants.SESSION_SUMMARIES, [])
    summaries.append(summary)
    tool_context.state[constants.SESSION_SUMMARIES] = summaries
    
    # Update session count
    tool_context.state[constants.SESSION_COUNT] = session_count + 1
    
    return {"status": "Session summary created and saved."}

def _set_initial_state(source: Dict[str, Any], target: State | Dict[str, Any]) -> None:
    """
    Initialize session state with default values.
    
    Args:
        source: Initial state values to set.
        target: The session state to modify.
    """
    if constants.SYSTEM_TIME not in target: 
        target[constants.SYSTEM_TIME] = str(datetime.now())
    
    if constants.SESSION_INITIALIZED not in target:
        target[constants.SESSION_INITIALIZED] = True
        target.update(source)
        
        # Initialize user profile if provided
        if constants.USER_PROFILE in source:
            target[constants.USER_PROFILE] = source[constants.USER_PROFILE]
        else:
            target[constants.USER_PROFILE] = {
                constants.USER_NAME: "",
                constants.USER_AGE: None,
                constants.USER_GENDER: None,
                constants.USER_FAITH: None,
                constants.USER_CONCERNS: []
            }
        
        # Initialize session counters and lists
        target[constants.SESSION_COUNT] = source.get(constants.SESSION_COUNT, 0)
        target[constants.SESSION_INSIGHTS] = []
        target[constants.SESSION_SUMMARIES] = source.get(constants.SESSION_SUMMARIES, [])

def _load_default_profile(callback_context: CallbackContext) -> None:
    """
    Load a default user profile into session state.
    This function is called as a callback before the agent starts.
    
    Args:
        callback_context: The callback context.
    """
    data = {"state": {
        "user_profile": {
            "name": "",
            "age": None,
            "gender": None,
            "faith_preference": None,
            "concerns": [],
            "session_count": 0
        },
        "session_insights": [],
        "session_summaries": [],
        "treatment_plan": {},
        "session_count": 0,
        "session_initialized": False
    }}
    
    try:
        if os.path.exists(DEFAULT_PROFILE_PATH):
            with open(DEFAULT_PROFILE_PATH, "r") as file:
                data = json.load(file)
                print(f"\nLoading Initial State: {data}\n")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Using default initial state. Error loading profile: {e}")
    
    _set_initial_state(data.get("state", {}), callback_context.state)

def create_treatment_plan(concerns: List[str], goals: List[Dict[str, Any]], 
                          approaches: List[str], timeline: str, 
                          milestones: List[str], tool_context: ToolContext) -> Dict[str, str]:
    """
    Create or update a treatment plan based on the user's needs.
    
    Args:
        concerns: List of therapeutic concerns being addressed
        goals: List of therapeutic goals and their status
        approaches: List of therapeutic approaches being utilized
        timeline: Estimated timeline for treatment
        milestones: Key milestones to work toward
        tool_context: The ADK tool context
        
    Returns:
        A status message confirming the plan was created/updated
    """
    print(f"DEBUG: Creating treatment plan with {len(concerns)} concerns and {len(goals)} goals")
    
    # Create the treatment plan
    treatment_plan = {
        "concerns": concerns,
        "goals": goals,
        "approaches": approaches,
        "estimated_timeline": timeline,
        "milestones": milestones,
        "created_on": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat()
    }
    
    # Assign the entire object to state
    tool_context.state[constants.TREATMENT_PLAN] = treatment_plan
    
    print(f"DEBUG: Treatment plan created with {len(concerns)} concerns")
    
    return {"status": "Treatment plan created successfully."}