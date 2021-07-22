from prefect.core import flow
from prefect.orion import schemas


async def test_create_then_read_flow(orion_client):
    @flow
    def foo():
        pass

    flow_id = await orion_client.create_flow(foo)
    assert isinstance(flow_id, str)

    lookup = await orion_client.read_flow(flow_id)
    assert isinstance(lookup, schemas.api.Flow)
    assert lookup.name == foo.name
    assert lookup.tags == list(foo.tags)
    assert lookup.parameters == foo.parameters


async def test_create_then_read_flow_run(orion_client):
    @flow
    def foo():
        pass

    flow_run_id = await orion_client.create_flow_run(foo)
    assert isinstance(flow_run_id, str)

    lookup = await orion_client.read_flow_run(flow_run_id)
    assert isinstance(lookup, schemas.api.FlowRun)
    assert lookup.tags == list(foo.tags)

    # TODO: Check parameters
