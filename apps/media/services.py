from .models import Media


def create_media(*, record, uploaded_file, media_type):
	return Media.objects.create(record=record, file=uploaded_file, media_type=media_type)


def delete_media(media):
	media.file.delete(save=False)
	media.delete()
