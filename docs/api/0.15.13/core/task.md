---
sidebarDepth: 2
editLink: false
---
# Task
---
 ## Task
 <div class='class-sig' id='prefect-core-task-task'><p class="prefect-sig">class </p><p class="prefect-class">prefectlegacy.core.task.Task</p>(name=None, slug=None, tags=None, max_retries=None, retry_delay=None, timeout=None, trigger=None, skip_on_upstream_skip=True, cache_for=None, cache_validator=None, cache_key=None, checkpoint=None, state_handlers=None, on_failure=None, log_stdout=False, result=None, target=None, task_run_name=None, nout=None)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L199">[source]</a></span></div>

The Task class which is used as the full representation of a unit of work.

This Task class can be used directly as a first class object where it must be inherited from by a class that implements the `run` method.  For a more functional way of generating Tasks, see [the task decorator](../utilities/tasks.html).

Inheritance example: 
```python
class AddTask(Task):
    def run(self, x, y):
        return x + y

```

*Note:* The implemented `run` method cannot have `*args` in its signature. In addition, the following keywords are reserved: `upstream_tasks`, `task_args` and `mapped`.

An instance of a `Task` can be used functionally to generate other task instances with the same attributes but with different values bound to their `run` methods.

**Example**: 
```python
class AddTask(Task):
    def run(self, x, y):
        return x + y

a = AddTask()

with Flow("My Flow") as f:
    t1 = a(1, 2) # t1 != a
    t2 = a(5, 7) # t2 != a

```

To bind values to a Task's run method imperatively (and without making a copy), see `Task.bind`.

**Args**:     <ul class="args"><li class="args">`name (str, optional)`: The name of this task     </li><li class="args">`slug (str, optional)`: The slug for this task. Slugs provide a stable ID for tasks so         that the Prefect API can identify task run states. If a slug is not provided, one         will be generated automatically once the task is added to a Flow.     </li><li class="args">`tags ([str], optional)`: A list of tags for this task     </li><li class="args">`max_retries (int, optional)`: The maximum amount of times this task can be retried     </li><li class="args">`retry_delay (timedelta, optional)`: The amount of time to wait until task is retried     </li><li class="args">`timeout (Union[int, timedelta], optional)`: The amount of time (in seconds) to wait while         running this task before a timeout occurs; note that sub-second         resolution is not supported, even when passing in a timedelta.     </li><li class="args">`trigger (callable, optional)`: a function that determines whether the         task should run, based on the states of any upstream tasks.     </li><li class="args">`skip_on_upstream_skip (bool, optional)`: if `True`, if any immediately         upstream tasks are skipped, this task will automatically be skipped as         well, regardless of trigger. By default, this prevents tasks from         attempting to use either state or data from tasks that didn't run. If         `False`, the task's trigger will be called as normal, with skips         considered successes. Defaults to `True`.     </li><li class="args">`cache_for (timedelta, optional)`: The amount of time to maintain a cache         of the outputs of this task.  Useful for situations where the containing Flow         will be rerun multiple times, but this task doesn't need to be.     </li><li class="args">`cache_validator (Callable, optional)`: Validator that will determine         whether the cache for this task is still valid (only required if `cache_for`         is provided; defaults to `prefectlegacy.engine.cache_validators.duration_only`)     </li><li class="args">`cache_key (str, optional)`: if provided, a `cache_key`         serves as a unique identifier for this Task's cache, and can be shared         across both Tasks _and_ Flows; if not provided, the Task's _name_ will         be used if running locally, or the Task's database ID if running in         Cloud     </li><li class="args">`checkpoint (bool, optional)`: if this Task is successful, whether to         store its result using the configured result available during the run;         Also note that checkpointing will only occur locally if         `prefectlegacy.config.flows.checkpointing` is set to `True`     </li><li class="args">`result (Result, optional)`: the result instance used to retrieve and         store task results during execution     </li><li class="args">`target (Union[str, Callable], optional)`: location to check for task Result. If a result         exists at that location then the task run will enter a cached state.         `target` strings can be templated formatting strings which will be         formatted at runtime with values from `prefectlegacy.context`. If a callable function         is provided, it should have signature `callable(**kwargs) -> str` and at write         time all formatting kwargs will be passed and a fully formatted location is         expected as the return value. The callable can be used for string formatting logic that         `.format(**kwargs)` doesn't support.     </li><li class="args">`state_handlers (Iterable[Callable], optional)`: A list of state change handlers         that will be called whenever the task changes state, providing an         opportunity to inspect or modify the new state. The handler         will be passed the task instance, the old (prior) state, and the new         (current) state, with the following signature:             `state_handler(task: Task, old_state: State, new_state: State) -> Optional[State]`         If multiple functions are passed, then the `new_state` argument will be the         result of the previous handler.     </li><li class="args">`on_failure (Callable, optional)`: A function with signature         `fn(task: Task, state: State) -> None` that will be called anytime this         Task enters a failure state     </li><li class="args">`log_stdout (bool, optional)`: Toggle whether or not to send stdout messages to         the Prefect logger. Defaults to `False`.     </li><li class="args">`task_run_name (Union[str, Callable], optional)`: a name to set for this task at runtime.         `task_run_name` strings can be templated formatting strings which will be         formatted at runtime with values from task arguments, `prefectlegacy.context`, and flow         parameters (in the case of a name conflict between these, earlier values take precedence).         If a callable function is provided, it should have signature `callable(**kwargs) -> str`         and at write time all formatting kwargs will be passed and a fully formatted location is         expected as the return value. The callable can be used for string formatting logic that         `.format(**kwargs)` doesn't support. **Note**: this only works for tasks running against a         backend API.     </li><li class="args">`nout (int, optional)`: for tasks that return multiple results, the number of outputs         to expect. If not provided, will be inferred from the task return annotation, if         possible.  Note that `nout=1` implies the task returns a tuple of         one value (leave as `None` for non-tuple return types).</li></ul> **Raises**:     <ul class="args"><li class="args">`TypeError`: if `tags` is of type `str`     </li><li class="args">`TypeError`: if `timeout` is not of type `int`</li></ul>

