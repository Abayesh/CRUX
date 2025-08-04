from . import github, fab
from .config import GITHUB_REPO

def parse_and_comment(repo, pr_number, path, fab_text, head_sha):
    if "No rule violations found." in fab_text:
        print(f"  ✅ No violations in {path}")
        return

    lines = fab_text.split('\n')
    violation = {}

    for line in lines:
        line = line.strip()
        if line.startswith("violation number"):
            if violation.get("Line Number"):
                try:
                    line_no = int(str(violation["Line Number"]).split('-')[0])
                    message = f"**Rule**: {violation['Rule Name']}\n**Severity**: {violation['Severity']}\n**Explanation**: {violation['Explanation']}\n**Suggested Fix**: {violation['Suggested Fix']}"
                    github.post_review_comment(repo, pr_number, path, line_no, message, head_sha)
                except Exception:
                    pass
            violation.clear()
        elif line.startswith("Rule Name:"):
            violation["Rule Name"] = line.replace("Rule Name:", "").strip()
        elif line.startswith("Severity:"):
            violation["Severity"] = line.replace("Severity:", "").strip()
        elif line.startswith("Line Number:"):
            violation["Line Number"] = line.replace("Line Number:", "").strip()
        elif line.startswith("Explanation:"):
            violation["Explanation"] = line.replace("Explanation:", "").strip()
        elif line.startswith("Suggested Fix:"):
            violation["Suggested Fix"] = line.replace("Suggested Fix:", "").strip()

def review_pr(pr):
    pr_number = pr['number']
    pr_title = pr['title']
    head_sha = pr['head']['sha']

    print(f"\n🔍 Reviewing PR #{pr_number}: {pr_title}")
    for file in github.get_pr_files(GITHUB_REPO, pr_number):
        if file['status'] in ['added', 'modified']:
            path = file['filename']
            print(f"  📄 Reviewing {path}...")
            content = github.get_file_content(GITHUB_REPO, path, head_sha)
            if content:
                fab_text = fab.send_to_fab(path, content)
                parse_and_comment(GITHUB_REPO, pr_number, path, fab_text, head_sha)

def review_all_open_pr():
    prs = github.get_open_prs(GITHUB_REPO)
    for pr in prs:
        review_pr(pr)
