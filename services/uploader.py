import os


class Uploader:

    @staticmethod
    def user_image(instance, filename):
        return f"User_Image/{instance.first_name}-{instance.last_name}/{filename}"

    @staticmethod
    def task_image(instance, filename):
        return f"Task_Image/{instance.author.first_name}-{instance.author.last_name}/{instance.title}/{filename}"
