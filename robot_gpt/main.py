from robot_gpt.robot import RobotGPT


def main() -> None:
    robot = RobotGPT()

    for i in range(5):
        robot.run()


if __name__ == "__main__":
    main()
