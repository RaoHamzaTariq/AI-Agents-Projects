from astra.connection import connect_to_database
from astrapy.constants import VectorMetric
from astrapy.info import (
    CollectionDefinition,
    CollectionVectorOptions,
    VectorServiceOptions,
)


def main() -> None:
    database = connect_to_database()

    collection = database.create_collection(
        "testing_collection",
        definition=CollectionDefinition(
            vector=CollectionVectorOptions(
                metric=VectorMetric.COSINE,
                service=VectorServiceOptions(
                    provider="nvidia",
                    model_name="NV-Embed-QA",
                ),
            )
        ),
    )

    print(f"Created collection {collection.full_name}")


if __name__ == "__main__":
    main()