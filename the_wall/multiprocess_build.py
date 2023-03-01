from multiprocessing import Lock, Process, Queue
import logging
import queue
import time

from django.conf import settings

from .models import Section, Ledger
from .utils import parse_input_file

logger = logging.getLogger(__name__)


def locked_log(message: str, lock: Lock) -> None:
    lock.acquire()
    try:
        logger.info(message)
    finally:
        lock.release()


def adapt_wall_data(initial_heights_data: list[list[int]]) -> list[tuple[int, int, int]]:
    """
    Changes initial_heights_data data structure to list of tuples
    tuple structure - (initial_section_height, profile_order, section_order)
    these are arguments for BuildingTeam.assign_section method
    """
    result = []
    for profile_index, profile_data in enumerate(initial_heights_data):
        result.extend(
            (height, profile_index + 1, section_index + 1)  # +1 because 1-based index in db
            for section_index, height in enumerate(profile_data)
        )
    # sorted for prioritization - realm needs to build most vulnarable (lowest) sections first
    return sorted(result)


class BuildingTeam:

    def __init__(self, idx: int, name: str = ""):
        self.idx: int = idx
        self.name: str = name or f"Team {idx}"
        self.day: int = 0
        self.section: Section | None = None
        self.current_height: int | None = None

    def assign_section(self, height: int, profile: int, section: int) -> None:
        if height < settings.WALL_HEIGHT:
            self.current_height = height
            self.section = Section.objects.create(profile=profile, order=section)

    def build_section(self) -> None:
        self.day += 1
        self.current_height += 1
        Ledger.objects.create(section=self.section, day=self.day)
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


def build_wall_multiprocess(teams_count: int):
    logger.info("\n==== Another wall building ====")

    lock = Lock()
    processes = []
    unfinished_sections = Queue()
    wall_data = parse_input_file()
    for section_params in adapt_wall_data(wall_data):
        unfinished_sections.put(section_params)

    teams = [BuildingTeam(i) for i in range(teams_count)]
    for team in teams:
        p = Process(target=team_process, args=(team, unfinished_sections, lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
