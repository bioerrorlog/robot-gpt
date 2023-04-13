from robot_gpt.robot import RobotGPT


def main() -> None:
    robot = RobotGPT()
    robot.look()
    robot.recognize()

    for i in range(3):
        robot.call_and_recognize()


if __name__ == "__main__":
    main()
