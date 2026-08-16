# ============================================================================
# PROMPT TEMPLATES FOR THE YOUTUBE AI ASSISTANT
# ============================================================================

# ============================================================================
# SUMMARY PROMPT
# ============================================================================
# This prompt tells the LLM how to summarize a YouTube video transcript

SUMMARY_PROMPT = """You are an expert summarizer. Your task is to create a comprehensive yet concise summary of the following YouTube video transcript.

Please provide:
1. Main topic/subject of the video
2. Key points (3-5 most important takeaways)
3. Important details or statistics mentioned
4. Conclusion or final message

Keep the summary clear and well-structured. Use bullet points where appropriate.

Transcript:
{transcript}

Summary:"""