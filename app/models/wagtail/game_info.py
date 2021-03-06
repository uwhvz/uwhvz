from django.db import models
from enumfields import Enum
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from app.models import Game
from app.util import most_recent_game


class ViewableBy(Enum):
    ALL = 'A'
    HUMANS = 'H'
    ZOMBIES = 'Z'


class GameInfoPage(Page):
    template = "wagtail/game_info.html"

    subpage_types = ['app.AnnouncementPage', 'app.MissionPage']
    parent_page_types = ['app.DashboardPage']

    def get_context(self, request, *args, **kwargs):
        context = super(GameInfoPage, self).get_context(request)
        game = most_recent_game()
        participant = request.user.participant(game)
        context['is_mobile'] = request.user_agent.is_mobile
        context['participant'] = participant
        context['game'] = game

        announcements = self.get_children().type(AnnouncementPage).live().order_by('-first_published_at')
        viewable_announcements = [a for a in announcements if a.specific.is_viewable_by(participant)]
        context['announcements'] = viewable_announcements

        missions = self.get_children().type(MissionPage).live().order_by('-first_published_at')
        viewable_missions = [m for m in missions if m.specific.is_viewable_by(participant)]
        context['missions'] = viewable_missions
        return context


class AnnouncementPage(Page):
    template = "wagtail/announcement.html"

    body: str = RichTextField(blank=True)
    viewable_by: Enum = models.CharField(choices=[(tag.value, tag.label) for tag in ViewableBy], max_length=1)
    game: Game = models.ForeignKey(Game, on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        FieldPanel('viewable_by'),
        FieldPanel('game'),
        FieldPanel('body', classname="full"),
    ]

    parent_page_types = ['app.GameInfoPage']
    subpage_types = []

    def get_admin_display_title(self) -> str:
        return f'<{self.get_viewable_by_display()}> {self.draft_title or self.title}'

    def get_context(self, request, *args, **kwargs):
        context = super(AnnouncementPage, self).get_context(request)
        game = most_recent_game()
        participant = request.user.participant(game)
        context['participant'] = participant
        context['game'] = game
        return context

    def is_viewable_by(self, participant) -> bool:
        game = most_recent_game()
        if self.game != game or not participant:
            return False

        if self.viewable_by == ViewableBy.ALL.value:
            return True
        if self.viewable_by == ViewableBy.HUMANS.value and participant.is_player and participant.is_human:
            return True
        if self.viewable_by == ViewableBy.ZOMBIES.value and participant.is_player and participant.is_zombie:
            return True
        if participant.is_spectator or participant.is_moderator or participant.user.is_staff:
            return True
        return False


class MissionPage(Page):
    template = "wagtail/mission.html"

    body: str = RichTextField(blank=True)
    viewable_by = models.CharField(choices=[(tag.value, tag.label) for tag in ViewableBy], max_length=1)
    game: Game = models.ForeignKey(Game, on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        FieldPanel('viewable_by'),
        FieldPanel('game'),
        FieldPanel('body', classname="full")
    ]

    parent_page_types = ['app.GameInfoPage']
    subpage_types = []

    def get_admin_display_title(self) -> str:
        return f'<{self.get_viewable_by_display()}> {self.draft_title or self.title}'

    def get_context(self, request, *args, **kwargs):
        context = super(MissionPage, self).get_context(request)
        game = most_recent_game()
        participant = request.user.participant(game)
        context['participant'] = participant
        context['game'] = game
        return context

    def is_viewable_by(self, participant) -> bool:
        game = most_recent_game()
        if self.game != game or not participant:
            return False

        if self.viewable_by == ViewableBy.ALL.value:
            return True
        if self.viewable_by == ViewableBy.HUMANS.value and participant.is_player and participant.is_human:
            return True
        if self.viewable_by == ViewableBy.ZOMBIES.value and participant.is_player and participant.is_zombie:
            return True
        if participant.is_spectator or participant.is_moderator or participant.user.is_staff:
            return True
        return False
