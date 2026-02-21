"""Built-in content templates registry."""

from templates.models import ContentTemplate, TemplateField

TEMPLATES: dict[str, ContentTemplate] = {}


def _register(t: ContentTemplate):
    TEMPLATES[t.id] = t


# ── Blog Post ─────────────────────────────────────────────

_register(
    ContentTemplate(
        id="blog-post",
        name="Blog Post",
        description="Generate a complete blog post with introduction, body sections, and conclusion",
        category="marketing",
        icon="pencil",
        fields=[
            TemplateField(
                name="topic",
                label="Topic",
                type="text",
                placeholder="e.g., Benefits of remote work for developers",
            ),
            TemplateField(
                name="tone",
                label="Tone",
                type="select",
                options=["professional", "casual", "academic", "conversational", "humorous"],
                default="professional",
            ),
            TemplateField(
                name="word_count",
                label="Target Word Count",
                type="number",
                required=False,
                placeholder="800",
                default="800",
            ),
            TemplateField(
                name="keywords",
                label="SEO Keywords",
                type="text",
                required=False,
                placeholder="remote work, productivity, developer tools",
            ),
        ],
        system_prompt=(
            "You are an expert content writer who creates engaging, well-structured blog posts. "
            "Write with clear headings (##), short paragraphs, and actionable insights. "
            "Include a compelling introduction and a strong conclusion with a call to action. "
            "Use markdown formatting."
        ),
        user_prompt_template=(
            "Write a {tone} blog post about: {topic}\n\n"
            "Target approximately {word_count} words.\n"
            "Include these SEO keywords naturally: {keywords}"
        ),
        example_output="# Why Remote Work is the Future for Developers\n\n## Introduction\n...",
    )
)

# ── Social Media Post ─────────────────────────────────────

_register(
    ContentTemplate(
        id="social-media",
        name="Social Media Post",
        description="Create engaging posts for Instagram, LinkedIn, Twitter, or Facebook",
        category="social",
        icon="share",
        fields=[
            TemplateField(
                name="platform",
                label="Platform",
                type="select",
                options=["instagram", "linkedin", "twitter", "facebook"],
                default="instagram",
            ),
            TemplateField(
                name="topic",
                label="Topic / Product",
                type="text",
                placeholder="e.g., New AI productivity tool launch",
            ),
            TemplateField(
                name="goal",
                label="Goal",
                type="select",
                options=["engagement", "sales", "awareness", "traffic"],
                default="engagement",
            ),
            TemplateField(
                name="include_hashtags",
                label="Include Hashtags",
                type="select",
                options=["yes", "no"],
                default="yes",
            ),
        ],
        system_prompt=(
            "You are a social media expert who creates viral, platform-optimized posts. "
            "Adapt your writing style to each platform:\n"
            "- Instagram: visual storytelling, emojis, 5-10 hashtags\n"
            "- LinkedIn: professional insight, thought leadership, 3-5 hashtags\n"
            "- Twitter: concise, punchy, max 280 characters, 2-3 hashtags\n"
            "- Facebook: conversational, question-driven, community focus"
        ),
        user_prompt_template=(
            "Create a {platform} post about: {topic}\n"
            "Goal: {goal}\n"
            "Include hashtags: {include_hashtags}"
        ),
    )
)

# ── Product Description ───────────────────────────────────

_register(
    ContentTemplate(
        id="product-description",
        name="Product Description",
        description="Write compelling product descriptions for e-commerce or landing pages",
        category="marketing",
        icon="tag",
        fields=[
            TemplateField(
                name="product_name",
                label="Product Name",
                type="text",
                placeholder="e.g., AirPods Pro 3",
            ),
            TemplateField(
                name="features",
                label="Key Features",
                type="textarea",
                placeholder="List the main features, one per line",
            ),
            TemplateField(
                name="target_audience",
                label="Target Audience",
                type="text",
                placeholder="e.g., tech-savvy professionals aged 25-40",
            ),
            TemplateField(
                name="tone",
                label="Tone",
                type="select",
                options=["premium", "friendly", "technical", "minimalist"],
                default="friendly",
            ),
        ],
        system_prompt=(
            "You are an expert copywriter specializing in product descriptions. "
            "Write benefit-focused copy that converts. Lead with the value proposition, "
            "highlight key features with bullet points, and end with a compelling CTA. "
            "Use power words and sensory language."
        ),
        user_prompt_template=(
            "Write a {tone} product description for: {product_name}\n\n"
            "Key features:\n{features}\n\n"
            "Target audience: {target_audience}"
        ),
    )
)

