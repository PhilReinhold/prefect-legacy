# Run a flow

Now that you have Prefect installed,  you're ready to run a flow.

A [flow](/core/concepts/flows.html) is a container for [tasks](/core/concepts/tasks.html) and shows the direction of work and the dependencies between tasks.

To run your flow, paste the code below into an interactive Python REPL session: 

```python
import prefectlegacy
from prefectlegacy import task, Flow

@task
def hello_task():
    logger = prefectlegacy.context.get("logger")
    logger.info("Hello world!")

with Flow("hello-flow") as flow:
    hello_task()

flow.run()
```

You should see the following logs after running `flow.run()`:

```
[2020-01-08 23:49:00,239] INFO - prefectlegacy.FlowRunner | Beginning Flow run for 'hello-flow'
[2020-01-08 23:49:00,242] INFO - prefectlegacy.FlowRunner | Starting flow run.
[2020-01-08 23:49:00,249] INFO - prefectlegacy.TaskRunner | Task 'hello_task': Starting task run...
[2020-01-08 23:49:00,249] INFO - prefectlegacy.Task: hello_task | Hello world!
[2020-01-08 23:49:00,251] INFO - prefectlegacy.TaskRunner | Task 'hello_task': finished task run for task with final state: 'Success'
[2020-01-08 23:49:00,252] INFO - prefectlegacy.FlowRunner | Flow run SUCCESS: all reference tasks succeeded
```

And that's it.  You have run your first Prefect flow using Prefect Core!  
