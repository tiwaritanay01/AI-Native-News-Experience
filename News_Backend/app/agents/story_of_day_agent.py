from app.services.story_detector import detect_story_of_the_day


def get_story_of_the_day():

    story = detect_story_of_the_day()

    return story