import os


class Uploader:

    @staticmethod
    def user_image(instance, filename):
        return f"User_Image/{instance.first_name}-{instance.last_name}/{filename}"
