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

"""Onboarding agent for Sei therapist that handles first-time sessions."""

from google.adk.agents import Agent

from sei_therapist.sub_agents.onboarding import prompt
from sei_therapist.tools.memory import update_user_profile, add_user_concern, remember_insight

# Agent for handling first-time users and gathering essential information
onboarding_agent = Agent(
    model="gemini-2.0-flash",
    name="onboarding_agent",
    description="Handles initial therapy sessions, gathers user information, and builds therapeutic rapport",
    instruction=prompt.ONBOARDING_AGENT_INSTR,
    tools=[update_user_profile, add_user_concern, remember_insight],
)