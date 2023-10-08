import json
import os

from db.models.dataset import Dataset
from db.setup import SessionLocal, get_db
from embedding.embedding import embed


def addDatasets():
    # db = get_db()
    db = SessionLocal()

    rootdir = "dataset-info"

    for subdir, dirs, files in os.walk(rootdir):
        if len(files) > 0:
            dataset = Dataset()
            if "metadata.json" in files:
                metadataFile = open(os.path.join(subdir, "metadata.json"))
                metadata = json.loads(metadataFile.read())
                dataset.title = metadata["title"]
                dataset.description = metadata["description"]
                metadataFile.close()

                # if already exists, continue
                if db.query(Dataset).where(Dataset.title == dataset.title).first():
                    continue

            if "sample.csv" in files:
                sampleFile = open(os.path.join(subdir, "sample.csv"))
                dataset.sampleData = sampleFile.read()
                sampleFile.close()
            if "embedding.txt" in files:
                embeddingFile = open(os.path.join(subdir, "embedding.txt"))
                embeddingText = embeddingFile.read()
                embedding = embed(embeddingText)
                dataset.embedding = embedding
                embeddingFile.close()

            db.add(dataset)
            db.commit()


if __name__ == "__main__":
    addDatasets()
