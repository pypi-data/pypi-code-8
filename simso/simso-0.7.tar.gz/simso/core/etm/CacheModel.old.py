# coding=utf-8

from simso.core.etm.AbstractExecutionTimeModel \
    import AbstractExecutionTimeModel
from simso.core.cachemodels import History, cpi_alone
from simso.core.cachemodels.calc_e import calc_e_task
from math import ceil, exp


def calc_cache_sizes(caches, task, running_jobs):
    """Calculates the size of the cache taking into account the other running
    tasks."""
    # FOA model.
    result = []
    for cache in caches:
        shared_jobs = [t for t in running_jobs
                       if (t[0].cpu in cache.shared_with)]
        proportion = ((float(task.mix) / task.get_cpi_alone()) /
                      sum([t[0].task.mix / t[0].task.get_cpi_alone()
                           for t in shared_jobs]))

#        proportion = (float(task.mix)) / sum([t[0].mix for t in shared_tasks])
        result.append(cache.size * proportion)
    return result


def calc_lines_lru(task, sizes, lines, mem_access):
    return [min(float(task.footprint - l) *
            (1 - exp(-float(mem_access) / task.footprint)) + l, size)
            for size, l in zip(sizes, lines)]


class CacheModel(AbstractExecutionTimeModel):
    def __init__(self, sim, nb_processors):
        self.sim = sim
        self._hist = History(nb_processors)

    def init(self):
        for task in self.sim.task_list:
            for proc in self.sim.processors:
                caches = proc.caches
                task.set_cpi_alone(
                    proc,
                    cpi_alone(task, [c.size for c in caches],
                              [proc.penalty_memaccess] +
                              [c.penalty for c in caches])
                )

    def update(self):
        self._update_instructions()

    def _update_instructions(self):
        running_jobs = [x for x in self._hist.get() if x]

        for job, deb, lines in running_jobs:
            if self.sim.now() == deb:
                continue

            caches = job.cpu.caches
            cache_sizes = calc_cache_sizes(caches, job.task, running_jobs)

            instr_count = calc_e_task(
                job.task,
                cache_sizes,
                [job.cpu.penalty_memaccess] +
                [c.penalty for c in caches], self.sim.now() - deb, lines)

            lines = calc_lines_lru(job.task, cache_sizes, lines,
                                   instr_count * job.task.mix)

            for cache, l in zip(caches, lines):
                cache.update(job.task, l)

            job.instr_count += int(ceil(instr_count))
            # instr_count n'a rien à faire ici je pense.

            self._hist.update(self.sim.now(), job, lines)

    def on_activate(self, job):
        pass

    def on_execute(self, job):
        # Update the number of instructions executed for the running jobs.
        self._update_instructions()

        # Nombre de lignes appartenant à cette tâche initialement.
        lines = [c.get_lines(job.task) for c in job.cpu.caches]

        # Ajoute à l'historique la tâche avec son processeur et le nombre de
        # lignes initiales.
        self._hist.update(self.sim.now(), job, lines)

    def on_preempted(self, job):
        self._update_instructions()
        self._hist.stop(self.sim.now(), job.cpu)

    def on_terminated(self, job):
        self._update_instructions()
        self._hist.stop(self.sim.now(), job.cpu)

    def on_abort(self, job):
        self._update_instructions()
        self._hist.stop(self.sim.now(), job.cpu)

    def get_ret(self, job):
        hist = self._hist.get()

        hjob, deb, lines = hist[job.cpu.internal_id]

        running_jobs = [x for x in hist if x]

        caches = job.cpu.caches
        cache_sizes = calc_cache_sizes(caches, hjob.task,
                                       running_jobs)
        instr = calc_e_task(
            job.task,
            cache_sizes,
            [hjob.task.cpu.penalty_memaccess] +
            [c.penalty for c in caches],
            self.sim.now() - deb, lines)

        # XXX Multiplier par base_cpi ?
        return job.task.n_instr - job.instr_count - instr