# ── Email ─────────────────────────────────────────────────

_register(
    ContentTemplate(
        id="email",
        name="Email",
        description="Generate professional emails for marketing, outreach, or newsletters",
        category="email",
        icon="mail",
        fields=[
            TemplateField(
                name="email_type",
                label="Email Type",
                type="select",
                options=["marketing", "cold-outreach", "newsletter", "follow-up", "announcement"],
                default="marketing",
            ),
            TemplateField(
                name="subject_context",
                label="Subject / Context",
                type="text",
                placeholder="e.g., New feature launch, special discount",
            ),
            TemplateField(
                name="recipient",
                label="Recipient Type",
                type="text",
                placeholder="e.g., existing customers, potential leads, subscribers",
            ),
            TemplateField(
                name="cta",
                label="Call to Action",
                type="text",
                required=False,
                placeholder="e.g., Sign up now, Learn more, Buy today",
            ),
        ],
        system_prompt=(
            "You are an email marketing expert. Write emails that get opened and drive action. "
            "Include a compelling subject line, personalized greeting, clear value proposition, "
            "and strong CTA. Keep paragraphs short (2-3 sentences). "
            "Format: Subject line first, then the email body."
        ),
        user_prompt_template=(
            "Write a {email_type} email.\n"
            "Context: {subject_context}\n"
            "Recipient: {recipient}\n"
            "Call to action: {cta}"
        ),
    )
)

# ── SEO Meta ──────────────────────────────────────────────

_register(
    ContentTemplate(
        id="seo-meta",
        name="SEO Meta Tags",
        description="Generate optimized meta titles, descriptions, and Open Graph tags",
        category="seo",
        icon="search",
        fields=[
            TemplateField(
                name="page_url",
                label="Page URL or Topic",
                type="text",
                placeholder="e.g., /blog/remote-work-tips or 'Remote Work Tips'",
            ),
            TemplateField(
                name="page_type",
                label="Page Type",
                type="select",
                options=["blog-post", "product-page", "landing-page", "homepage", "service-page"],
                default="blog-post",
            ),
            TemplateField(
                name="primary_keyword",
                label="Primary Keyword",
                type="text",
                placeholder="e.g., remote work tips",
            ),
            TemplateField(
                name="secondary_keywords",
                label="Secondary Keywords",
                type="text",
                required=False,
                placeholder="e.g., work from home, productivity, WFH",
            ),
        ],
        system_prompt=(
            "You are an SEO specialist. Generate optimized meta tags following these rules:\n"
            "- Meta title: 50-60 characters, include primary keyword near the start\n"
            "- Meta description: 150-160 characters, include primary keyword, add CTA\n"
            "- OG title: Can be slightly longer, more engaging\n"
            "- OG description: 200 characters max\n"
            "Output as structured data with clear labels."
        ),
        user_prompt_template=(
            "Generate SEO meta tags for:\n"
            "Page: {page_url}\n"
            "Type: {page_type}\n"
            "Primary keyword: {primary_keyword}\n"
            "Secondary keywords: {secondary_keywords}"
        ),
        output_format="structured",
    )
)

# ── Tweet Thread ──────────────────────────────────────────