|methods: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|:----|
 | <div class='method-sig' id='prefect-core-task-task-bind'><p class="prefect-class">prefectlegacy.core.task.Task.bind</p>(*args, mapped=False, upstream_tasks=None, flow=None, **kwargs)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L638">[source]</a></span></div>
<p class="methods">Binding a task to (keyword) arguments creates a _keyed_ edge in the active Flow that will pass data from the arguments (whether Tasks or constants) to the Task's `run` method under the appropriate key. Once a Task is bound in this manner, the same task instance cannot be bound a second time in the same Flow.<br><br>To bind arguments to a _copy_ of this Task instance, see `__call__`. Additionally, non-keyed edges can be created by passing any upstream dependencies through `upstream_tasks`.<br><br>**Args**:     <ul class="args"><li class="args">`*args`: arguments to bind to the current Task's `run` method     </li><li class="args">`mapped (bool, optional)`: Whether the results of these tasks should be mapped over         with the specified keyword arguments; defaults to `False`.         If `True`, any arguments contained within a `prefectlegacy.utilities.edges.unmapped`         container will _not_ be mapped over.     </li><li class="args">`upstream_tasks ([Task], optional)`: a list of upstream dependencies for the         current task.     </li><li class="args">`flow (Flow, optional)`: The flow to set dependencies on, defaults to the current         flow in context if no flow is specified     </li><li class="args">`**kwargs`: keyword arguments to bind to the current Task's `run` method</li></ul> **Returns**:     <ul class="args"><li class="args">`Task`: the current Task instance</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-copy'><p class="prefect-class">prefectlegacy.core.task.Task.copy</p>(**task_args)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L498">[source]</a></span></div>
<p class="methods">Creates and returns a copy of the current Task.<br><br>**Args**:     <ul class="args"><li class="args">`**task_args (dict, optional)`: a dictionary of task attribute keyword arguments,         these attributes will be set on the new copy</li></ul> **Raises**:     <ul class="args"><li class="args">`AttributeError`: if any passed `task_args` are not attributes of the original</li></ul> **Returns**:     <ul class="args"><li class="args">`Task`: a copy of the current Task, with any attributes updated from `task_args`</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-inputs'><p class="prefect-class">prefectlegacy.core.task.Task.inputs</p>()<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L871">[source]</a></span></div>
<p class="methods">Describe the inputs for this task. The result is a dictionary that maps each input to a `type`, `required`, and `default`. All values are inferred from the `run()` signature; this method can be overloaded for more precise control.<br><br>**Returns**:     <ul class="args"><li class="args">dict</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-is-equal'><p class="prefect-class">prefectlegacy.core.task.Task.is_equal</p>(other)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L923">[source]</a></span></div>
<p class="methods">Produces a Task that evaluates `self == other`<br><br>This can't be implemented as the __eq__() magic method because of Task comparisons.<br><br>**Args**:     <ul class="args"><li class="args">`other (object)`: the other operand of the operator. It will be converted to a Task         if it isn't one already.</li></ul> **Returns**:     <ul class="args"><li class="args">Task</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-is-not-equal'><p class="prefect-class">prefectlegacy.core.task.Task.is_not_equal</p>(other)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L939">[source]</a></span></div>
<p class="methods">Produces a Task that evaluates `self != other`<br><br>This can't be implemented as the __neq__() magic method because of Task comparisons.<br><br>**Args**:     <ul class="args"><li class="args">`other (object)`: the other operand of the operator. It will be converted to a Task         if it isn't one already.</li></ul> **Returns**:     <ul class="args"><li class="args">Task</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-map'><p class="prefect-class">prefectlegacy.core.task.Task.map</p>(*args, upstream_tasks=None, flow=None, task_args=None, **kwargs)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L712">[source]</a></span></div>
<p class="methods">Map the Task elementwise across one or more Tasks. Arguments that should _not_ be mapped over should be placed in the `prefectlegacy.utilities.edges.unmapped` container.<br><br>For example:     <br><pre class="language-python"><code class="language-python">    task<span class="token operator">.</span>map<span class="token punctuation">(</span>x<span class="token operator">=</span>X<span class="token punctuation">,</span> y<span class="token operator">=</span>unmapped<span class="token punctuation">(</span>Y<span class="token punctuation">)</span><span class="token punctuation">)</span><br>    <br></code></pre><br> will map over the values of `X`, but not over the values of `Y`<br><br><br>**Args**:     <ul class="args"><li class="args">`*args`: arguments to map over, which will elementwise be bound to the Task's `run`         method     </li><li class="args">`upstream_tasks ([Task], optional)`: a list of upstream dependencies         to map over     </li><li class="args">`flow (Flow, optional)`: The flow to set dependencies on, defaults to the current         flow in context if no flow is specified     </li><li class="args">`task_args (dict, optional)`: a dictionary of task attribute keyword arguments,         these attributes will be set on the new copy     </li><li class="args">`**kwargs`: keyword arguments to map over, which will elementwise be bound to the         Task's `run` method</li></ul> **Raises**:     <ul class="args"><li class="args">`AttributeError`: if any passed `task_args` are not attributes of the original</li></ul> **Returns**:     <ul class="args"><li class="args">`Task`: a new Task instance</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-not'><p class="prefect-class">prefectlegacy.core.task.Task.not_</p>()<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L955">[source]</a></span></div>
<p class="methods">Produces a Task that evaluates `not self`<br><br>**Returns**:     <ul class="args"><li class="args">Task</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-or'><p class="prefect-class">prefectlegacy.core.task.Task.or_</p>(other)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L964">[source]</a></span></div>
<p class="methods">Produces a Task that evaluates `self or other`<br><br>**Args**:     <ul class="args"><li class="args">`other (object)`: the other operand of the operator. It will be converted to a Task         if it isn't one already.</li></ul> **Returns**:     <ul class="args"><li class="args">Task</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-outputs'><p class="prefect-class">prefectlegacy.core.task.Task.outputs</p>()<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L898">[source]</a></span></div>
<p class="methods">Get the output types for this task.<br><br>**Returns**:     <ul class="args"><li class="args">Any</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-run'><p class="prefect-class">prefectlegacy.core.task.Task.run</p>()<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L468">[source]</a></span></div>
<p class="methods">The `run()` method is called (with arguments, if appropriate) to run a task.<br><br>*Note:* The implemented `run` method cannot have `*args` in its signature. In addition, the following keywords are reserved: `upstream_tasks`, `task_args` and `mapped`.<br><br>If a task has arguments in its `run()` method, these can be bound either by using the functional API and _calling_ the task instance, or by using `self.bind` directly.<br><br>In addition to running arbitrary functions, tasks can interact with Prefect in a few ways: <ul><li> Return an optional result. When this function runs successfully,     the task is considered successful and the result (if any) can be     made available to downstream tasks. </li> <li> Raise an error. Errors are interpreted as failure. </li> <li> Raise a [signal](../engine/signals.html). Signals can include `FAIL`, `SUCCESS`,     `RETRY`, `SKIP`, etc. and indicate that the task should be put in the indicated state.         <ul>         <li> `FAIL` will lead to retries if appropriate </li>         <li> `SUCCESS` will cause the task to be marked successful </li>         <li> `RETRY` will cause the task to be marked for retry, even if `max_retries`             has been exceeded </li>         <li> `SKIP` will skip the task and possibly propogate the skip state through the             flow, depending on whether downstream tasks have `skip_on_upstream_skip=True`.         </li></ul> </li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-serialize'><p class="prefect-class">prefectlegacy.core.task.Task.serialize</p>()<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L912">[source]</a></span></div>
<p class="methods">Creates a serialized representation of this task<br><br>**Returns**:     <ul class="args"><li class="args">dict representing this task</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-set-dependencies'><p class="prefect-class">prefectlegacy.core.task.Task.set_dependencies</p>(flow=None, upstream_tasks=None, downstream_tasks=None, keyword_tasks=None, mapped=False, validate=None)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L763">[source]</a></span></div>
<p class="methods">Set dependencies for a flow either specified or in the current context using this task<br><br>**Args**:     <ul class="args"><li class="args">`flow (Flow, optional)`: The flow to set dependencies on, defaults to the current     flow in context if no flow is specified     </li><li class="args">`upstream_tasks ([object], optional)`: A list of upstream tasks for this task     </li><li class="args">`downstream_tasks ([object], optional)`: A list of downtream tasks for this task     </li><li class="args">`keyword_tasks ({str, object}}, optional)`: The results of these tasks will be provided     to this task under the specified keyword arguments.     </li><li class="args">`mapped (bool, optional)`: Whether the results of the _upstream_ tasks should be         mapped over with the specified keyword arguments     </li><li class="args">`validate (bool, optional)`: Whether or not to check the validity of the flow. If not         provided, defaults to the value of `eager_edge_validation` in your Prefect         configuration file.</li></ul> **Returns**:     <ul class="args"><li class="args">self</li></ul>**Raises**:     <ul class="args"><li class="args">`ValueError`: if no flow is specified and no flow can be found in the current context</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-set-downstream'><p class="prefect-class">prefectlegacy.core.task.Task.set_downstream</p>(task, flow=None, key=None, mapped=False)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L841">[source]</a></span></div>
<p class="methods">Sets the provided task as a downstream dependency of this task.<br><br>**Args**:     <ul class="args"><li class="args">`task (Task)`: A task that will be set as a downstream dependency of this task.     </li><li class="args">`flow (Flow, optional)`: The flow to set dependencies on, defaults to the current         flow in context if no flow is specified     </li><li class="args">`key (str, optional)`: The key to be set for the new edge; the result of this task         will be passed to the downstream task's `run()` method under this keyword argument.     </li><li class="args">`mapped (bool, optional)`: Whether this dependency is mapped; defaults to `False`</li></ul> **Returns**:     <ul class="args"><li class="args">self</li></ul>**Raises**:     <ul class="args"><li class="args">`ValueError`: if no flow is specified and no flow can be found in the current context</li></ul></p>|
 | <div class='method-sig' id='prefect-core-task-task-set-upstream'><p class="prefect-class">prefectlegacy.core.task.Task.set_upstream</p>(task, flow=None, key=None, mapped=False)<span class="source"><a href="https://github.com/PrefectHQ/prefect/blob/master/src/prefectlegacy/core/task.py#L811">[source]</a></span></div>
<p class="methods">Sets the provided task as an upstream dependency of this task.<br><br>**Args**:     <ul class="args"><li class="args">`task (object)`: A task or object that will be converted to a task that will be set         as a upstream dependency of this task.     </li><li class="args">`flow (Flow, optional)`: The flow to set dependencies on, defaults to the current         flow in context if no flow is specified     </li><li class="args">`key (str, optional)`: The key to be set for the new edge; the result of the         upstream task will be passed to this task's `run()` method under this keyword         argument.     </li><li class="args">`mapped (bool, optional)`: Whether this dependency is mapped; defaults to `False`</li></ul> **Returns**:     <ul class="args"><li class="args">self</li></ul>**Raises**:     <ul class="args"><li class="args">`ValueError`: if no flow is specified and no flow can be found in the current context</li></ul></p>|

---
<br>


<p class="auto-gen">This documentation was auto-generated from commit <a href='https://github.com/PrefectHQ/prefect/commit/n/a'>n/a</a> </br>on February 23, 2022 at 19:26 UTC</p>