import numpy as np
import matplotlib.pyplot as plt
import optuna
import vtk
from vtk.util import numpy_support
import imp, os, tempfile,shutil

import trako as TKO


class Tuner:

  @staticmethod
  def tune(vtpfile, search_space, maxdelta=0.01):
    '''
    '''

    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)

    vtpsize = os.path.getsize(vtpfile)

    tmpdir = tempfile.mkdtemp()
    tkofile = os.path.join(tmpdir, os.path.basename(vtpfile).replace('vtp', 'tko'))
    
    print('VTP size', vtpsize)
    
    tkoed = TKO.Encoder.fromVtp(vtpfile, config=None, verbose=False)
    tkoed.save(tkofile)
    tkosize = os.path.getsize(tkofile)
    
    shutil.rmtree(tmpdir)

    print('TKO default size', tkosize)
    


    study = optuna.create_study(sampler=GridSampler(search_space), pruner=RepeatPruner)
    study.set_user_attr('vtpfile', vtpfile)
    
    
    #
    # optimize for file size with a maxdelta
    #
    study.set_user_attr('maxdelta', 0.005)

    # unique_trials = 20
    # while unique_trials > len(set(str(t.params) for t in study.trials)):
    #   # study.optimize(objective, n_trials=1)
    study.optimize(Tuner.run, n_trials=1000)#, n_jobs=4)


  @staticmethod
  def run(trial):
    '''
    '''


    tkompare = imp.load_source('tkompare', '../tkompare')
    untrakofy = imp.load_source('untrakofy', '../untrakofy')

    vtpfile = trial.study.user_attrs['vtpfile']

    tmpdir = tempfile.mkdtemp()
    tkofile = os.path.join(tmpdir, os.path.basename(vtpfile).replace('vtp', 'tko'))

    position = trial.suggest_categorical('position', [True, False])
    sequential = trial.suggest_categorical('sequential', [True, False])
    quantization_bits = trial.suggest_int('quantization_bits', 0, 31)
    compression_level = trial.suggest_int('compression_level', 0, 10)
#     quantization_bits = trial.suggest_discrete_uniform('quantization_bits', 0, 31, 1)
#     compression_level = trial.suggest_discrete_uniform('compression_level', 0, 10, 1)
#     quantization_range = 
#     quantization_origin = 
    

    # Check duplication and skip if it's detected.
    # for t in trial.study.trials:
    #     if t.state != optuna.structs.TrialState.COMPLETE:
    #         print('skipping')
    #         continue


    #     if t.params == trial.params:
    #         return t.value  # Return the previous value without re-evaluating it.


    config = {
      '*': { 
        'position':position,
        'sequential':sequential,
        'quantization_bits':quantization_bits,
        'compression_level':compression_level,
        'quantization_range':-1,
        'quantization_origin':None
      }

    }
    
#     print(config['position'], config['sequential'], config['quantization_bits'], config['compression_level'])
    
    try:
        tkoed = TKO.Encoder.fromVtp(vtpfile, config=config, verbose=False)
        tkoed.save(tkofile)
    except ValueError as e:
        # print(e)
        raise optuna.exceptions.TrialPruned()

    tkosize = os.path.getsize(tkofile)

    tmpdir = tempfile.mkdtemp()
    restoredfile = os.path.join(tmpdir, 'restored.vtp')

    try:
        
        untrakofy.untrakofy(tkofile, restoredfile, verbose=False)
    except:
        # print(e)
        shutil.rmtree(tmpdir)
        raise optuna.exceptions.TrialPruned()
    

    try:

      poly_a = TKO.Util.loadvtp(vtpfile)
      poly_b = TKO.Util.loadvtp(restoredfile)

      overall_mean_delta = 0

      mean_a = abs(poly_a['number_of_streamlines']-poly_b['number_of_streamlines'])

      overall_mean_delta = max(mean_a, overall_mean_delta)

      (min_a, max_a, mean_a, std_a), dist_a = TKO.Util.error(poly_a['points'], poly_b['points'])


      overall_mean_delta = max(mean_a, overall_mean_delta)

      (min_a, max_a, mean_a, std_a), dist_a = TKO.Util.error(poly_a['lines'], poly_b['lines'])


      overall_mean_delta = max(mean_a, overall_mean_delta)

      for i,s in enumerate(poly_a['scalar_names']):

        if s == "EstimatedUncertainty":
          continue
        (min_a, max_a, mean_a, std_a), dist_a = TKO.Util.error(poly_a['scalars'][i], poly_b['scalars'][i])

        overall_mean_delta = max(mean_a, overall_mean_delta)


      # for i,s in enumerate(poly_a['property_names']):


      #   (min_a, max_a, mean_a, std_a), dist_a = TKO.Util.error(poly_a['properties'][i], poly_b['properties'][i])


        if overall_mean_delta > trial.study.user_attrs['maxdelta']:
          # shutil.rmtree(tmpdir)
          raise optuna.exceptions.TrialPruned()

    except:
      shutil.rmtree(tmpdir)
      raise optuna.exceptions.TrialPruned()

    shutil.rmtree(tmpdir)
    return tkosize
    

