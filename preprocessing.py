import json
from llm_code import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path=None):
    """Reads raw LinkedIn posts, extracts metadata, unifies tags, and saves the processed output."""
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []

        for post in posts:
            
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

   
    unified_tags = get_unified_tags(enriched_posts)

    
    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    
    if processed_file_path:
        with open(processed_file_path, "w", encoding='utf-8') as outfile:
            json.dump(enriched_posts, outfile, indent=4, ensure_ascii=False)

    print(f"✅ Processed {len(enriched_posts)} posts saved to {processed_file_path}")



def extract_metadata(post: str):
    """Uses LLM to extract metadata such as line count, language, and tags from a LinkedIn post."""
    template = """
    Analyze the given LinkedIn post and return structured metadata as JSON.

    Required keys:
    - line_count: integer (number of lines in the post)
    - language: "English" or "Hinglish"
    - tags: array (max 2) of meaningful themes related to the post

    Tag examples:
    - Jobs, hiring, career → "Career"
    - Confidence, failure, growth → "Motivation"
    - Leadership, management → "Leadership"
    - Gratitude, mindfulness → "Life Lessons"
    - Learning, productivity → "Personal Growth"

    Return only JSON. Example:
    {{ "line_count": 5, "language": "English", "tags": ["Career", "Motivation"] }}

    Post:
    {post}
    """

    pt = PromptTemplate(input_variables=["post"], template=template)
    response = (pt | llm).invoke({"post": post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except Exception:
        raise OutputParserException("⚠️ Unable to parse metadata JSON output.")
    return res



def get_unified_tags(posts_with_metadata):
    """Unifies raw tags across multiple posts into a standardized tagging system."""
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post.get('tags', []))

    all_tags = ', '.join(unique_tags)

    template = """
    Unify similar tags from this list into standardized ones.

    Rules:
    - Merge similar ones:
      - "Jobseekers", "Career Growth" → "Career"
      - "Motivation", "Inspiration" → "Motivation"
      - "Leadership", "Teamwork" → "Leadership"
      - "Gratitude", "Mindfulness" → "Life Lessons"
      - "Personal Growth", "Self Improvement" → "Personal Growth"
    - Output only JSON mapping of original → unified tag.

    Example:
    {{
      "Jobseekers": "Career",
      "Inspiration": "Motivation"
    }}

    Tags:
    {tags}
    """

    pt = PromptTemplate(input_variables=["tags"], template=template)
    response = (pt | llm).invoke({"tags": all_tags})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except Exception:
        raise OutputParserException("⚠️ Unable to parse unified tags JSON output.")
    return res


if __name__ == "__main__":
    process_posts("data/raw_data.json", "data/processed_posts.json")