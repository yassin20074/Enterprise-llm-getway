from fastapi import HTTPException, status
from config import redis_client, langfuse, groq_client, rails

"""
Create a functiob to Check rate limiting
"""
def check_rate_limit(user_id: str, max_requests: int = 5, window_seconds: int = 60) -> bool:
    key = f"rate_limit:{user_id}"
    current_requests = redis_client.get(key)
    
    if current_requests and int(current_requests) >= max_requests:
        return False
    
    pipeline = redis_client.pipeline()
    pipeline.incr(key)
    if not current_requests:
        pipeline.expire(key, window_seconds)
    pipeline.execute()
    return True

async def process_chat_request(user_id: str, prompt: str, model: str):
    """
    1. Rate Limiting Check
    """
    if not check_rate_limit(user_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Maximum 5 requests per minute allowed."
        )
    """
    2. Guardrails Check
    """
    guard_response = await rails.generate_async(prompt=prompt)
    if "Security Alert" in guard_response.response[0]["content"]:
        trace = langfuse.trace(
            name="llm_chat_completion_blocked",
            user_id=user_id,
            metadata={"model": model, "blocked": True}
        )
        return {
            "response": guard_response.response[0]["content"],
            "model_used": model,
            "trace_id": trace.id,
            "cached": False,
            "blocked": True
        }
    """
    3. Caching Check
    """
    cache_key = f"cache:{model}:{prompt.strip().lower()}"
    cached_response = redis_client.get(cache_key)

    if cached_response:
        trace = langfuse.trace(
            name="llm_chat_completion_cache_hit",
            user_id=user_id,
            metadata={"model": model, "cached": True}
        )
        return {
            "response": cached_response,
            "model_used": model,
            "trace_id": trace.id,
            "cached": True,
            "blocked": False
        }
    """
    4. LLM Execution
    """
    trace = langfuse.trace(
        name="llm_chat_completion",
        user_id=user_id,
        metadata={"model": model, "cached": False}
    )
    
    generation = trace.generation(
        name="groq_llm_call",
        model=model,
        input=prompt
    )
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )
        output_text = chat_completion.choices[0].message.content
        """
         Cache standard TTL
        """
        redis_client.setex(name=cache_key, time=3600, value=output_text)
        
        generation.end(
            output=output_text,
            usage={
                "prompt_tokens": chat_completion.usage.prompt_tokens,
                "completion_tokens": chat_completion.usage.completion_tokens,
                "total_tokens": chat_completion.usage.total_tokens,
            }
        )
        
        return {
            "response": output_text,
            "model_used": model,
            "trace_id": trace.id,
            "cached": False,
            "blocked": False
        }

    except Exception as e:
        generation.end(level="ERROR", status_message=str(e))
        raise HTTPException(status_code=500, detail=str(e))