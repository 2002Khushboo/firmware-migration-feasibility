def generate_report(detected, notes):

    with open("migration_report.txt", "w") as f:
        f.write("STM to TI Migration Analysis Report\n")
        f.write("=================================\n\n")

        f.write("Detected Features:\n")
        for key, value in detected.items():
            f.write(f"{key}: {value}\n")

        f.write("\nMigration Guidance:\n")
        for note in notes:
            f.write("- " + note + "\n")