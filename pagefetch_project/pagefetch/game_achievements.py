__author__ = 'leif'


from game_models import PlayerAchievement, Achievement
import logging


class GameAchievement(object):

    def __init__(self, userprofile, highscores, currentgame=None):
        """
        :param userprofile: ifind.models.game_models.UserProfile
        :param highscores: list of highscores for this user
        :return:
        """
        self.userprofile = userprofile
        self.highscores = highscores
        self.currentgame = currentgame
        self.logger = logging.getLogger(__name__)

    def check_achievement_criteria(self):
        pass


class AllCat(GameAchievement):

    def __init__(self, userprofile, highscores, currentgame=None, num_of_cats = 8):
        GameAchievement.__init__(self,userprofile, highscores)
        #self.logger.info("AllCats Achievement set to %d cats", num_of_cats)
        self.num_of_cats = num_of_cats

    def check_achievement_criteria(self):
        """
        the number of highscores is a list of the highest_score in each category
        a highest_score is only recorded once they have played a game.
        but we could also check to make sure they have score points in each category, too
        :return:
        """
        #self.logger.info("AllCats Achievement check being performed")
        if len(self.highscores) == self.num_of_cats:
            return True
        else:
            return False

    def __str__(self):
        #TODO(leifos): there probably a neat way to return the class name
        return self.__class__.__name__


class HighScorer(GameAchievement):

    def __init__(self, userprofile, highscores, currentgame=None, score_required=10000):
        GameAchievement.__init__(self,userprofile, highscores)
        self.score_required = score_required

    def check_achievement_criteria(self):
        total = 0
        for hs in self.highscores:
            total += hs.highest_score
        if total > self.score_required:
            return True
        else:
            return False

    def __str__(self):
        #TODO(leifos): there probably a neat way to return the class name
        return self.__class__.__name__


class UberSearcher(GameAchievement):

    def __init__(self, userprofile, highscores, currentgame=None, score_required=3000):
        GameAchievement.__init__(self,userprofile, highscores)
        self.score_required = score_required

    def check_achievement_criteria(self):
        for hs in self.highscores:
            if hs.highest_score >= self.score_required:
                return True


class TenGamesPlayed(GameAchievement):

    def __init__(self, userprofile, highscores, currentgame=None, score_required=10):
        GameAchievement.__init__(self,userprofile, highscores)
        self.score_required = score_required

    def check_achievement_criteria(self):
        if self.userprofile.no_games_played >= self.score_required:
            return True
        return False


class FivePagesInAGame(GameAchievement):

    def __init__(self, userprofile, highscores, currentgame=None, score_required=5):
        GameAchievement.__init__(self,userprofile, highscores)
        self.score_required = score_required

    def check_achievement_criteria(self):
        for hs in self.highscores:
            if hs.most_no_pages_found >= self.score_required:
                return True
        return False


class GameAchievementChecker(object):
    def __init__(self, user):
        """
        :param user:
        :return:
        """
        self.user=user

    def check_and_set_new_achievements(self, userprofile, highscores, currentgame):
        """ test whether the crtieria are met for achievements that have not yet been awarded
        :param userprofile:
        :param highscores:
        :param currentgame:
        :return:
        """
        # get list of the users current player achievements
        cpal = PlayerAchievement.objects.filter(user=self.user)

        # pull out the list of achievements they have obtained.
        pal = []
        for cpa in cpal:
            pal.append(cpa.achievement)

        # get list of possible achievements
        aal = Achievement.objects.all()

        # exclude achievements already obtained
        al = []
        for a in aal:
            if a not in pal:
                al.append(a)

        # create an empty list of new achievements
        nal = []

        # for each achievement, check whether the criteria is met
        for a in al:
            outcome = self._test_achievement(a, userprofile, highscores, currentgame)
            if outcome:
                # if met, create the PlayerAchievement Record
                pa = PlayerAchievement(user=self.user, achievement=a)
                pa.save()
                # add this PlayerAchievement to a list
                nal.append(pa)

        # return list of new achievements
        return nal


    def _test_achievement(self, achievement, userprofile, highscores, currentgame):
        """ For the given achievement (ifind.models.game_models.Achievement),
        instantiate the related class and then check the criteria

        :return: true, if the achievement criteria are met, else false

        """

        #TODO(leifos): use reflection ? or some kind of class inspection to determine if the class has been implemented and then use that class
        # need some reflection in here to inspect whether the achievement class specified exists or not
        outcome = False
        ga =  None

        classes = {'HighScorer': HighScorer, 'AllCat': AllCat,
                   'UberSearcher': UberSearcher,
                   'TenGamesPlayed': TenGamesPlayed,
                   'FivePagesInAGame': FivePagesInAGame}
        if achievement.achievement_class in classes:
            gac = classes[achievement.achievement_class]
            ga = gac(userprofile, highscores, currentgame)
        if ga:
            outcome = ga.check_achievement_criteria()

        return outcome
