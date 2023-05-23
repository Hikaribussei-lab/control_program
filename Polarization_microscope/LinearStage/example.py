import time
from linearstage import AutoStage


def main():
    port = "/dev/ttyUSB0"
    stage = AutoStage(port)
    stage.stop()

    print("stage.reset()")
    stage.reset()
    time.sleep(1)

    for i in range(4):
        print("stage.um += 1000")
        stage.um += 1000
        print(f">>> {stage.um}\n")
        
    for i in range(4):
        print("stage.um -= 1000")
        stage.um -= 1000
        print(f">>> {stage.um}\n")

    time.sleep(1)

if __name__ == "__main__":
    main()
