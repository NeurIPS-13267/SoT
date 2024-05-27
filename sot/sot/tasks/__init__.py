def get_task(name):
    if name == 'trivia_creative_writing':
        from sot.tasks.trivia_creative_writing import TriviaCreativeWritingTask
        return TriviaCreativeWritingTask()
    else:
        raise NotImplementedError
