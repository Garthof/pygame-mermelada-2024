def main():
    from engine import Engine

    with Engine() as engine:
        engine.run()


if __name__ == "__main__":
    main()
