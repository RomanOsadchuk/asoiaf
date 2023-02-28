from multiprocessing import Lock, Process, Queue
import os
import queue
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from the_wall.models import Section


def locked_log(message: str, lock: Lock) -> None:
    lock.acquire()
    try:
        print(message)
    finally:
        lock.release()


def parse_wall() -> list[tuple]:
    result = []
    file_path = os.path.join(settings.BASE_DIR, settings.CONFIG_FILE)
    with open(file_path, "r") as conf_file:
        profile = 1
        for line in conf_file.readlines():
            for section_order, height in enumerate(line.split(" ")):
                height = int(height)
                result.append((height, profile, section_order + 1))
            profile += 1
    return sorted(result)


class BuildingTeam:

    def __init__(self, idx: int, name: str = ""):
        self.idx: int = idx
        self.name: str = name or f"Team {idx}"
        self.day: int = 0
        self.section: Section | None = None
        self.current_height: int | None = None

    def assign_section(self, height: int, profile: int, section: int) -> None:
        self.current_height = height
        self.section = Section(profile=profile, order=section, building_days_str="")

    def build_section(self) -> None:
        self.day += 1
        start = "," if self.section.building_days_str else ""
        self.section.building_days_str += f"{start}{self.day}"
        self.current_height += 1
        time.sleep(.5)

    def section_finished_message(self) -> str:
        return f"Day {self.day}: {self.name} finished Profile " \
               f"{self.section.profile} Section {self.section.order}"

    def job_done_message(self) -> str:
        return f"Day {self.day} was last worfing day for {self.name}"


def team_process(team: BuildingTeam, unfinished_sections: Queue, lock: Lock):
    while True:
        if team.section:
            team.build_section()
            if team.current_height >= settings.WALL_HEIGHT:
                locked_log(team.section_finished_message(), lock)
                team.section.save()
                team.section = None
            continue

        try:
            section_params = unfinished_sections.get_nowait()
        except queue.Empty:
            locked_log(team.job_done_message(), lock)
            break
        else:
            team.assign_section(*section_params)
    return True


class Command(BaseCommand):
    help = "Build the wall from config file"

    def add_arguments(self, parser):
        parser.add_argument("teams_count", type=int)

    def handle(self, *args, **options):
        Section.objects.all().delete()

        lock = Lock()
        processes = []
        unfinished_sections = Queue()
        for section_params in parse_wall():
            unfinished_sections.put(section_params)

        teams = [BuildingTeam(i) for i in range(options["teams_count"])]
        for team in teams:
            p = Process(target=team_process, args=(team, unfinished_sections, lock))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()
        self.stdout.write("The wall has been built", ending='\n')
