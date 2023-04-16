from robot_gpt.robot import RobotGPT


def main() -> None:
    with RobotGPT() as robot:
        robot.look()
        robot.recognize()

        # OpenAI API rate limit: 3 / min.
        for i in range(3):
            robot.call_and_recognize()

        robot.talk("Summarize your surroundings.")


if __name__ == "__main__":
    main()
