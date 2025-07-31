#!/usr/bin/env python3

from final_forest_fire_agent import ForestFireAgent

print("Creating agent...")
agent = ForestFireAgent()

print("Agent attributes:")
print(f"- has gemini_model: {hasattr(agent, 'gemini_model')}")
print(f"- has agent: {hasattr(agent, 'agent')}")
print(f"- has api_key: {hasattr(agent, 'api_key')}")

if hasattr(agent, 'gemini_model'):
    print(f"- gemini_model: {agent.gemini_model}")
    print(f"- gemini_model type: {type(agent.gemini_model)}")

if hasattr(agent, 'agent'):
    print(f"- agent: {agent.agent}")
    print(f"- agent type: {type(agent.agent)}")

print("\nTesting query...")
response = agent.query("Test message")
print(f"Response: {response[:100]}...")