import math

from optuna.pruners import BasePruner
from optuna.storages import BaseStorage  # NOQA
from optuna.structs import TrialState

# from https://github.com/Minyus/optkeras/blob/master/optkeras/optkeras.py#L395
class RepeatPruner(BasePruner):
    """ Prune if the same parameter set was found in Optuna database
        Coded based on source code of MedianPruner class at
        https://github.com/pfnet/optuna/blob/master/optuna/pruners/median.py
    """
    def prune(self, storage, study_id, trial_id, step):
        # type: (BaseStorage, int, int, int) -> bool
        """Please consult the documentation for :func:`BasePruner.prune`."""

        n_trials = storage.get_n_trials(study_id, TrialState.COMPLETE)

        if n_trials == 0:
            return False

        trials = storage.get_all_trials(study_id)
        assert storage.get_n_trials(study_id, TrialState.RUNNING)
        assert trials[-1].state == optuna.structs.TrialState.RUNNING
        completed_params_list = \
            [t.params for t in trials \
             if t.state == optuna.structs.TrialState.COMPLETE]
        if trials[-1].params in completed_params_list:
            return True

        return False


import collections
import itertools
import random

from optuna.samplers.base import BaseSampler
from optuna import type_checking

if type_checking.TYPE_CHECKING:
    from typing import Any  # NOQA
    from typing import Dict  # NOQA
    from typing import List  # NOQA
    from typing import Union

    from optuna.distributions import BaseDistribution  # NOQA
    from optuna.structs import FrozenTrial  # NOQA
    from optuna.study import Study  # NOQA

    GridValueType = Union[str, float, int, bool, None]


