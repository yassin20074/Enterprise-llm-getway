import os
from dotenv import load_dotenv 
import redis
from groq import Groq
from langfuse import Langfuse
from nemoguardrails import LLMRails , RailsConfig

load_dotenv()

"""
Redis setup
"""
redis_client=redis.Redis(
    host=os.getenv("REDIS_HOST", "Localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

"""
Langfuse setup
"""

langfuse = Langfuse(
    public_key= os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key= os.getenv("LANGFUSE_SECRET_KEY"),
    host= os.getenv("LANGFUSE_HOST")
)

"""
GROQ Setup
"""

groq_client= Groq(api_key=os.getenv("GROQ_API_KEY"))

"""
NeMo Setup
"""
rails_config=RailsConfig.from_path("./config")
rails=LLMRails(rails_config)