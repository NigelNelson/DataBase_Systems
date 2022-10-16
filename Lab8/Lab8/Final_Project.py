from pymongo import MongoClient


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

    # client.Final_Project.video_recordings.update_many({ }, {"$unset": {"actors": ""}})


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
            # client.Final_Project.video_actors.delete_one(actor)
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

def drop_recordingID_duplicates(client):
    actor_names = set()
    client.Final_Project.video_actors.update_many({}, {"$unset": {"recording_id": ""}})
    actors = client.Final_Project.video_actors.find()
    for actor in actors:
        if actor['name'] in actor_names:
            client.Final_Project.video_actors.delete_one(actor)
        else:
            actor_names.add(actor['name'])




def main():
    client = MongoClient(
        "mongodb+srv://Nigel:1234@cluster0.9d2q0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    #add_category_array(client)
    drop_recordingID_duplicates(client)

if __name__ == "__main__":
  main()