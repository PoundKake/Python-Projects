import datetime
import datetime as dtutil

START_TIME = "2019-09-15T23:03:37.760159Z"
STOP_TIME = "2019-09-15T23:13:52.652860Z"

class datetimeTest:
    def __init__(self):
        pass

    # Converting starttime datetime
    def convert_starttime_datetime(self, starttimeDatetime: str):
        """
        Converts starttime from datetime format to string. This is needed for easier comparison
        when querind database for approporiate video files.

        :param starttimeDatetime: The start time in datetime formate represented as a string.
        :return: datetime
        """
        # yourdate = dtutil.parse(starttimeDatetime)
        datetimeObj = dtutil.datetime.strptime(starttimeDatetime, "%Y-%m-%dT%H:%M:%S.%fZ")

        return datetimeObj

    # Converting stoptime datetime
    def convert_stoptime_datetime(self, stoptimeDatetime: str):
        """
        Converts stoptime from datetime format to string. This is needed for easier comparison
        when querind database for approporiate video files.

        :param stoptimeDatetime: The stop time in datetime formate represented as a string.
        :return: datetime
        """
        datetimeObj = dtutil.datetime.strptime(stoptimeDatetime, "%Y-%m-%dT%H:%M:%S.%fZ")
        # print(type(datetimeObj))

        return datetimeObj

    # Formatting datetime.
    def format_datetime(self, datetimeString: datetime.datetime):
        """
        Converts stoptime from datetime format to string. This is needed for easier comparison
        when querind database for approporiate video files.

        :param datetimeString: The datetime string onject to reformat.
        :return:
        """
        h = datetimeString.time().hour
        m = datetimeString.time().minute
        s = datetimeString.time().second

        time = str("{}{}{}" .format(h, m, s))
        str2int = lambda s: int(s) # converts string to integer

        return str2int(time)

dt = datetimeTest()
# print("Hello World")
# print("Start time is: {}" .format(dt.convert_starttime_datetime(START_TIME)))
# print("Stop time is: {}" .format(dt.convert_stoptime_datetime(STOP_TIME)))
print(dt.format_datetime(dt.convert_starttime_datetime(START_TIME)))
print(dt.format_datetime(dt.convert_starttime_datetime(STOP_TIME)))
