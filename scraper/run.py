import argparse

from scraper.state import load_state, save_state
from scraper.utils import fetch_html
from scraper.notify import send_email
from scraper.sites import SITE_MODULES


def build_email_body(new_report):
    lines = ["New proposal links were found:\n"]
    for site_name, urls in new_report.items():
        lines.append(f"{site_name} ({len(urls)} new):")
        for url in urls:
            lines.append(f"- {url}")
        lines.append("")
    return "\n".join(lines)


def build_email_subject(new_report):
    total = sum(len(urls) for urls in new_report.values())
    sites = ", ".join(new_report.keys())
    return f"New proposal alert: {total} link(s) from {sites}"


def main(dry_run=False):
    state = load_state()
    new_report = {}

    for site in SITE_MODULES:
        print(f"Checking {site.SITE_NAME}...")
        html = fetch_html(site.SITE_URL)
        links = site.extract_links(html)

        previous_links = set(state.get(site.SITE_NAME, []))
        current_links = set(links)
        new_links = sorted(current_links - previous_links)

        if new_links:
            new_report[site.SITE_NAME] = new_links

        state[site.SITE_NAME] = sorted(previous_links | current_links)

    save_state(state)

    if not new_report:
        print("No new proposal links found.")
        return

    subject = build_email_subject(new_report)
    body = build_email_body(new_report)

    if dry_run:
        print("DRY RUN: email not sent.")
        print(f"Subject: {subject}")
        print(body)
        return

    send_email(subject, body)
    print("Notification sent.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the proposal monitor")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not send email, only print detected new links",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run)
