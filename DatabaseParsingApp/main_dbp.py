# Imports
import sqlite3
from sqlite3 import Error
import datetime as dtutil
import json

# Global Variables
camDat = None
filenameList = None

# Main class definition
# 
# reference: https://www.sqlitetutorial.net/sqlite-python/creating-database/
# reference: https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
class main_dbp_class:
    
    # default constructor
    def __init__(self, cameraName: str, startTime: int, endTime: int):
        """
        main_dbp_class Class constructor

        :param cameraName: name of the camera to being used.
        :param startTime: start time of desired capture.
        :param endTime: end time of desired capture.
        """
        path = "camera_recording\\%s\\" % cameraName

        self.filenameList = {}
        self.filenameList['data'] = []

        self.camDat = {
            'cameraName': cameraName,
            'startTime': str(startTime),
            'endTime': str(endTime),
            'path': path
        }

        with open('filenameList.json', 'w') as outfile:
            json.dump(self.filenameList, outfile)

        return

    # Create a database connection
    def create_connection(self, dbfile):
        """
        create a database connection to a SQLite database.

        :param dbfile: The database file to connect to.
        :return: Connection object or None.
        """
        conn = None
        try:
            print("Attempting to connect to database ...")
            conn = sqlite3.connect(dbfile)
            print("PySQLite verison used: %s" % (sqlite3.version))
        except Error as e:
            print("Error: %s" % e)

        print("Connection Successful!\n")
        return conn

    # Find desired recording_action_id from recordign_actions table.
    def find_recording_action_id(self, conn, recordingActionTrigger: str):
        """
        Find desired recording_action_id in recording_actions table from recordingActionTrigger

        :param conn: the connection object
        :param recordingActionTrigger: the desired trigger to find the needed recording action id as a str
        :return recording_action_id: the desired action id based off of constraints.
        """
        cur = conn.cursor()
        # grab the desired recording id from the recording_events table.
        cur.execute("SELECT id FROM recording_actions WHERE action_name=?", (recordingActionTrigger,))
        row = cur.fetchone()
        recording_action_id = row[0]
        # print(recording_action_id)

        return recording_action_id

    # Find desired recording_event_id from recording_events table.
    def find_recording_event_id(self, conn, recordingActionTrigger: str):
        """
        Find desired recording_event_id in recordings table from recordingEventTrigger

        :param conn: the connection object
        :param recordingActionTrigger: the desired trigger to find the needed recording_event_id as a str
        :return recording_event_id: the desired events id based off of constraints
        """
        cur = conn.cursor()

        # grab the desired recording id from the recording_events table.
        cur.execute("SELECT id FROM recording_events WHERE event_name=?", (recordingActionTrigger,))
        row = cur.fetchone()
        recording_event_id = row[0]
        # print(recording_event_id)

        return recording_event_id

    # Query selected recording_id in recording table.
    def find_recording_id(self, conn, recordingEventID: str, recordingActionID: str):
        """
        Query select rows in the recordings table according to recordingActionID and recordingEventID.

        :param conn: the connection object
        :param recordingActionID: the recording action id used to query recordings table.
        :param recordingEventID: the recording event id used to query recordings table.
        :return recording_id: the desired recording id based off of constraints.
        """
        cur = conn.cursor()

        # grab the desired recording_id from the recordings table.
        cur.execute("SELECT * FROM recordings WHERE recording_event_id=? AND recording_action_id=?" , (recordingEventID,recordingActionID,))
        row = cur.fetchone()

        recording_id = row[0]
        self.camDat['path'] += "%s\\%s" % (row[2], row[1])
        # print(recording_id) # test to make sure this is what you want

        return recording_id

    # Query all recordings in database wtih recording_id constraint.
    def query_recording_id_blocks(self, conn, recordingID: str):
        """
        Query all rows in the blocks table to match recording_id constraint.

        :param conn: the connection object.
        :param recordingID: recording_id constraint for query.
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM blocks WHERE recording_id=?", (recordingID,))

        rows = cur.fetchall()

        for row in rows:
            print(row)
            # print("\n")

    # Query all recordings in database with startTime, endTime and recording_id constraints.
    def query_recording_id_time_blocks(self, conn, recordingID: str, startTimeConstraint: str, endTimeConstraint: str):
        """
        Query all rows in the blocks table to match recording_id, start and stop time constraints.

        :param conn: the connection object.
        :param recordingID: recording_id constraint for query.
        :param startTimeContraint: startTime constraint for query.
        :param endTimeContraint: endTime constraint for query.
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM blocks WHERE recording_id=:recordingID", {"recordingID":recordingID} )
        rows = cur.fetchall()
        index = 0
        for row in rows:
            # NOTE: row[3] = starttime and row[4] = stoptime. Both are in ISO 8601 format with Zulu time.
            timevar = {
                "start": None,
                "stop": None,
                "startC": self.format_datetime( self.convert_starttime_datetime( startTimeConstraint ) ),
                "stopC": self.format_datetime( self.convert_stoptime_datetime( endTimeConstraint ) )
            }

            if row[3] != None and row[4] != None:
                timevar["start"] = self.format_datetime( self.convert_starttime_datetime( row[3] ) )
                timevar["stop"] = self.format_datetime( self.convert_stoptime_datetime( row[4] ) )

                if timevar["start"] >= timevar["startC"] and timevar["stop"] <= timevar["stop"]:
                    # self.camDat['path'] += "%s\\%s.mkv" % (row[2], row[1])
                    pathHolder = self.camDat['path'] + "\\%s\\%s.mkv" % (row[2], row[1])


                    # Split the path to filter query results to return only paths with matching 'path' fields from the 'recordings' and 'blocks' tables.
                    splitPathHolder = pathHolder.split("\\")
                    spltToken = lambda st: splitPathHolder[st]
                    # Separate recordings and blocks path into separate tokens.
                    recordingsPathToken = spltToken(4)  # bigNumber_number
                    blocksPathToken = spltToken(2)      # bigNumber/sameNumber

                    if recordingsPathToken.split("_")[1] == blocksPathToken.split("/")[1]:
                        # print( pathHolder )
                        self.add_to_json( self.filenameList['data'], pathHolder, index)
                        index += 1 
            else:
                pass

    # Query all blocks in database. 
    def query_all_blocks(self, conn): # THIS FUNCTION HAS BEEN DEPRICATED.
        """
        Query all rows in the blocks table.

        :param conn: the connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM blocks")

        rows = cur.fetchall()

        # for row in rows:
        #     print(row)
        print("This function has been depricated.")

    ''' =========================== Helper Functions ============================= '''

    # Converting starttime datetime
    def convert_starttime_datetime(self, starttimeDatetime: str):
        """
        Converts starttime from datetime format to string. This is needed for easier comparison
        when querind database for approporiate video files.

        :param starttimeDatetime: The start time in datetime formate represented as a string.
        :return: datetime
        """
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

        return datetimeObj

    # Formatting datetime.
    def format_datetime(self, datetimeString: dtutil.datetime):
        """
        Converts stoptime from datetime format to string. This is needed for easier comparison
        when querind database for approporiate video files.

        :param datetimeString: The datetime string onject to reformat.
        :return: int
        """
        h = datetimeString.time().hour
        m = datetimeString.time().minute
        s = datetimeString.time().second

        time = str("{}{}{}" .format(h, m, s))
        str2int = lambda s: int(s) # converts string to integer

        return str2int(time)

    # Return camera data dictionary
    def getCamDat(self):
        """
        Returns camera data dictionary.

        :return: Dic
        """
        if camDat != None:
            return camDat
        else:
            return None
        return camDat

    # return path to recording file.
    def getPath(self):
        """
        Returns path to desired recording file. Desired file needs to be appended to be able to retrieve.

        :return: str
        """
        if self.camDat['path'] != None:
            return self.camDat['path']
        else:
            return "Error: current Path is Null"
        return self.camDat['path']

    # Append Result into JSON file then write results to file.
    def add_to_json(self, jsonObject, pathAddition, index):
        """
        Adds search results represented in pathAddition, formats proper clipOrder and writes to json file.

        :param jsonObject: The json file for which to write path value and clipOrder to.
        :param pathAddition: The added path to the json file.
        :param index: The clip order.
        """
        jsonObject.append({ "clipOrder":index, "filename_path":pathAddition })

        with open('filenameList.json', 'w') as outfile:
            json.dump(self.filenameList, outfile)
        