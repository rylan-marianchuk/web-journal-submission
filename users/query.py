from JournalSubmission.models import Journal, Submission
from users.models import Profile, User


def getProfile(primaryKey):
    """
    Get the profile object from its primary key
    :param primaryKey:
    :return: the profile database (db) object that has the given primary key by making a query
             first to users and then the profile table.
    """
    return Profile.objects.get(user=User.objects.get(pk=primaryKey))


def getProfile_id(id):
    """
    Get the profile object from its id number
    :param id: INTEGER the id number requested
    :return: the profile with given id number
    """
    return Profile.objects.get(id=id)


def getJournal(editor):
    """
    Must catch the exception of query not found
    Return the journal associated with this editor, if any
    :param editor: model of Profile
    :return:
    """
    return Journal.objects.filter(editor=editor)


def getSubmissionsAUTHOR(authorProfile, onlyPending):
    """
    Return a list of all submissions this author has made

    :param authorProfile: the Profile model of the object
    :param onlyPending: bool whether mask the list to only those submissions in review
    :return: list of db objects
    """
    if onlyPending:
        return list(Submission.objects.filter(author=authorProfile, inReview=True))
    return list(Submission.objects.filter(author=authorProfile, editorApproved = True, inReview=False))


def getSubmissionsJournal(journal_db, editorApproved):
    """
    Return a list of all submissions this journal has published

    :param journal_db: the journal db object
    :param editorApproved: bool whether mask the list to only those submissions in review by editor
    :return: list of db submission objects that have been made to this journal
    """
    return list(Submission.objects.filter(journal_id=journal_db, editorApproved=editorApproved))


def getSubmissionsEditor(journal_db, editorApproved):
    """
    Return the query for submissions of a given editor
    :param journal_db: the journal database object
    :param editorApproved: whether or not the submissions should be editor approved
    :return: None if query was blank, otherwise a single object in the query
    """
    query = list(Submission.objects.filter(journal_id=journal_db, editorApproved=editorApproved))

    if not query:
        return None
    return query[0]


def getSubmissionsToReview(reviewer_id):
    """
    Return the query for submissions of a given editor
    :param journal_db: the journal database object
    :return: None if query was blank, otherwise return a submission object and the number of reviewer
             of the submission found with this given reviewer chosen.
    """

    zip_ = zip(Submission.objects.filter(editorApproved=True).values(), Submission.objects.filter(editorApproved=True))
    for subm_dict, obj in zip_:
        # Each submission will be a dictionary
        for i in range(1, 4):
            if subm_dict['reviewer' + str(i) + '_id'] == reviewer_id and subm_dict['inReview'] and \
                    not obj.didSee(i):
                # Then this submission should be given to the reviewer
                # Only return one at a time
                return obj, i
    return None, 0
