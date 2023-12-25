import os
import pika, json


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)  # try to put the file in mongodb
    except Exception as err:
        return f"ERROR : {err}"

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",  # name of the queue
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as e:
        fs.delete(fid)
        return f"Internal Server Error {e}", 500
