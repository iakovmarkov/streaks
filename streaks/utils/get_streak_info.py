from models.Streak import Streak

def get_streak_info(streak: Streak):
    lines = []

    if streak.count_total == 0:
        lines.append(f'You haven\'t tracked "{streak.title}" yet. The first step is the hardest, but it\'s well worth it.')
    elif streak.count_streak == 0:
        lines.append(f'Your current streak at "{streak.title}" is zero.')
        lines.append(f"Your longest streak was {streak.longest}. Get back on track quickly!")
    else:
        lines.append(f'Your streak at "{streak.title}" is {streak.count_streak}, with a total of {streak.count_total}. ')
        if streak.count_streak == streak.longest:
            lines.append("This is your longest streak. Keep it up, champion!")
        else:
            lines.append(f'Your longest streak was {streak.longest}. Work hard and you\'ll beat it!')

    return lines