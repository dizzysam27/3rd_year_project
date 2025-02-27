import GUI
import GUItest

def main():
    try:
        #gui = GUI.App()
        #gui.run()
        #gui.show()

        processor = GUItest.ImageProcessor()
        processor.run()

        while True:
            pass

    except KeyboardInterrupt:
        # Cleanup on exit
        pass

if __name__ == "__main__":
    print("runnin")
    main()