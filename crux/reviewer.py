from crux import github, fab

def parse_and_post(repo, pr_number, file_path, fab_text, commit_id, token):
    if "No rule violations found." in fab_text:
        print(f" No violations in {file_path}")
        return

    lines = fab_text.split('\n')
    violation = {}
    for line in lines:
        line = line.strip()
        if line.startswith("violation number"):
            if violation and "Line Number" in violation:
                github.post_comment(
                    repo, pr_number, file_path, violation["Line Number"],
                    f"**Rule**: {violation['Rule Name']}\n**Severity**: {violation['Severity']}\n**Explanation**: {violation['Explanation']}\n**Suggested Fix**: {violation['Suggested Fix']}",
                    commit_id, token
                )
                violation.clear()
        elif line.startswith("Rule Name:"):
            violation["Rule Name"] = line.split(":", 1)[1].strip()
        elif line.startswith("Severity:"):
            violation["Severity"] = line.split(":", 1)[1].strip()
        elif line.startswith("Line Number:"):
            try:
                violation["Line Number"] = int(line.split(":", 1)[1].strip())
            except:
                violation["Line Number"] = 1
        elif line.startswith("Explanation:"):
            violation["Explanation"] = line.split(":", 1)[1].strip()
        elif line.startswith("Suggested Fix:"):
            violation["Suggested Fix"] = line.split(":", 1)[1].strip()

    if violation and "Line Number" in violation:
        github.post_comment(
            repo, pr_number, file_path, violation["Line Number"],
            f"**Rule**: {violation['Rule Name']}\n**Severity**: {violation['Severity']}\n**Explanation**: {violation['Explanation']}\n**Suggested Fix**: {violation['Suggested Fix']}",
            commit_id, token
        )

def review(repo, pr_number, commit_id, token):
    files = github.get_pr_files(repo, pr_number, token)
    for file in files:
        if file["status"] in ["added", "modified"]:
            path = file["filename"]
            print(f" Reviewing {path}")
            content = github.get_file_content(repo, path, commit_id, token)
            if content:
                review_text = fab.get_fab_review(path, content)
                parse_and_post(repo, pr_number, path, review_text, commit_id, token)
