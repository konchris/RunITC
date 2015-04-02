"""The ITC Module.

"""
import visa


class ITCDevice(object):

    def __init__(self):
        super(ITCDevice, self).__init__()
        self.resource = None


def main():
    itc = ITCDevice()
    print(itc)



if __name__ == "__main__":
    main()