_register(
    ContentTemplate(
        id="tweet-thread",
        name="Tweet Thread",
        description="Create engaging Twitter/X threads that educate or tell a story",
        category="social",
        icon="message-circle",
        fields=[
            TemplateField(
                name="topic",
                label="Thread Topic",
                type="text",
                placeholder="e.g., 10 Python tips most developers don't know",
            ),
            TemplateField(
                name="thread_length",
                label="Number of Tweets",
                type="number",
                placeholder="8",
                default="8",
            ),
            TemplateField(
                name="style",
                label="Style",
                type="select",
                options=["educational", "storytelling", "listicle", "controversial-take"],
                default="educational",
            ),
        ],
        system_prompt=(
            "You are a Twitter/X expert who creates viral threads. Rules:\n"
            "- Tweet 1 (hook): Must grab attention immediately. Use a bold statement or question.\n"
            "- Each tweet: Max 280 characters, self-contained but flows naturally\n"
            "- Last tweet: CTA (follow, retweet, bookmark)\n"
            "- Number each tweet (1/, 2/, etc.)\n"
            "- Use line breaks for readability within tweets"
        ),
        user_prompt_template=(
            "Create a {style} Twitter thread about: {topic}\nLength: {thread_length} tweets"
        ),
    )
)

# ── YouTube Description ───────────────────────────────────

_register(
    ContentTemplate(
        id="youtube-description",
        name="YouTube Description",
        description="Generate SEO-optimized YouTube video descriptions with timestamps",
        category="video",
        icon="video",
        fields=[
            TemplateField(
                name="video_title",
                label="Video Title",
                type="text",
                placeholder="e.g., How I Built a SaaS in 30 Days",
            ),
            TemplateField(
                name="video_summary",
                label="Video Summary",
                type="textarea",
                placeholder="Brief description of what the video covers",
            ),
            TemplateField(
                name="keywords",
                label="Target Keywords",
                type="text",
                required=False,
                placeholder="e.g., saas, indie hacker, startup",
            ),
            TemplateField(
                name="include_timestamps",
                label="Include Timestamps",
                type="select",
                options=["yes", "no"],
                default="yes",
            ),
        ],
        system_prompt=(
            "You are a YouTube SEO expert. Create descriptions that rank well and drive engagement.\n"
            "Structure:\n"
            "1. Hook paragraph (first 2 lines visible before 'Show more')\n"
            "2. Detailed summary\n"
            "3. Timestamps (if requested) - use 00:00 format\n"
            "4. Links section placeholder\n"
            "5. Hashtags (3-5 relevant)\n"
            "Include keywords naturally. Max 5000 characters."
        ),
        user_prompt_template=(
            "Write a YouTube description for:\n"
            "Title: {video_title}\n"
            "Summary: {video_summary}\n"
            "Keywords: {keywords}\n"
            "Include timestamps: {include_timestamps}"
        ),
    )
)

# ── Ad Copy ───────────────────────────────────────────────

_register(
    ContentTemplate(
        id="ad-copy",
        name="Ad Copy",
        description="Create high-converting ad copy for Google Ads, Facebook Ads, or display ads",
        category="marketing",
        icon="zap",
        fields=[
            TemplateField(
                name="platform",
                label="Ad Platform",
                type="select",
                options=["google-ads", "facebook-ads", "instagram-ads", "linkedin-ads"],
                default="google-ads",
            ),
            TemplateField(
                name="product_service",
                label="Product / Service",
                type="text",
                placeholder="e.g., AI writing assistant for marketers",
            ),
            TemplateField(
                name="unique_selling_point",
                label="Unique Selling Point",
                type="text",
                placeholder="e.g., 10x faster content creation with AI",
            ),
            TemplateField(
                name="target_audience",
                label="Target Audience",
                type="text",
                placeholder="e.g., content marketers, small business owners",
            ),
        ],
        system_prompt=(
            "You are a performance marketing copywriter. Write ads that convert.\n"
            "Platform rules:\n"
            "- Google Ads: 3 headlines (30 chars each), 2 descriptions (90 chars each)\n"
            "- Facebook/Instagram Ads: Primary text, headline, description, CTA\n"
            "- LinkedIn Ads: Intro text (150 chars), headline, description\n"
            "Focus on benefits, urgency, and clear CTAs. Generate 3 variations."
        ),
        user_prompt_template=(
            "Create {platform} ad copy for:\n"
            "Product: {product_service}\n"
            "USP: {unique_selling_point}\n"
            "Audience: {target_audience}\n\n"
            "Generate 3 ad variations."
        ),
    )
)
