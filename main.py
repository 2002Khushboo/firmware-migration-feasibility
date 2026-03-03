import sys
from scanner import scan_project
from detector import detect_features
from rules import generate_migration_notes
from report import generate_report


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_stm_project>")
        sys.exit(1)

    project_path = sys.argv[1]

    print("Scanning STM project...")
    files_content = scan_project(project_path)

    print("Detecting STM features...")
    detected_data = detect_features(files_content)

    print("Generating migration guidance...")
    migration_notes = generate_migration_notes(detected_data)

    print("Creating report...")
    generate_report(detected_data, migration_notes)

    print("Done. Check migration_report.txt")


if __name__ == "__main__":
    main()