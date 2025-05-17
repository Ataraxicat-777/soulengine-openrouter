# deployment_ready_generator.py
# Purpose: Unified deployment and sync script with full auto-ingestion capabilities and manual entry fallback
# Enhanced for seamless syncing and export-ready formats

import os
import json
from datetime import datetime

# Base directory
BASE = os.path.dirname(os.path.abspath(__file__))
DESKTOP_DIR = os.path.join(BASE, "SOULENGINE-DESKTOP")

LOG_PATH = os.path.join(DESKTOP_DIR, "soulengine_log.json")
ARCHIVE_PATH = os.path.join(DESKTOP_DIR, "soulengine_archive.json")
DEPLOY_PATH = os.path.join(DESKTOP_DIR, "soulengine_deployments.json")
RENDER_EXPORT_PATH = os.path.join(DESKTOP_DIR, "render_ready.json")


def ensure_file(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([], f)

def read_json(path):
    ensure_file(path)
    with open(path, 'r') as f:
        return json.load(f)

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def extract_construct_from_text(text):
    lines = text.splitlines()
    name = "Untitled Construct"
    traits = []
    for line in lines:
        if line.lower().startswith("# idea") or "idea:" in line.lower():
            name = line.split(":", 1)[1].strip()
        elif line.lower().startswith("# traits") or "traits:" in line.lower():
            trait_line = line.split(":", 1)[1].strip()
            traits = [t.strip() for t in trait_line.split(",") if t.strip()]
    return {
        "idea": name,
        "traits": traits,
        "score": round(1.0 + len(traits) * 0.1, 2),
        "verdict": "APPROVED" if len(traits) >= 5 else "REVIEW",
        "source": "script_import",
        "timestamp": datetime.utcnow().isoformat()
    }

def auto_ingest_constructs():
    ingested = []
    for file in os.listdir(BASE):
        if file.endswith(('.py', '.html', '.txt', '.json')) and not file.startswith("soulengine_"):
            path = os.path.join(BASE, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    if file.endswith(".json"):
                        data = json.loads(content)
                        ingested.extend(data if isinstance(data, list) else [data])
                    else:
                        construct = extract_construct_from_text(content)
                        ingested.append(construct)
                except Exception as e:
                    print(f"❌ Failed to parse {file}: {e}")
    return ingested

def generate_deployments_from_log():
    log_data = read_json(LOG_PATH)
    deploy_data = []
    for entry in log_data:
        if entry.get("verdict") == "APPROVED":
            usd_value = round(entry["score"] * 42.0, 2)
            deploy = {
                "id": entry.get("id", entry["idea"].lower().replace(" ", "_")),
                "name": entry["idea"],
                "score": entry["score"],
                "usd_value": usd_value,
                "traits": entry["traits"],
                "description": f"Deployment Summary for {entry['idea']}\n- Score: {entry['score']}\n- Estimated Value: ${usd_value} USD\n- Primary Traits: {', '.join(entry['traits'][:5])}\n- Description: This construct is designed for deployment in systems requiring traits such as {', '.join(entry['traits'])}. It is expected to demonstrate advanced resilience, adaptability, and ethically-aligned performance.\n- Recommended Use: Use this construct in experimental governance models, recursive learning frameworks, or intelligent agent mesh systems.",
                "tier": "ultra" if entry["score"] >= 4.0 else "standard",
                "aliases": [entry["idea"][:40] + "..."],
                "evolved_from": entry.get("evolved_from", []),
                "timestamp": entry.get("timestamp"),
                "trait_info": entry.get("trait_info", [])
            }
            deploy_data.append(deploy)
            print("\n🚀 Generated Deployment:")
            print(json.dumps(deploy, indent=2))
    write_json(DEPLOY_PATH, deploy_data)
    write_json(RENDER_EXPORT_PATH, deploy_data)
    print(f"\n✅ Rebuilt deployments from {len(deploy_data)} approved ideas in log.")

def refresh_archive_from_log():
    log_data = read_json(LOG_PATH)
    write_json(ARCHIVE_PATH, log_data)
    print(f"✅ Archive synced with {len(log_data)} total entries from log.")

if __name__ == "__main__":
    print("🔁 Full Deployment & Sync: single source control via soulengine_log.json...")
    ensure_file(LOG_PATH)
    ensure_file(ARCHIVE_PATH)
    ensure_file(DEPLOY_PATH)
    ensure_file(RENDER_EXPORT_PATH)

    log_data = read_json(LOG_PATH)
    choice = input("Mode (file | manual | all): ").strip().lower()

    if choice == "file":
        target_file = input("Enter file to ingest: ").strip()
        path = os.path.join(BASE, target_file)
        if not os.path.isfile(path):
            print(f"❌ File not found: {target_file}")
        else:
            constructs = []
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if path.endswith(".json"):
                        data = json.loads(content)
                        constructs = data if isinstance(data, list) else [data]
                    else:
                        constructs = [extract_construct_from_text(content)]
                log_data.extend(constructs)
                write_json(LOG_PATH, log_data)
                print(f"✅ Imported {len(constructs)} construct(s) from {target_file}.")
            except Exception as e:
                print(f"❌ Failed to process {target_file}: {e}")

    elif choice == "manual":
        idea = input("Enter idea name: ").strip()
        traits = input("Enter traits (comma-separated): ").split(",")
        traits = [t.strip() for t in traits if t.strip()]
        entry = {
            "idea": idea,
            "traits": traits,
            "score": round(1.0 + len(traits) * 0.1, 2),
            "verdict": "APPROVED" if len(traits) >= 5 else "REVIEW",
            "source": "manual_entry",
            "timestamp": datetime.utcnow().isoformat()
        }
        log_data.append(entry)
        write_json(LOG_PATH, log_data)
        print("✅ Manual entry added.")

    else:
        constructs = auto_ingest_constructs()
        if constructs:
            log_data.extend(constructs)
            write_json(LOG_PATH, log_data)
            print(f"✅ Imported {len(constructs)} new constructs from file(s).")

    refresh_archive_from_log()
    generate_deployments_from_log()
    print("✅ Unified deployment+sync complete.")
