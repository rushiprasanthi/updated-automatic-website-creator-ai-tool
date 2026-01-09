import re
import markdown2
from pathlib import Path
from jinja2 import Template
from urllib.parse import quote_plus

# Paths
TEMPLATE_FILE = "template.html"
OUTPUT_DIR = Path("Blog/Pages")

# Ensure output folder exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def slugify(value: str) -> str:
    """Simple slugify: keep letters, numbers, hyphen and underscore."""
    value = (value or "").strip().lower()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^a-z0-9\-_]", "", value)
    return value or "post"


def validate_email(email: str) -> str:
    email = (email or "").strip()
    if not EMAIL_REGEX.match(email):
        raise ValueError("Invalid email format")
    return email


def load_template():
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return Template(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file '{TEMPLATE_FILE}' not found. Please create it in the working directory.")


def generate_article(title, slug, meta_desc, md_content, name, company, phone, email, services):
    template = load_template()
    html_body = markdown2.markdown(md_content)

    safe_slug = slugify(slug or title)
    job_q = quote_plus(title or "")

    # Fill template with blog + contact + services data
    html_full = template.render(
        title=title,
        meta=meta_desc,
        content=html_body,
        contact_name=name,
        contact_company=company,
        contact_phone=phone,
        contact_email=email,
        services=services,
        slug=safe_slug,
        job_q=job_q
    )

    output_file = OUTPUT_DIR / f"{safe_slug}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_full)
    print(f"\n✅ Article saved as: {output_file}")


def main():
    print("\U0001F4C4 Blog Post Generator\n")

    title = input("Enter article title: ").strip()
    slug = input("Enter slug (filename without .html) [leave blank to auto from title]: ").strip()
    meta = input("Enter meta description: ").strip()

    print("\n\U0001F464 Contact Information:")
    name = input("Your Name: ").strip()
    company = input("Company Name: ").strip()
    phone = input("Phone Number: ").strip()

    # email validation loop (ensures syntactically valid email)
    while True:
        try:
            email_input = input("Gmail ID (owner email - will receive applications): ").strip()
            email = validate_email(email_input)
            break
        except ValueError as e:
            print("❌", e)

    print("\n\U0001F6E0️ Services Offered:")
    try:
        service_count = int(input("How many services do you want to list? "))
        if service_count < 0:
            service_count = 0
    except ValueError:
        service_count = 0

    services = []
    for i in range(service_count):
        print(f"\n🔹 Service {i+1}")
        s_title = input("Service Title: ").strip()
        s_desc = input("Service Description: ").strip()
        # use key 'description' to match template
        services.append({"title": s_title, "description": s_desc})

    print("\n📝 Paste your Markdown content. End with a single line: END")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    md_content = "\n".join(lines)

    generate_article(title, slug, meta, md_content, name, company, phone, email, services)


if __name__ == "__main__":
    main()
