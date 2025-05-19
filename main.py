import json
from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Dict, List, Any
from datetime import datetime

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

load_dotenv()

class LinkedInProfileGenerator:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize the LinkedIn profile generator with specified model."""
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.7)
        self.json_parser = JsonOutputParser()
        self.training_data = []
        
    def load_training_data(self, training_data_path: str):
        """Load real LinkedIn profiles for training."""
        with open(training_data_path, 'r') as f:
            self.training_data = json.load(f)
            
    def create_profile_schema(self) -> Dict:
        """Create a schema for LinkedIn profiles."""
        return {
            "type": "object",
            "properties": {
                "profile_id": {"type": "string"},
                "full_name": {"type": "string"},
                "headline": {"type": "string"},
                "location": {"type": "string"},
                "about": {"type": "string"},
                "experience": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "company": {"type": "string"},
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    }
                },
                "education": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "school": {"type": "string"},
                            "degree": {"type": "string"},
                            "field_of_study": {"type": "string"},
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"}
                        }
                    }
                },
                "skills": {"type": "array", "items": {"type": "string"}},
                "languages": {"type": "array", "items": {"type": "string"}},
                "certifications": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "issuing_organization": {"type": "string"},
                            "issue_date": {"type": "string"},
                            "expiration_date": {"type": "string"}
                        }
                    }
                }
            }
        }
    
    def create_profile_generation_prompt(self, industry: str = None, experience_level: str = None) -> PromptTemplate:
        """Create a prompt for generating LinkedIn profiles."""
        training_context = ""
        if self.training_data:
            training_context = f"""
            Here are some example profiles to learn from:
            {json.dumps(self.training_data[:2], indent=2)}
            """
            
        return PromptTemplate(
            template=f"""Generate a realistic LinkedIn profile with the following characteristics:
            Industry: {industry or 'any'}
            Experience Level: {experience_level or 'any'}
            
            {training_context}
            
            The profile should be realistic and include:
            1. A professional headline
            2. A compelling about section
            3. Relevant work experience
            4. Educational background
            5. Skills and certifications
            6. Languages
            
            Make sure the dates are realistic and the career progression makes sense.
            
            {{format_instructions}}""",
            input_variables=[],
            partial_variables={"format_instructions": self.json_parser.get_format_instructions()}
        )
    
    def generate_profile(self, industry: str = None, experience_level: str = None) -> Dict:
        """Generate a single LinkedIn profile."""
        prompt = self.create_profile_generation_prompt(industry, experience_level)
        chain = prompt | self.llm | self.json_parser
        return chain.invoke({})
    
    def generate_profiles(self, num_profiles: int, industry: str = None, experience_level: str = None) -> List[Dict]:
        """Generate multiple LinkedIn profiles."""
        profiles = []
        for _ in range(num_profiles):
            profile = self.generate_profile(industry, experience_level)
            profiles.append(profile)
        return profiles
    
    def combine_with_real_profiles(self, synthetic_profiles: List[Dict], real_profiles: List[Dict]) -> List[Dict]:
        """Combine synthetic profiles with real profiles."""
        return synthetic_profiles + real_profiles
    
    def save_profiles(self, profiles: List[Dict], output_path: str):
        """Save generated profiles to a JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(profiles, f, indent=2)

def main():
    # Example usage
    generator = LinkedInProfileGenerator()
    
    # Load training data if available
    training_data_path = "data/real_profiles.json"
    if os.path.exists(training_data_path):
        generator.load_training_data(training_data_path)
    
    # Generate profiles for software engineers
    profiles = generator.generate_profiles(
        num_profiles=3,
        industry="Software Engineering",
        experience_level="Senior"
    )
    
    # Print the first generated profile
    print("Generated Profile Example:", json.dumps(profiles[0], indent=2))
    
    # Save all profiles
    generator.save_profiles(profiles, "output/synthetic_linkedin_profiles.json")

if __name__ == "__main__":
    main()


