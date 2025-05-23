from __future__ import annotations

from datasets import load_dataset

from mteb.abstasks.TaskMetadata import TaskMetadata

from ....abstasks.AbsTaskRetrieval import AbsTaskRetrieval


class HunSum2AbstractiveRetrieval(AbsTaskRetrieval):
    metadata = TaskMetadata(
        name="HunSum2AbstractiveRetrieval",
        dataset={
            "path": "SZTAKI-HLT/HunSum-2-abstractive",
            "revision": "24e1445c8180d937f0a16f8ae8a62e77cc952e56",
        },
        description=(
            "HunSum-2-abstractive is a Hungarian dataset containing news articles along with lead, titles and metadata."
        ),
        reference="https://arxiv.org/abs/2404.03555",
        type="Retrieval",
        category="s2p",
        modalities=["text"],
        eval_splits=["test"],
        eval_langs=["hun-Latn"],
        main_score="ndcg_at_1",
        date=(
            "1848-12-15",
            "2024-03-19",
        ),
        domains=["News", "Written"],
        task_subtypes=["Article retrieval"],
        license="cc-by-4.0",
        annotations_creators="derived",
        dialect=[],
        sample_creation="found",
        bibtex_citation=r"""
@misc{barta2024news,
  archiveprefix = {arXiv},
  author = {Botond Barta and Dorina Lakatos and Attila Nagy and Milán Konor Nyist and Judit Ács},
  eprint = {2404.03555},
  primaryclass = {cs.CL},
  title = {From News to Summaries: Building a Hungarian Corpus for Extractive and Abstractive Summarization},
  year = {2024},
}
""",
    )

    def load_data(self, **kwargs):
        if self.data_loaded:
            return
        self.corpus, self.queries, self.relevant_docs = {}, {}, {}
        ds = load_dataset(**self.metadata.dataset, split=self.metadata.eval_splits)
        ds = dict(zip(self.metadata.eval_splits, ds))
        for split_name, split in ds.items():
            self.corpus[split_name] = {}
            self.queries[split_name] = {}
            self.relevant_docs[split_name] = {}
            for record in split:
                self.corpus[split_name]["d" + record["uuid"]] = {
                    "title": record["title"],
                    "text": record["article"],
                }
                self.queries[split_name]["q" + record["uuid"]] = record["lead"]
                self.relevant_docs[split_name]["q" + record["uuid"]] = {
                    "d" + record["uuid"]: 1
                }
        self.data_loaded = True
