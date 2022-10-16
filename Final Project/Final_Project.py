# CS-3860 Final Project
# Authors: Nigel Nelson and Mitchell Johnstone
# Date: 11/09/21


from pymongo import MongoClient
from pprint import pprint

# Method responsible for adding the array of actor names to the
# video_recording collection
def add_actor_array(client):
    actors = client.Final_Project.video_actors.find()
    actor_dict = dict()
    for actor in actors:
        if actor['recording_id'] in actor_dict:
            actor_dict[actor['recording_id']].append(actor['name'])
        else:
            actor_dict[actor['recording_id']] = [actor['name']]

    recordings = client.Final_Project.video_recordings.find()
    for recording in recordings:
        client.Final_Project.video_recordings.update_one(
            recording,
            {"$set": {"actors": actor_dict[recording['recording_id']]}})


# Method responsible for adding the array of recording_ids and
# the array of categories to the video_actors collection
def add_category_array(client):
    recording_category = dict()
    recordings = client.Final_Project.video_recordings.find()
    for recording in recordings:
        recording_category[recording["recording_id"]] = recording["category"]

    actor_names = dict()
    actors = client.Final_Project.video_actors.find()
    for actor in actors:
        if actor['name'] in actor_names:
            actor_names[actor['name']].append(actor['recording_id'])
        else:
            actor_names[actor['name']] = [actor['recording_id']]

    name_category = dict()
    for name, rec_list in actor_names.items():
        categories = []
        for recording in rec_list:
            if recording_category[recording] not in categories:
                categories.append(recording_category[recording])
        name_category[name] = categories

    actors = client.Final_Project.video_actors.find()
    for actor in actors:
        client.Final_Project.video_actors.update_one(
            actor,
            {"$set": {"categories": name_category[actor['name']]}})
        client.Final_Project.video_actors.update_one(
            actor,
            {"$set": {"recording_ids": actor_names[actor['name']]}})


# Method responsible for removing the recording_id field, as well as dropping
# duplicate actors from the video_actor collection
def drop_recordingID_duplicates(client):
    actor_names = set()
    client.Final_Project.video_actors.update_many({}, {"$unset": {"recording_id": ""}})
    actors = client.Final_Project.video_actors.find()
    for actor in actors:
        if actor['name'] in actor_names:
            client.Final_Project.video_actors.delete_one(actor)
        else:
            actor_names.add(actor['name'])


def P3(client):
  print("3) List the number of videos for each video category.")
  results = client.Final_Project.video_recordings.aggregate(
    [
      {
        "$group": {
          "_id": "$category",
          "count": {"$sum": 1}
        }
      } 
    ]
  )
  pprint(list(results))


def P4(client):
  print("\n4) List the number of videos for each video category where the inventory is non-zero.")
  results = client.Final_Project.video_recordings.aggregate(
    [
      {
        "$match" : {
          "stock_count": {
            "$ne" : 0
          }
        }
      },
      {
        "$group": {
          "_id": "$category",
          "count": {"$sum": 1}
        }
      } 
    ]
  )
  pprint(list(results))


def P5(client):
  print("\n5) For each actor, list the video categories.")
  results = client.Final_Project.video_actors.find(
    {},
    {
      "name" : 1,
      "categories" : 1,
      "_id": 0
    }
  )
  pprint(list(results)[:10])
  print("Total Rows:",results.count())


def P6(client):
  print("\n6) Which actors have appeared in movies in different video categories?")
  results = client.Final_Project.video_actors.find(
    {
      "categories.1": {"$exists": True}
    },
    {
      "name" : 1,
      "categories" : 1,
      "_id": 0
    }
  )
  pprint(list(results)[:10])
  print("Total Rows:",results.count())


def P7(client):
  print("\n7) Which actors have not appeared in a comedy?")
  results = client.Final_Project.video_actors.find(
    {
      "categories": {"$nin": ["Comedy"]}
    },
    {
      "name" : 1,
      "categories" : 1,
      "_id": 0
    }
  )
  pprint(list(results)[:10])
  print("Total Rows:",results.count())


def P8(client):
  print("\n8) Which actors have appeared in comedy and action adventure movies?")
  results = client.Final_Project.video_actors.find(
    {
      "categories": {"$all": ["Comedy", "Action & Adventure"]}
    },
    {
      "name" : 1,
      "categories" : 1,
      "_id": 0
    }
  )
  pprint(list(results)[:10])
  print("Total Rows:",results.count())


def main():
    client = MongoClient("mongodb+srv://Mitchell:1234@cluster0.9d2q0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    P3(client)
    P4(client)
    P5(client)
    P6(client)
    P7(client)
    P8(client)


if __name__ == "__main__":
  main()