import lm_eval.tasks as tasks
import lm_eval.base as base
from itertools import islice
import pytest


@pytest.mark.parametrize("taskname,Task", tasks.TASK_REGISTRY.items())
def test_basic_interface(taskname, Task):
    print('Evaluating task', taskname)
    #dl = Task.download
    #Task.download = MagicMock()
    task = Task()
    #Task.download = dl

    assert task.has_training_docs() in [True, False]
    assert task.has_validation_docs() in [True, False]
    assert task.has_test_docs() in [True, False]

    assert isinstance(task.aggregation(), dict)
    assert isinstance(task.higher_is_better(), dict)
    assert task.aggregation().keys() == task.higher_is_better().keys()

    for v in task.higher_is_better().values(): assert v in [True, False]


@pytest.mark.parametrize("taskname,Task", tasks.TASK_REGISTRY.items())
def test_documents_and_requests(taskname, Task):
    print('Evaluating task', taskname)
    task = Task()
    fns = []
    if task.has_training_docs(): fns.append(task.training_docs)
    if task.has_validation_docs(): fns.append(task.validation_docs)
    # test doce might not have labels
    #if task.has_test_docs(): fns.append(task.test_docs)

    for fn in fns:
        #print(list(islice(fn(), 10)))
        for doc in islice(fn(), 10):
            
            txt = task.doc_to_text(doc)
            tgt = task.doc_to_target(doc)

            assert isinstance(txt, str)
            assert isinstance(tgt, str)
            
            # space convention
            assert txt[-1] != ' '
            assert tgt[0] == ' ' or txt[-1] == '\n'

            reqs = task.construct_requests(doc, txt)

            # todo: mock lm after refactoring evaluator.py to not be a mess
            for req in reqs:
                assert isinstance(req, base.Request)