class GridSampler(BaseSampler):
    """Sampler using grid search.
    With :class:`~optuna.samplers.GridSampler`, the trials suggest all combinations of parameters
    in the given search space during the study.
    This sampler is based on *relative sampling*.
    See also :class:`~optuna.samplers.BaseSampler` for more details of 'relative sampling'.
    Example:
        .. testcode::
            import optuna
            def objective(trial):
                x = trial.suggest_uniform('x', -100, 100)
                y = trial.suggest_int('y', -100, 100)
                return x ** 2 + y ** 2
            search_space = {
                'x': [-50, 0, 50],
                'y': [-99, 0, 99]
            }
            study = optuna.create_study(sampler=optuna.samplers.GridSampler(search_space))
            study.optimize(objective, n_trials=3*3)
    Note:
        :class:`~optuna.samplers.GridSampler` does not take care of a parameter's quantization
        specified by discrete suggest methods but just samples one of values specified in the
        search space. E.g., in the following code snippet, either of ``-0.5`` or ``0.5`` is
        sampled as ``x`` instead of an integer point.
        .. testcode::
            import optuna
            def objective(trial):
                # The following suggest method specifies integer points between -5 and 5.
                x = trial.suggest_discrete_uniform('x', -5, 5, 1)
                return x ** 2
            # Non-int points are specified in the grid.
            search_space = {'x': [-0.5, 0.5]}
            study = optuna.create_study(sampler=optuna.samplers.GridSampler(search_space))
            study.optimize(objective, n_trials=2)
    Args:
        search_space:
            A dictionary whose key and value are a parameter name and the corresponding candidates
            of values, respectively.
    """

    def __init__(self, search_space):
        # type: (Dict[str, List[GridValueType]]) -> None

        for param_name, param_values in search_space.items():
            for value in param_values:
                self._check_value(param_name, value)
            search_space[param_name] = param_values[:]

        self._search_space = collections.OrderedDict(
            sorted(search_space.items(), key=lambda x: x[0]))
        self._all_grids = list(itertools.product(*self._search_space.values()))
        self._param_names = sorted(search_space.keys())
        self._n_min_trials = len(self._all_grids)

    def infer_relative_search_space(self, study, trial):
        # type: (Study, FrozenTrial) -> Dict[str, BaseDistribution]

        return {}

    def sample_relative(self, study, trial, search_space):
        # type: (Study, FrozenTrial, Dict[str, BaseDistribution]) -> Dict[str, Any]

        # Instead of returning param values, GridSampler puts the target grid id as a system attr,
        # and the values are returned from `sample_independent`. This is because the distribution
        # object is hard to get at the beginning of trial, while we need the access to the object
        # to validate the sampled value.

        unvisited_grids = self._get_unvisited_grid_ids(study)

        if len(unvisited_grids) == 0:
            raise ValueError('All grids have been evaluated. If you want to avoid this error, '
                             'please make sure that unnecessary trials do not run during '
                             'optimization by properly setting `n_trials` in `study.optimize`.')

        # In distributed optimization, multiple workers may simultaneously pick up the same grid.
        # To make the conflict less frequent, the grid is chosen randomly.
        grid_id = random.choice(unvisited_grids)

        study._storage.set_trial_system_attr(trial._trial_id, 'search_space', self._search_space)
        study._storage.set_trial_system_attr(trial._trial_id, 'grid_id', grid_id)

        return {}

    def sample_independent(self, study, trial, param_name, param_distribution):
        # type: (Study, FrozenTrial, str, BaseDistribution) -> Any

        if param_name not in self._search_space:
            message = 'The parameter name, {}, is not found in the given grid.'.format(param_name)
            raise ValueError(message)

        grid_id = trial.system_attrs['grid_id']
        param_value = self._all_grids[grid_id][self._param_names.index(param_name)]
        contains = param_distribution._contains(param_distribution.to_internal_repr(param_value))
        if not contains:
            raise ValueError('The value `{}` is out of range of the parameter `{}`. Please make '
                             'sure the search space of the `GridSampler` only contains values '
                             'consistent with the distribution specified in the objective '
                             'function. The distribution is: `{}`.'
                             .format(param_value, param_name, param_distribution))

        return param_value

    @staticmethod
    def _check_value(param_name, param_value):
        # type: (str, Any) -> None

        if param_value is None or isinstance(param_value, (str, int, float, bool)):
            return

        raise ValueError('{} contains a value with the type of {}, which is not supported by '
                         '`GridSampler`. Please make sure a value is `str`, `int`, `float`, `bool`'
                         ' or `None`.'.format(param_name, type(param_value)))

    def _get_unvisited_grid_ids(self, study):
        # type: (Study) -> List[int]

        # List up all finished trials in the same search space.
        trials = study.trials
        trials = [t for t in trials if t.state.is_finished()]
        trials = [t for t in trials if 'grid_id' in t.system_attrs]
        trials = [t for t in trials if self._same_search_space(t.system_attrs['search_space'])]

        # List up unvisited trials based on already finished ones.
        visited_grids = [t.system_attrs['grid_id'] for t in trials]
        unvisited_grids = set(range(self._n_min_trials)) - set(visited_grids)

        return list(unvisited_grids)

    def _same_search_space(self, search_space):
        # type: (Dict[str, List[GridValueType]]) -> bool

        if set(search_space.keys()) != set(self._search_space.keys()):
            return False

        for param_name in search_space.keys():
            if len(search_space[param_name]) != len(self._search_space[param_name]):
                return False

            for i, param_value in enumerate(search_space[param_name]):
                if param_value != self._search_space[param_name][i]:
                    return False

        return True
