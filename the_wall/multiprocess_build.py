from multiprocessing import Lock, Process, Queue
import logging
import queue
import time

from .entities import UnfinishedSection, BuildingTeam
from .use_cases import build_section

logger = logging.getLogger(__name__)


def locked_log(message: str, lock: Lock) -> None:
    lock.acquire()
    try:
        logger.info(message)
    finally:
        lock.release()


def build_process(team: BuildingTeam, unfinished_sections: Queue, lock: Lock) -> bool:
    while True:
        try:
            section = unfinished_sections.get_nowait()
        except queue.Empty:
            locked_log(f"Day {team.day}: No more work for {team.name}", lock)
            break
        else:
            days_took = build_section(section, team)
            time.sleep(.2 * days_took)
            locked_log(_section_finished_message(section, team), lock)
    return True


def build_wall_multiprocess(sections: list[UnfinishedSection], teams_count: int) -> None:
    logger.info(f"\n==== Building wall with {teams_count} teams ====")

    lock = Lock()
    processes = []
    sections_queue = Queue()
    for section in sorted(sections, key=lambda s: s.height):
        sections_queue.put(section)

    teams = [BuildingTeam(f"Team {i}") for i in range(teams_count)]
    for team in teams:
        p = Process(target=build_process, args=(team, sections_queue, lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def _section_finished_message(section: UnfinishedSection, team: BuildingTeam) -> str:
    return f"Day {team.day - 1}: {team.name} finished Profile {section.profile} Section {section.order}"
