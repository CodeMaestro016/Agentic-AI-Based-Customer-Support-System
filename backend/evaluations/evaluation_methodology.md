# How to Measure Agent Performance Metrics

This document explains how to obtain the performance metrics for each agent in the Agentic AI-Based Customer Support System.

## 1. Accuracy Measurement

### Methodology:
- Create a test dataset with known correct answers
- Run each query through the agent
- Compare the agent's output with the expected result
- Calculate accuracy as: (Correct Responses / Total Tests) × 100

### Example Implementation:
```python
def measure_accuracy(agent, test_cases):
    correct = 0
    total = len(test_cases)
    
    for input_query, expected_output in test_cases:
        actual_output = agent.process(input_query)
        if actual_output == expected_output:
            correct += 1
    
    accuracy = (correct / total) * 100
    return accuracy
```

## 2. Response Time Measurement

### Methodology:
- Record the time before calling the agent
- Call the agent with a test query
- Record the time after the agent responds
- Calculate the difference

### Example Implementation:
```python
import time

def measure_response_time(agent, query):
    start_time = time.time()
    response = agent.process(query)
    end_time = time.time()
    
    response_time = end_time - start_time
    return response_time
```

## 3. Special Features Assessment

### Methodology:
- Document the unique capabilities of each agent
- Count the number of distinct features
- Qualitatively assess feature quality

## 4. Actual Metrics Generation

Instead of hardcoding results, the evaluation system should generate metrics dynamically by:

1. Running comprehensive test cases for each agent
2. Measuring response times for each query
3. Calculating accuracy based on correct classifications
4. Documenting special features observed during testing

### Example Evaluation Process:
```python
# evaluation_runner.py
from agents import QueryClassifierAgent, RAGAgent, SolutionAgent
import time
import json

def run_evaluation():
    # Initialize agents
    classifier = QueryClassifierAgent()
    
    # Test data with expected results
    test_queries = [
        ("I have a headache", "symptom_inquiry"),
        ("What are your hours?", "center_information"),
        # ... more test cases
    ]
    
    # Measure accuracy and response times
    correct = 0
    response_times = []
    
    for query, expected in test_queries:
        start = time.time()
        result = classifier.classify_query(query)
        end = time.time()
        
        response_times.append(end - start)
        
        if result["intent"] == expected:
            correct += 1
    
    accuracy = (correct / len(test_queries)) * 100
    avg_response_time = sum(response_times) / len(response_times)
    
    # Return actual measured metrics
    return {
        "accuracy": accuracy,
        "avg_response_time": avg_response_time,
        "total_tests": len(test_queries),
        "correct_classifications": correct
    }

if __name__ == "__main__":
    # Run evaluation for each agent
    results = {}
    results["query_classifier"] = run_evaluation()
    
    # Save results to file
    with open("agent_metrics.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Display formatted results
    print("Agent Evaluation Results:")
    print(f"Query Classifier - Accuracy: {results['query_classifier']['accuracy']:.1f}%, "
          f"Response Time: {results['query_classifier']['avg_response_time']:.2f}s")
```

## 5. Running Your Own Evaluation

To run a full evaluation of your system:

1. Create test datasets for each agent with known correct answers
2. Implement timing measurements using Python's time module
3. Compare outputs with expected results to calculate accuracy
4. Document special features observed during testing
5. Save results for reporting in both console and JSON format

The actual metrics will be generated when you run the evaluation script, providing real performance data rather than estimates.