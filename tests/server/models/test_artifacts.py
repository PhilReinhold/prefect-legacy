from uuid import uuid4

import pytest

from prefect.server import models, schemas
from prefect.server.schemas import actions


@pytest.fixture
async def artifact(session):
    artifact_schema = schemas.core.Artifact(
        key="voltaic", data=1, metadata_={"description": "opens many doors"}
    )
    artifact = await models.artifacts.create_artifact(
        key=artifact_schema.key, session=session, artifact=artifact_schema
    )
    await session.commit()
    return artifact


@pytest.fixture
async def artifacts(session):
    artifact1_schema = schemas.core.Artifact(
        key="voltaic", data=1, metadata_={"description": "opens many doors"}
    )
    artifact1 = await models.artifacts.create_artifact(
        key=artifact1_schema.key, session=session, artifact=artifact1_schema
    )

    artifact2_schema = schemas.core.Artifact(
        key="voltaic", data=2, metadata_={"description": "opens many doors"}
    )
    artifact2 = await models.artifacts.create_artifact(
        key=artifact2_schema.key, session=session, artifact=artifact2_schema
    )

    artifact3_schema = schemas.core.Artifact(
        key="voltaic", data=3, metadata_={"description": "opens many doors"}
    )
    artifact3 = await models.artifacts.create_artifact(
        key=artifact3_schema.key, session=session, artifact=artifact3_schema
    )

    yield [artifact1, artifact2, artifact3]


class TestCreateArtifacts:
    async def test_creating_artifact_without_key_succeeds(self, session):
        artifact_schema = schemas.core.Artifact(
            data=1, metadata_={"description": "opens many doors"}
        )
        artifact = await models.artifacts.create_artifact(
            session=session, artifact=artifact_schema
        )

        read_artifact = await models.artifacts.read_artifact(session, artifact.id)
        assert read_artifact.data == artifact_schema.data
        assert read_artifact.metadata_ == artifact_schema.metadata_

    async def test_creating_artifact_with_key_upserts_to_artifact_collection(
        self, artifact, session
    ):
        newest_artifact_version = await models.artifacts.read_latest_artifact(
            session=session, key=artifact.key
        )
        assert newest_artifact_version.latest_id == artifact.id
        assert newest_artifact_version.key == artifact.key

    async def test_creating_artifact_without_key_arg_does_not_upsert_to_artifact_collection(
        self, session
    ):
        artifact_schema = schemas.core.Artifact(
            key="lotus", data=1, metadata_={"description": "opens many doors"}
        )
        artifact = await models.artifacts.create_artifact(
            # no key arg is specified
            session=session,
            artifact=artifact_schema,
        )

        newest_artifact_version = await models.artifacts.read_latest_artifact(
            session=session, key=artifact.key
        )
        assert newest_artifact_version is None

    async def test_creating_artifact_with_key_already_in_artifact_collection_updates_row(
        self, artifact, session
    ):
        latest_artifact_version = await models.artifacts.read_latest_artifact(
            session=session, key=artifact.key
        )
        assert latest_artifact_version.latest_id == artifact.id
        assert latest_artifact_version.updated == latest_artifact_version.created

        new_artifact_schema = schemas.core.Artifact(
            key=artifact.key, data=2, metadata_={"description": "opens many doors"}
        )
        assert new_artifact_schema.id != artifact.id
        new_artifact = await models.artifacts.create_artifact(
            session=session, artifact=new_artifact_schema, key=new_artifact_schema.key
        )

        new_artifact_version = await models.artifacts.read_latest_artifact(
            session=session, key=artifact.key
        )
        assert new_artifact_version.latest_id == new_artifact.id
        assert new_artifact_version.created < new_artifact_version.updated

    async def test_creating_artifact_with_null_key_does_not_upsert_to_artifact_collection(
        self, session
    ):
        artifact_schema = schemas.core.Artifact(
            data=1, metadata_={"description": "opens many doors"}
        )
        artifact = await models.artifacts.create_artifact(
            key=artifact_schema.key, session=session, artifact=artifact_schema
        )

        newest_artifact_version = await models.artifacts.read_latest_artifact(
            session=session, key=artifact.key
        )
        assert newest_artifact_version is None


