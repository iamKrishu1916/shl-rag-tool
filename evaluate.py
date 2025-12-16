from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset
import os

eval_data = {
    "question": ["I need a test for logical reasoning", "What is good for personality?"],
    "answer": ["The Verify G+ test is ideal as it covers inductive and deductive reasoning.", "OPQ32 is the standard for behavioral style."],
    "contexts": [["Verify G+ covers cognitive ability."], ["OPQ32 measures behavioral style."]],
    "ground_truth": ["Verify G+ is the best choice.", "OPQ32 is for personality."]
}

def run_eval():
    print("Running RAGAS evaluation...")
    dataset = Dataset.from_dict(eval_data)
    
    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy]
    )
    
    print("\nEvaluation Results:")
    print(results)

if __name__ == "__main__":
    run_eval()