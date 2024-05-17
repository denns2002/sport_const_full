import spreads as s


def main():
    services = s.start_services('credentials.json')
    batch_update_structure_body = {"requests": []}
    batch_update_values_data = []
    s.create_sample(
        "Ведомость",
        services['service'],
        services['drive_service'],
        20,
        batch_update_values_data,
        batch_update_structure_body,
    )


if __name__ == "__main__":
    main()
