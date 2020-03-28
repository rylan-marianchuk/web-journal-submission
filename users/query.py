from JournalSubmission.models import Journal, Submission
from users.models import Profile, User

def getProfile(primaryKey):
    """
    Get the profile object from its primary key
    :param primaryKey:
    :return:
    """
    return Profile.objects.get(user = User.objects.get(pk=primaryKey))



def getJournal(editor):
    """
    Must catch the exception of query not found
    Return the journal associated with this editor, if any
    :param editor: model of Profile
    :return:
    """
    return Journal.objects.get(editor=editor)


def getSubmissionsAUTHOR(authorProfile, onlyPending):
    """
    Return a list of all submissions this author has made

    :param authorProfile: the Profile model of the object
    :param onlyPending: bool whether mask the list to only those submissions in review
    :return: list of db objects
    """
    if onlyPending:
        return list(Submission.objects.filter(author = authorProfile, inReview=True))
    return list(Submission.objects.filter(author=authorProfile, inReview=False))



def getSubmissionsJournal(journ):
    """
    Return a list of all submissions this journal has published

    :param authorProfile: the Profile model of the object
    :param onlyPending: bool whether mask the list to only those submissions in review
    :return: list of db objects
    """
    return list()

