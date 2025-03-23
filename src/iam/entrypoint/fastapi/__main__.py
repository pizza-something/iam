from iam.entrypoint.common.uvicorn import run_dev


def main() -> None:
    run_dev("iam.entrypoint.fastapi.asgi:app")


if __name__ == "__main__":
    main()
