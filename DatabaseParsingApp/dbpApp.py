import main_dbp
import sqlite3
from sqlite3 import Error
import json

camera = "axis-ACCC8E5B4C2D"                    # This camera should be on a Prime
START_TIME = "2019-09-15T15:38:52.121925Z"      # Starttime taken from database
STOP_TIME = "2019-09-15T15:38:52.121925Z"      # Starttime taken from database

# STOP_TIME = "2019-09-15T23:03:37.652860Z"       # Endtime taken from the database

returnPath = None

def main():
    "Main method for main_dbp class"
    # databasePath = "W:\%s\index.db" % camera  # Path to desired database.
    databasePath = r"../../index.db"
    mdbp = main_dbp.main_dbp_class(camera, START_TIME, STOP_TIME)

    # 1.) Create a new database connection.
    database_connection = mdbp.create_connection(databasePath)    # returns a database connection object

    # 2.) Find the recording_action_id from a subscribed event trigger in the recording_events table
    recording_action_id = mdbp.find_recording_action_id(database_connection,"ACC_ContinuousAction")
    print("recording_action_id = {}" .format(recording_action_id))    # print for testing values

    # 3.) Find the recording_event_id from a subscribed action trigger in the recording_actions table
    recording_event_id = mdbp.find_recording_event_id(database_connection,"ACC_Continuous")
    print("recording_event_id = {}" .format(recording_event_id))    # print for testing values

    # 4.) Use the recording_action_id and the recording_event_id from step 2 and step 3 to find recording_id
    recording_id = mdbp.find_recording_id(database_connection,recording_event_id, recording_action_id)
    print("recording_id = {}" .format(recording_id))    # print for testing values
    
    # 5.) Use the recording_id found in step 4 to cross reference desired filepath filename pairs in blocks table within the start and stop time constraints.
    # mdbp.query_recording_id_blocks(database_connection, recording_id)
    mdbp.query_recording_id_time_blocks(database_connection, recording_id, START_TIME, STOP_TIME)
    # mdbp.query_recording_id_starttime_blocks(database_connection, recording_id, START_TIME)
    # mdbp.query_recording_id_endtime_blocks(database_connection, recording_id, STOP_TIME)

    # 6.) Take recordings found and add them to a Dictionary object
    # print(mdbp.filenameList)
    with open('filenameList.json') as json_file:
        data = json.load(json_file)
    print(json.dumps(data, indent=4))

    # 7.) Take dictionary object and turn it into .json file format. Check to make sure this is in the correcet format for part 8.) below

    # 8.) Return json file 'filenameList' in the format specified by datbaseparser_db.py.


    # print("\nRecording Path : %s + 'Name of file'.mkv" % mdbp.getPath())

    print("\n")
    print("Selected Camera: %s" % mdbp.camDat["cameraName"])
    print("Start Time: %s" % mdbp.camDat["startTime"])
    print("End Time: %s" % mdbp.camDat["endTime"])

if __name__ == "__main__":
    main()