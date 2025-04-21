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

"""Farewell agent for Sei therapist that handles session closings."""

from google.adk.agents import Agent

from sei_therapist.sub_agents.farewell import prompt
from sei_therapist.tools.memory import create_session_summary

# Agent for handling session closings with summary and continuity
farewell_agent = Agent(
    model="gemini-2.0-flash",
    name="farewell_agent",
    description="Handles session closings with summary and therapeutic continuity",
    instruction=prompt.FAREWELL_AGENT_INSTR,
    tools=[create_session_summary],
)