class TestUpdateArtifacts:
    async def test_update_artifact_succeeds(self, artifact, session):
        new_metadata = {"description": "opens all doors"}

        assert await models.artifacts.update_artifact(
            session=session,
            artifact_id=artifact.id,
            artifact=actions.ArtifactUpdate(metadata_=new_metadata),
        )

        updated_artifact = await models.artifacts.read_artifact(session, artifact.id)
        assert updated_artifact.metadata_ == new_metadata

    async def test_update_artifact_fails_if_missing(self, session):
        updated_result = await models.artifacts.update_artifact(
            session=session,
            artifact_id=str(uuid4()),
            artifact=actions.ArtifactUpdate(
                metadata_={"description": "opens many doors"}
            ),
        )
        assert not updated_result

    async def test_update_artifact_does_not_update_if_fields_not_set(
        self, artifact, session
    ):
        assert await models.artifacts.update_artifact(
            session=session, artifact_id=artifact.id, artifact=actions.ArtifactUpdate()
        )

        unchanged_artifact = await models.artifacts.read_artifact(session, artifact.id)
        assert unchanged_artifact.data == artifact.data
        assert unchanged_artifact.metadata_ == artifact.metadata_


class TestReadingSingleArtifacts:
    async def test_reading_artifacts_by_id(self, session):
        artifact_schema = schemas.core.Artifact(
            key="voltaic", data=1, metadata_={"description": "opens many doors"}
        )
        artifact = await models.artifacts.create_artifact(
            session=session, artifact=artifact_schema
        )

        tutored_artifact = await models.artifacts.read_artifact(session, artifact.id)

        assert tutored_artifact.key == artifact_schema.key
        assert tutored_artifact.data == artifact_schema.data
        assert tutored_artifact.metadata_ == artifact_schema.metadata_

    async def test_reading_artifacts_returns_none_if_missing(self, session):
        tutored_artifact = await models.artifacts.read_artifact(session, str(uuid4()))

        assert tutored_artifact is None


class TestReadingMultipleArtifacts:
    @pytest.fixture
    async def artifacts(self, flow_run, task_run, session):
        # create 3 artifacts w/ diff keys
        artifact1_schema = schemas.core.Artifact(
            key="voltaic1",
            data=1,
            metadata_={"description": "opens many doors"},
            flow_run_id=flow_run.id,
            task_run_id=task_run.id,
        )
        artifact1 = await models.artifacts.create_artifact(
            session=session, artifact=artifact1_schema
        )

        artifact2_schema = schemas.core.Artifact(
            key="voltaic2",
            data=2,
            metadata_={"description": "opens many doors"},
            flow_run_id=flow_run.id,
            task_run_id=task_run.id,
        )
        artifact2 = await models.artifacts.create_artifact(
            session=session, artifact=artifact2_schema
        )

        artifact3_schema = schemas.core.Artifact(
            key="voltaic3",
            data=3,
            metadata_={"description": "opens many doors"},
        )
        artifact3 = await models.artifacts.create_artifact(
            session=session, artifact=artifact3_schema
        )
        yield [artifact1, artifact2, artifact3]

    async def test_reading_artifacts_by_ids(self, artifacts, session):
        artifact_ids = [artifact.id for artifact in artifacts]
        artifact_filter = schemas.filters.ArtifactFilter(
            id=schemas.filters.ArtifactFilterId(
                any_=[artifact_ids[0], artifact_ids[1], artifact_ids[2]]
            )
        )
        tutored_artifacts = await models.artifacts.read_artifacts(
            session, artifact_filter=artifact_filter
        )

        assert len(tutored_artifacts) == 3
        assert tutored_artifacts[0].id in artifact_ids
        assert tutored_artifacts[1].id in artifact_ids
        assert tutored_artifacts[2].id in artifact_ids

    async def test_reading_artifacts_by_keys(self, artifacts, session):
        artifact_keys = [artifact.key for artifact in artifacts]
        artifact_filter = schemas.filters.ArtifactFilter(
            key=schemas.filters.ArtifactFilterKey(
                any_=[artifact_keys[1], artifact_keys[2]]
            )
        )
        tutored_artifacts = await models.artifacts.read_artifacts(
            session, artifact_filter=artifact_filter
        )

        assert len(tutored_artifacts) == 2
        assert tutored_artifacts[0].key in artifact_keys
        assert tutored_artifacts[1].key in artifact_keys

    async def test_reading_artifacts_by_flow_run_id(self, artifacts, session):
        flow_run_ids = [artifact.flow_run_id for artifact in artifacts]
        artifact_filter = schemas.filters.ArtifactFilter(
            flow_run_id=schemas.filters.ArtifactFilterFlowRunId(any_=[flow_run_ids[1]])
        )
        tutored_artifacts = await models.artifacts.read_artifacts(
            session, artifact_filter=artifact_filter
        )

        assert len(tutored_artifacts) == 2
        assert tutored_artifacts[0].flow_run_id == flow_run_ids[1]
        assert tutored_artifacts[1].flow_run_id == flow_run_ids[1]

    async def test_reading_artifacts_by_task_run_id(self, artifacts, session):
        task_run_ids = [artifact.task_run_id for artifact in artifacts]
        artifact_filter = schemas.filters.ArtifactFilter(
            task_run_id=schemas.filters.ArtifactFilterTaskRunId(
                any_=[task_run_ids[0], task_run_ids[1]]
            )
        )
        tutored_artifacts = await models.artifacts.read_artifacts(
            session, artifact_filter=artifact_filter
        )

        assert len(tutored_artifacts) == 2
        assert tutored_artifacts[0].task_run_id == task_run_ids[0]
        assert tutored_artifacts[1].task_run_id == task_run_ids[1]

    async def test_reading_artifacts_by_flow_run(self, artifacts, session):
        flow_run_ids = [artifact.flow_run_id for artifact in artifacts]
        flow_run_filter = schemas.filters.FlowRunFilter(
            id=schemas.filters.FlowRunFilterId(any_=[flow_run_ids[0]])
        )
        tutored_artifacts = await models.artifacts.read_artifacts(
            session, flow_run_filter=flow_run_filter
        )

        assert len(tutored_artifacts) == 2
        assert tutored_artifacts[0].flow_run_id == flow_run_ids[0]

    async def test_reading_artifacts_by_task_run(self, artifacts, session):
        task_run_ids = [artifact.task_run_id for artifact in artifacts]
        task_run_filter = schemas.filters.TaskRunFilter(
            id=schemas.filters.TaskRunFilterId(any_=[task_run_ids[0]])
        )
        tutored_artifacts = await models.artifacts.read_artifacts(
            session, task_run_filter=task_run_filter
        )

        assert len(tutored_artifacts) == 2
        assert tutored_artifacts[0].task_run_id == task_run_ids[0]

    async def test_reading_artifacts_flow_run_filter_returns_empty_list_if_missing(
        self, session
    ):
        tutored_artifacts = await models.artifacts.read_artifacts(session)

        assert len(tutored_artifacts) == 0


