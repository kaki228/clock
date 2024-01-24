import time
from telethon import TelegramClient
from telethon.tl.types import InputFile
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from config import api_hash, api_id
from utils import time_has_changed, generate_time_image_bytes
from datetime import datetime, timedelta
import argparse
import pytz


def valid_tz(s):
    try:
        return pytz.timezone(s)
    except:
        msg = "Not a valid tz: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

api_id="20598182"
api_hash="17d98e76bfc32767151a1217a9d5370b"
parser = argparse.ArgumentParser()
parser.add_argument("--api_id", required=False, help="user api ID", type=str, default=api_id)
parser.add_argument("--api_hash", required=False, help="user api Hash", type=str, default=api_hash)
parser.add_argument("--tz", required=False,  help="user api Hash", type=valid_tz, default=valid_tz('Europe/Moscow'))

args = parser.parse_args()

client = TelegramClient("carpediem", args.api_id, args.api_hash)
client.start()


async def main():
    prev_update_time = datetime.now() - timedelta(minutes=1)

    while True:
        if time_has_changed(prev_update_time):
            bts = generate_time_image_bytes(datetime.now(args.tz).replace(tzinfo=None))
            await client(DeletePhotosRequest(await client.get_profile_photos('me')))
            #file = await client.upload_file(bts)
            #await client(UploadProfilePhotoRequest(file=bts))
            #result = await client(UploadProfilePhoto(file=bts))
            result = await client.upload_file(
            file=bts,
            part_size_kb=512,  # Adjust this value according to your needs
            file_name='profile_photo.jpg',
            )

            await client(UploadProfilePhotoRequest(file=result))
            prev_update_time = datetime.now()
            time.sleep(1)
            

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
