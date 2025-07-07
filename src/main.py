import asyncio

from utils import generate_report, read_logs, show_alerts


async def main():
    event_analyzer = None
    event_logger = None

    while True:
        print("\n=== Log Anomaly Analyzer Menu ===")
        print("1. Start processing")
        print("2. Show alerts")
        print("3. Generate report")
        print("4. Quit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            event_analyzer, event_logger = await read_logs("events.log")
            print("Processing completed.")
        elif choice == "2":
            if event_analyzer is None or event_logger is None:
                print("Please start processing first (option 1).")
            else:
                show_alerts(event_analyzer, event_logger)
        elif choice == "3":
            if event_analyzer is None:
                print("Please start processing first (option 1).")
            else:
                generate_report(event_analyzer)
                print("Report generated.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    asyncio.run(main())
