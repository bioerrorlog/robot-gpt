from robot_gpt.robot import RobotGPT


def main() -> None:
    robot = RobotGPT()

    robot.recognize(45, -30)

    message = robot.call_gpt()
    print(f"RobotGPT says: {message}")


if __name__ == "__main__":
    main()