class TestDeleteArtifacts:
    async def test_delete_only_artifact_deletes_row_in_artifact_and_artifact_collection(
        self, session
    ):
        artifact_schema = schemas.core.Artifact(
            key="voltaic", data=1, metadata_={"description": "opens many doors"}
        )
        artifact = await models.artifacts.create_artifact(
            session=session, artifact=artifact_schema
        )

        assert await models.artifacts.delete_artifact(session, artifact.id)

        artifact_result = await models.artifacts.read_artifact(session, artifact.id)
        assert artifact_result is None

        artifact_collection_result = await models.artifacts.read_latest_artifact(
            session, artifact.key
        )
        assert artifact_collection_result is None

    async def test_delete_earliest_artifact_deletes_row_in_artifact_and_ignores_artifact_collection(
        self, artifacts, session
    ):
        assert await models.artifacts.delete_artifact(session, artifacts[0].id)

        artifact_result = await models.artifacts.read_artifact(session, artifacts[0].id)
        assert artifact_result is None

        artifact_collection_result = await models.artifacts.read_latest_artifact(
            session, artifacts[0].key
        )
        assert artifact_collection_result.latest_id == artifacts[2].id
        assert artifact_collection_result.key == artifacts[2].key

    async def test_delete_middle_artifact_deletes_row_in_artifact_and_ignores_artifact_collection(
        self, artifacts, session
    ):
        assert await models.artifacts.delete_artifact(session, artifacts[1].id)

        artifact_result = await models.artifacts.read_artifact(session, artifacts[1].id)
        assert artifact_result is None

        artifact_collection_result = await models.artifacts.read_latest_artifact(
            session, artifacts[1].key
        )
        assert artifact_collection_result.latest_id == artifacts[2].id
        assert artifact_collection_result.key == artifacts[2].key

    async def test_delete_latest_artifact_deletes_row_in_artifact_and_updates_artifact_collection(
        self, artifacts, session
    ):
        assert await models.artifacts.delete_artifact(session, artifacts[2].id)

        artifact_result = await models.artifacts.read_artifact(session, artifacts[2].id)
        assert artifact_result is None

        artifact_collection_result = await models.artifacts.read_latest_artifact(
            session, artifacts[2].key
        )
        assert artifact_collection_result.latest_id == artifacts[1].id
        assert artifact_collection_result.key == artifacts[1].key

    async def test_delete_artifact_fails_if_missing(self, session):
        deleted_result = await models.artifacts.delete_artifact(session, str(uuid4()))

        assert not deleted_result
