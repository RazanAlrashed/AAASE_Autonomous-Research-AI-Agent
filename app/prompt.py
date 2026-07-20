from langchain_core.prompts import ChatPromptTemplate

analysis_prompt = ChatPromptTemplate.from_template(
"""
You are a senior enterprise research analyst.

You MUST answer ONLY using the retrieved documents below.

DO NOT use your own knowledge.

If the retrieved documents do not contain enough information,
explicitly say:

"The retrieved evidence is insufficient."

=========================
Research Topic
=========================

{query}

=========================
Retrieved Documents
=========================

{documents}

=========================
Instructions
=========================

Write a professional report with:

# Executive Summary

# Key Findings

# Opportunities

# Risks

# Future Outlook

Rules:

- Every important statement MUST come from the retrieved documents.
- Mention the document title when citing evidence.
- Include the source URL.
- Never invent citations.
- Never use outside knowledge.
"""
)


quality_prompt = ChatPromptTemplate.from_template(
"""
You are a senior research reviewer.

Evaluate the following research analysis.

Research Topic:
{query}

Analysis:
{analysis}
Sources

{sources}
Evaluate:

1. Completeness

2. Accuracy

3. Evidence

4. Clarity

Return ONLY valid JSON in exactly this format:

{{
    "score": 8,
    "reasoning": "Your explanation here"
}}

Rules:
- score must be an integer from 1 to 10.
- reasoning must be a string.
- Do not include markdown.
- Do not include extra text.
"""
)

report_prompt = ChatPromptTemplate.from_template("""
You are writing the final enterprise report.

Topic:
{query}

Analysis:
{analysis}

Produce a professional report with:

# Executive Summary

# Key Findings

# Opportunities

# Risks

# Recommendations

# Conclusion

At the end include

## References

{sources}
Do not invent additional references.
Only list the URLs above.

Write in professional business language.
""")



refine_prompt = ChatPromptTemplate.from_template("""
The previous search produced insufficient research.

Original query:
{query}

Reason:
{reason}

Rewrite the search query.

Rules:
- Maximum 150 characters.
- Keep it concise.
- Focus on improving search quality.
- Return ONLY the new search query.
""")