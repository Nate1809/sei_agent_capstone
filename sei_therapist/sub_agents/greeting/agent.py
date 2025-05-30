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

"""Greeting agent for Sei therapist that handles session openings."""

from google.adk.agents import Agent

from sei_therapist.sub_agents.greeting import prompt

# Agent for handling session openings with warmth and continuity
greeting_agent = Agent(
    model="gemini-2.0-flash",
    name="greeting_agent",
    description="Handles session openings with warmth and therapeutic continuity",
    instruction=prompt.GREETING_AGENT_INSTR,
)